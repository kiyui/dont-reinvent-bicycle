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
PLUGINS = ["sitemap", "gzip_cache", "minchin.pelican.plugins.nojekyll"]

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
MARKDOWN = {
    'extensions': [
        'pymdownx.tilde',
        'pymdownx.inlinehilite',
    ],
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Static content
ARTICLE_EXCLUDES = ['extra', 'images', 'demos']
STATIC_PATHS = [
    'extra',
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
    },
    'extra/brave-rewards-verification.txt': {
        'path': '.well-known/brave-rewards-verification.txt'
    },
    'extra/robots.txt': {
        'path': 'robots.txt'
    },
    'extra/favicon.ico': {
        'path': 'favicon.ico'
    },
    'extra/favicon-16x16.png': {
        'path': 'favicon-16x16.png'
    },
    'extra/favicon-32x32.png': {
        'path': 'favicon-32x32.png'
    },
    'extra/apple-touch-icon.png': {
        'path': 'apple-touch-icon.png'
    },
    'extra/site.webmanifest': {
        'path': 'site.webmanifest'
    },
    'extra/android-chrome-192x192.png': {
        'path': 'android-chrome-192x192.png'
    },
    'extra/android-chrome-384x384.png': {
        'path': 'android-chrome-384x384.png'
    },
    'extra/browserconfig.xml': {
        'path': 'browserconfig.xml'
    },
    'extra/safari-pinned-tab.svg': {
        'path': 'safari-pinned-tab.svg'
    },
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
          'https://represent.io/kiyui'),
         ('GNOME Extensions',
          'https://extensions.gnome.org/accounts/profile/TimurKiyivinski'),)

# Social widget
SOCIAL = (('Codeberg',
           'https://codeberg.org/kiyui',
           None),
          ('GitHub',
           'https://github.com/kiyui',
           None),
          ('Mastodon',
           'https://deadinsi.de/@dafne',
           'me'),
          ('Birbsite',
           'https://twitter.com/dafnelately',
           'None'),
          ('LinkedIn',
           'https://www.linkedin.com/in/dafnelately/',
           None),)
