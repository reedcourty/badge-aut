#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

'''
Created on 2012.11.23.

@author: reedcourty
'''

from badge.models import Felhasznalo, Feladat, Tipus 
from django.contrib import admin

admin.site.register(Felhasznalo, Feladat, Tipus)
