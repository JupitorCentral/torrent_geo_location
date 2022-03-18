# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import os
import argparse
import string
import sys
from threading import local
print(os.getcwd())

try: 
    from torrent_geolocation.main import main
except:
    from main import main


def execute_with_args():
    args = sys.argv[:]
    prog_name = os.path.basename(args[0])
    parser = argparse.ArgumentParser(
        prog=prog_name, description='Show geo locations of announces of torrent file')
    parser.add_argument(
        'TORRENT_FILE', help=r"Torrent file to show its announce's location")
    parser.add_argument('-m', '--method', dest='method', help='which method to fetch geo infos. default : ip2',
                        default='ip2', choices=['ip2', 'ipapi'])
    parser.add_argument('-n', '--processes', dest='num_process', type=int, help='when using ip2, how many processes for fetching.' + \
                        ' Too many processes are more likely to fail to fetch.' + \
                        ' recommend 6-10, default = 6'
                        )

    args = parser.parse_args(args[1:])
    main(args)


if __name__ == '__main__':
    execute_with_args()
