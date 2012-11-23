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

class Feladat(models.Model):
    nev = models.CharField(max_length=50)
    leiras = models.CharField(max_length=200)
    tipus = models.ForeignKey(Tipus)

class Felhasznalo(models.Model):
    user = models.OneToOneField(User)
    nev = models.CharField(max_length=200)
    neptun = models.CharField(max_length=6)
    szerep = models.CharField(max_length=1, choices=SZEREPEK)
    teljesitett = models.ManyToManyField(Feladat)


    