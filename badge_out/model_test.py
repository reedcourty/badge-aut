#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

'''
Created on 2012.11.24.

@author: reedcourty
'''

import os

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "badge_out.settings"

from badge.models import Felhasznalo, Feladat, Tipus, Badge, Cel

u = Felhasznalo.objects.get(pk=1)
t = u.teljesitett.all()
celok = Cel.objects.all()



for u in Felhasznalo.objects.all():
    print(u"\n\n------------------------------------------------------------")
    print(u"A {0} nevű hallgató vizsgálata:".format(u))
    for cel in celok:
        minden_megvan = True
        print(u"__{0}__ - A kapcsolódó badge: {1}".format(cel, cel.badge))
        cel_feladatai = cel.feladatok.all()
        print(u"    A következő feladatokból áll:")
        for feladat in cel_feladatai:
            print(u"     - {0}".format(feladat)),
            if u.teljesitett.filter(pk=feladat.pk):
                print(u" -- a hallgató teljesítette a feladatot.")
            else:
                minden_megvan = False
                print(u" -- a hallgató NEM teljesítette a feladatot.")
                break
        print(u"\n")
        if minden_megvan:
            print(u"\n* A hallgató jogosult a {0} nevű badge-re. {1}".format(cel.badge, cel.badge.kep))
            u.badge.add(cel.badge)
            u.save()
        else:
            u.badge.remove(cel.badge)
            u.save()