#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Dafne Kiyui'
DEADNAME = 'Timur Kiyui'
SITENAME = 'dont reinvent велосипед'
SITEURL = 'https://dontreinventbicycle.com'
SITE_DESCRIPTION = 'dont reinvent bicycle - programming practices and musings'
SITE_KEYWORDS = ['programming', 'practice', 'standards', 'hacking', 'musing']

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
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True

# Static content
ARTICLE_EXCLUDES = ['extra', 'images', 'demos']
STATIC_PATHS = [
    'extra/CNAME',
    'extra/BingSiteAuth.xml',
    'extra/google84482ab458ba2d3d.html'
]
EXTRA_PATH_METADATA = {
    'extra/CNAME': {
        'path': 'CNAME'
    },
    'extra/BingSiteAuth.xml': {
        'path': 'BingSiteAuth.xml'
    },
    'extra/google84482ab458ba2d3d.html': {
        'path': 'google84482ab458ba2d3d.html'
    }
}

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
LINKS = (('Resume',
          'https://registry.jsonresume.org/kiyui'),
         ('GNOME Extensions',
          'https://extensions.gnome.org/accounts/profile/TimurKiyivinski'),)

# Social widget
SOCIAL = (('GitHub',
           'https://github.com/kiyui'),
          ('Mastodon',
           'https://queer.chat/@dafne'),
          ('LinkedIn',
           'https://www.linkedin.com/in/dafnelately/'),)
