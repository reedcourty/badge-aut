#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

'''
Created on 2012.11.23.

@author: reedcourty
'''

from badge.models import Felhasznalo, Feladat, Tipus, Badge, Cel
from django.contrib import admin

class BadgeAdmin(admin.ModelAdmin):     
    list_display = ('nev', 'leiras', 'kep_link')

admin.site.register(Felhasznalo)
admin.site.register(Feladat)
admin.site.register(Tipus)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Cel)
