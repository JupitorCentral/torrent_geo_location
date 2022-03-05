
import json, socket, io
from urllib import request as req
from urllib import parse
from ip2geotools.databases.noncommercial import DbIpCity
import importlib, folium, webbrowser
import torrent_parser

def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]
# globals(), locals()


def all_announce_list(torrent_file_name):
    # f = open(torrent_file)
    d = torrent_parser.parse_torrent_file(torrent_file_name)
    # d = json.load(f)
    l = []
    for a in d['announce-list']:
        o = parse.urlparse(a[0])
        k = o.netloc.find(':')
        if k == -1:
            l.append(o.netloc)
        else:
            l.append(o.netloc[0:o.netloc.find(':')])
    return l



def get_geoinfo_ipapi(target):
    info_server = 'http://ip-api.com/json/'
    print(f"target : {target}")
    ip = socket.gethostbyname(target)
    rep = req.urlopen(info_server+ip)
    d = json.load(rep)

    # status country countryCode region regionName city zip lat lon timezone isp org as query
    r = (d['regionName'], d['lat'], d['lon'])
    return r


def get_geoinfo_ip2(target):
    print(target)
    ip = socket.gethostbyname(target)
    rep = DbIpCity.get(ip, api_key='free')
    return (rep.region, rep.latitude, rep.longitude)


def get_all_geoinfo(torrent_file):
    alist = all_announce_list(torrent_file_name=torrent_file)

    geo_list = []
    for domain in alist:
        try:
            info = get_geoinfo_ip2(domain)
            if info.count(None) > 0:
                continue
            geo_list.append(info)
        except:
            pass

    return geo_list


def plot_worldmap():

    md = importlib.import_module('variables')
    geo_list = md.geo_list


    m = folium.Map(location=[sum(j for i, j, k in geo_list)/len(geo_list), sum(k for i, j, k in geo_list)/len(geo_list)],
                    zoom_start=3)
    for cood in geo_list:
        folium.Marker(
            [cood[1], cood[2]], popup=f"{cood[0]}"
        ).add_to(m)

    m.save('map.html')
    webbrowser.open('map.html')


def save_geo_list(geo_list):

    # save list
    f = open('variables.py', 'w', encoding='utf-8')

    f.write(f"geo_list = {geo_list}")
    f.close()
    
def test():
    # md = importlib.import_module('variables')
    # geo_list = md.geo_list
    # print(geo_list))
    pass

if __name__ == '__main__':
    tfile = 'result.json'
    tfile = 'test.torrent'
    geo_total = get_all_geoinfo(tfile)
    save_geo_list(geo_total)
    plot_worldmap()

    # test()