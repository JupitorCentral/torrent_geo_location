
import json
import re
import socket
from turtle import width
from urllib import request as req
from urllib import parse
from ip2geotools.databases.noncommercial import DbIpCity
from gcmap import GCMapper
import importlib


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]
# globals(), locals()


def all_announce_list(torrent_file):
    f = open(torrent_file)
    d = json.load(f)
    l = []
    for a in d['announce-list']:
        o = parse.urlparse(a[0])
        k = o.netloc.find(':')
        if k == -1:
            l.append(o.netloc)
        else:
            l.append(o.netloc[0:o.netloc.find(':')])
    return l

# geo test


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
    alist = all_announce_list(torrent_file=torrent_file)

    geo_list = []
    for domain in alist:
        try:
            geo_list.append(get_geoinfo_ip2(domain))
        except:
            pass

    return geo_list


def plot_worldmap():

    m = importlib.import_module('variables')
    geo_list = m.geo_list

    width, height = 800, 600
    bgcol = (255, 255, 255)


    lons1, lats1 = [], []
    for x in geo_list:
        lons1.append(x[2])
        lats1.append(x[1])

    # lons1 = [-79.4, -73.9, -122.4, -123.1, -0.1]
    # lats1 = [43.7,  40.7,   37.8,   49.2,  51.5]
    lons2 = lons1[1:] + lons1[:1]
    lats2 = lats1[1:] + lats1[:1]

    gcm = GCMapper(width=width, height=height, bgcol=bgcol)
    gcm.set_data(lons1, lats1, lons2, lats2)
    img = gcm.draw()
    img.save('output.png')


def test_save_geo_list(geo_list):

    # save list
    f = open('variables.py', 'w', encoding='utf-8')

    # f.write('variables = {\n')
    # for x in geo_list:
    #     f.write(f"\t\"{namestr(x, locals())[0]}\" : {x},\n")
    # f.write('}\n')
    f.write(f"geo_list = {geo_list}")
    f.close()
    

def test_implib():
    m = importlib.import_module('variables')

    geo_list = m.geo_list


if __name__ == '__main__':
    tfile = 'result.json'
    # geo_total = get_all_geoinfo(tfile)

    plot_worldmap()
    # print(type(geo_total))

    # print(geo_total)
    # test_save_geo_list(geo_total)
    # test_implib()