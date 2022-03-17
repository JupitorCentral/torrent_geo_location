# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
import os
import argparse
import string
from threading import local



def execute_with_args():
    parser = argparse.ArgumentParser(description='Show geo locations of announces of torrent file')
    parser.add_argument('torrent_file', metavar='file', type=string, nargs=1,
    help='show locations of announces. main function')
    
    args = parser.parse_args()
    



if __name__ == '__main__':
    execute_with_args()
    
