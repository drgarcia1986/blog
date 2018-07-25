#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://drgarcia1986.github.io/blog'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'atom.xml'
CATEGORY_FEED_ATOM = '%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = 'codeforcloud'
GOOGLE_ANALYTICS = 'UA-56972446-1'
ADDTHIS_PUBID = 'ra-56c73262ac2c1b1d'

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
