#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

'''
Created on 2012.11.23.

@author: reedcourty
'''

from badge.models import Felhasznalo, Feladat, Tipus, Badge, Cel, BadgeTabla
from django.contrib import admin

class BadgeAdmin(admin.ModelAdmin):     
    list_display = ('nev', 'leiras', 'letrehozta', 'kep_link')
    
class FelhasznaloAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'szerep')
    
class BadgeTablaAdmin(admin.ModelAdmin):
    list_display = ('felhasznalo', 'badge', 'megszerzes_ideje')

admin.site.register(Felhasznalo, FelhasznaloAdmin)
admin.site.register(Feladat)
admin.site.register(Tipus)
admin.site.register(Badge, BadgeAdmin)
admin.site.register(Cel)
admin.site.register(BadgeTabla, BadgeTablaAdmin)

