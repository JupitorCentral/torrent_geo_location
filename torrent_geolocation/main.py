
import json
import socket
import queue
import string
import torrent_parser
import importlib
import folium
import webbrowser
import multiprocessing as mtp
import re
from urllib import request as req
from urllib import parse
from ip2geotools.databases.noncommercial import DbIpCity


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]
# globals(), locals()


def all_announce_list(torrent_file_name):
    print("parsing torrent file...")
    d = torrent_parser.parse_torrent_file(torrent_file_name)
    l = []

    for a in d['announce-list']:
        l.append(re.sub('/announce', '', a[0]))

    return l


def get_geoinfo_ipapi(target):
    info_server = 'http://ip-api.com/json/'
    print(f"target : {target}")
    ip = socket.gethostbyname(target)
    rep = req.urlopen(info_server+ip)
    d = json.load(rep)

    # status country countryCode region regionName city zip lat lon timezone isp org as query
    r = (d['regionName'], d['lat'], d['lon'], target)
    return r


def get_geoinfo_ip2(target):
    print(target)
    ip = socket.gethostbyname(target)
    rep = DbIpCity.get(ip, api_key='free')
    return (rep.region, rep.latitude, rep.longitude, target)


# return : region, latitude, longitude, url
def get_geoinfo_ip2_multi(alist_q: mtp.Queue, geo_list_q: mtp.Queue):

    while True:
        try:
            url = alist_q.get_nowait()
        except queue.Empty:
            break
        else:
            try:
                o = parse.urlparse(url)
                k = o.netloc.find(':')
                if k == -1:
                    domain = o.netloc
                else:
                    domain = o.netloc[0:o.netloc.find(':')]
                ip = socket.gethostbyname(domain)
            except:
                print(f"{url} : Faild")
                continue
            print(url)
            rep = DbIpCity.get(ip, api_key='free')
            item = (rep.region, rep.latitude, rep.longitude, url)
            if item.count(None) == 0:
                geo_list_q.put(item)

    return True


def get_all_geoinfo(torrent_file: string, ip_method: string, pr_number: int = 0):
    alist = all_announce_list(torrent_file_name=torrent_file)
    geo_list = []

    print('fetching geo infos...')
    if ip_method == 'ip2_multi':

        alist_q = mtp.Queue()
        geo_list_q = mtp.Queue()

        for domain in alist:
            alist_q.put(domain)

        prs = []

        pr_count = mtp.cpu_count() if pr_number == 0 else pr_number

        for _ in range(pr_count):
            pr = mtp.Process(target=get_geoinfo_ip2_multi,
                             args=(alist_q, geo_list_q))
            prs.append(pr)
            pr.start()
        for pr in prs:
            pr.join(3.0)
        geo_list_q.put('STOP')

        for item in iter(geo_list_q.get, 'STOP'):
            geo_list.append(item)
        return geo_list

    for domain in alist:
        try:
            if ip_method == 'ip2':
                info = get_geoinfo_ip2(domain)
            elif ip_method == 'ipapi':
                info = get_geoinfo_ipapi(domain)

            else:
                print('wrong ip get method')
                break
            if info.count(None) > 0:
                continue
            geo_list.append(info)
        except:
            pass

    return geo_list


def plot_worldmap():

    print('plotting...')
    md = importlib.import_module('variables')
    geo_list = md.geo_list

    m = folium.Map(location=[sum(j for i, j, k, l in geo_list)/len(geo_list), sum(k for i, j, k, l in geo_list)/len(geo_list)],
                   zoom_start=3)
    for cood in geo_list:
        folium.Marker(
            [cood[1], cood[2]], popup=f"{cood[0]}", tooltip=cood[3]
        ).add_to(m)

    m.save('map.html')
    webbrowser.open('map.html')


def save_geo_list(geo_list):

    # save list
    f = open('variables.py', 'w', encoding='utf-8')

    f.write(f"geo_list = {geo_list}")
    f.close()


def main():

    tfile = 'test.torrent'

    # ip2, ipapi, ip2_multi
    geo_total = get_all_geoinfo(tfile, 'ip2_multi', 10)
    save_geo_list(geo_total)
    plot_worldmap()