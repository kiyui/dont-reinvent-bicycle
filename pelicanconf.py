#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Timur Kiyui'
SITENAME = 'dont reinvent велосипед'
SITEURL = ''

# Site options
TIMEZONE = 'Asia/Kuching'
DEFAULT_LANG = 'en'
THEME = 'theme/'

# Site customization
PLUGIN_PATHS = ["pelican-plugins"]
PLUGINS = ["sitemap", "gzip_cache"]

# Plugin options
SITEMAP = {
    'format': 'xml',
    'changefreqs': {
        'pages': 'weekly',
        'indexes': 'daily',
        'articles': 'daily'
    }
}

# Compilation settings
PATH = 'content'
RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True

# Feed settings
FEED_DOMAIN = SITEURL
FEED_MAX_ITEMS = 10

FEED_ATOM = 'feeds/atom.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_RSS = 'feeds/all.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'

# Options
DEFAULT_PAGINATION = 10

# Blogroll
LINKS = (('GNOME Extensions',
          'https://extensions.gnome.org/accounts/profile/TimurKiyivinski'),)

# Social widget
SOCIAL = (('GitHub',
           'https://github.com/kiyui'),
          ('LinkedIn',
           'https://www.linkedin.com/in/timothy-kiyui-a47503180/'),)
