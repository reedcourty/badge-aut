#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.db import models
from django.contrib.auth.models import User

SZEREPEK = (
    (u'H', u'Hallgató'),
    (u'O', u'Oktató'),
)

class Tipus(models.Model):
    nev = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.nev
    
    class Meta:
        verbose_name = u'Típus'
        verbose_name_plural = u'Típusok'

class Feladat(models.Model):
    nev = models.CharField(max_length=100, verbose_name=u'Név')
    leiras = models.CharField(max_length=200, verbose_name=u'Leírás')
    tipus = models.ForeignKey(Tipus, verbose_name=u'Típus')
    
    def __unicode__(self):
        return self.nev
    
    class Meta:
        verbose_name = u'Feladat'
        verbose_name_plural = u'Feladatok'

class Badge(models.Model):
    nev = models.CharField(max_length=50, verbose_name=u'Név')
    leiras = models.CharField(max_length=200, verbose_name=u'Leírás')
    kep = models.ImageField(upload_to="badge_images")
    letrehozta = models.ForeignKey('Felhasznalo', verbose_name=u'Megszerzésére lehetőséget biztosított a badge létrehozásával', related_name='letrehozta')
    
    def kep_link(self):
        return '<img src="/media/{0}"/>'.format(self.kep)
    kep_link.allow_tags = True
    
    def __unicode__(self):
        return self.nev

class Cel(models.Model):
    rovid_leiras = models.CharField(max_length=50, verbose_name=u'Rövid leírás')
    leiras = models.CharField(max_length=200, verbose_name=u'Részletes leírás')
    feladatok = models.ManyToManyField(Feladat)
    badge = models.ForeignKey(Badge)
    
    def __unicode__(self):
        return self.rovid_leiras

class Felhasznalo(models.Model):
    user = models.OneToOneField(User)
    nev = models.CharField(max_length=200)
    neptun = models.CharField(max_length=6)
    szerep = models.CharField(max_length=1, choices=SZEREPEK)
    teljesitett = models.ManyToManyField(Feladat, blank=True, null=True)
    badge = models.ManyToManyField(Badge, blank=True, null=True)
    
    def __unicode__(self):
        return u"{0} ({1})".format(self.nev, self.neptun)
    
    class Meta:
        verbose_name = u'Felhasználó'
        verbose_name_plural = u'Felhasználók'
