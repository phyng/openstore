#!/usr/bin/env python
# coding: utf-8
# Author: phyng
# Date: 2014-09-19

from store.models import App, Imglist
import django
django.setup()

import sys
import json
import time

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "playstore.settings")

import requesocks as requests
from zlib import crc32
from PIL import Image
from StringIO import StringIO
import pathlib


def exists(url):

    filename = str(hex(crc32(url) & 0xffffffff))[2:] + ".png"

    path = os.path.dirname(__file__) + "/img/"
    fullpath = path + filename

    isexists = pathlib.Path(fullpath).exists()

    if isexists:
        return filename
    else:
        return False

if __name__ == '__main__':
    main()
