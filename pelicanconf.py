#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Diego Garcia'
SITENAME = u'Diego Garcia'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Social widget
SOCIAL = (
    ('twitter', 'https://twitter.com/drgarcia1986'),
    ('github', 'https://github.com/drgarcia1986'),
    ('linkedin', 'https://www.linkedin.com/in/drgarcia1986'),
)

DEFAULT_PAGINATION = 10

# Articles and urls
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

# Theme
THEME = 'theme'
COLOR_SCHEME_CSS = 'monokai.css'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['summary']

SUMMARY_END_MARKER = '<!-- more -->'

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}
