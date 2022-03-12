import logging
import unittest
import sys
from torrent_geolocation.main import *

class Test_main(unittest.TestCase):

    def test_main_flow_ip2_multi(self):
        tFile = r'C:\Users\aspire\Downloads\torrent_geolocation\test\test.torrent'
        geo_total = get_all_geoinfo(tFile, 'ip2_multi', 10)
        save_geo_list(geo_total)
        plot_worldmap()


    def test_all_announce_list(self):
        torrent_file = r'C:\Users\aspire\Downloads\torrent_geolocation\test\test.torrent'
        rst = all_announce_list(torrent_file)

        msg = ""
        for i, it in enumerate(rst):
            msg += f"{it}    "
            if (i+1) % 5 == 0:
                msg += '\n'
        msg = "\n\n" + msg + "\n\n"

        log = logging.getLogger()
        log.error(msg)
        self.assertEqual(1, 1)
