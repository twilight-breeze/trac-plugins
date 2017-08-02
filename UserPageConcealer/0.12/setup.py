#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from setuptools import setup

setup(
    name = 'TracUserPageConcealerPlugin',
    description = "conceal userpage from timeline.",
    keywords = "trac userpage conceal timeline",
    version = '0.12.1.0',
    url = "",
		license = "BSD",
    author = "jjyun",
    author_email = "hyper.gauntlet@gmail.com",
    packages = ['UserPageConcealer'],
    entry_points = { 
        'trac.plugins': [
            'UserPageConcealer.UserPageConcealer = UserPageConcealer.UserPageConcealer',
        ]
    }
)
