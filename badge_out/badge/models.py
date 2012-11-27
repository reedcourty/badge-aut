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
    nev = models.CharField(max_length=50, verbose_name=u"Név")
    
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
    kep = models.ImageField(upload_to="badge_images", verbose_name=u"Kép")
    letrehozta = models.ForeignKey('Felhasznalo', verbose_name=u'A badge-et létrehozta', related_name='letrehozta')
    
    def kep_link(self):
        return '<img src="/media/{0}"/>'.format(self.kep)
    kep_link.allow_tags = True
    
    def __unicode__(self):
        return self.nev
    
    class Meta:
        verbose_name = u'Badge'
        verbose_name_plural = u'Badge-ek'

class Cel(models.Model):
    rovid_leiras = models.CharField(max_length=50, verbose_name=u'Rövid leírás')
    leiras = models.CharField(max_length=200, verbose_name=u'Részletes leírás')
    feladatok = models.ManyToManyField(Feladat, verbose_name=u"Feladatok")
    badge = models.ForeignKey(Badge, verbose_name=u"Badge")
    
    def __unicode__(self):
        return self.rovid_leiras
    
    class Meta:
        verbose_name = u'Cél'
        verbose_name_plural = u'Célok'

class Felhasznalo(models.Model):
    user = models.OneToOneField(User, verbose_name=u"Felhasználói név")
    nev = models.CharField(max_length=200, verbose_name=u"Név")
    neptun = models.CharField(max_length=6, verbose_name=u"Neptun kód")
    szerep = models.CharField(max_length=1, choices=SZEREPEK, verbose_name=u"Szerep")
    teljesitett = models.ManyToManyField(Feladat, blank=True, null=True, verbose_name=u"Teljesített feladatok")
    badge = models.ManyToManyField(Badge, blank=True, null=True, verbose_name=u"Badge")
    
    def __unicode__(self):
        return u"{0} ({1})".format(self.nev, self.neptun)
    
    class Meta:
        verbose_name = u'Felhasználó'
        verbose_name_plural = u'Felhasználók'
        
class BadgeTabla(models.Model):
    felhasznalo = models.ForeignKey(Felhasznalo, verbose_name=u"Felhasználó")
    badge = models.ForeignKey(Badge, verbose_name=u"Badge")
    megszerzes_ideje = models.DateTimeField(verbose_name=u"Megszerzés ideje")
    
    class Meta:
        verbose_name = u'Badge tábla'
        verbose_name_plural = u'Badge táblák'