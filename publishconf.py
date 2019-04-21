#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Timur Kiyui'
SITENAME = 'dont reinvent велосипед'
SITEURL = 'https://dontreinventbicycle.com'

# Site options
TIMEZONE = 'Asia/Kuching'
DEFAULT_LANG = 'en'

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
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True

# Disable feed generation while developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

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
