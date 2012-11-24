#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from badge.models import Felhasznalo, Badge

def kilepes(request):
    logout(request)
    return HttpResponseRedirect('/')

def start(request):
    return render_to_response('start.html',
                              {},
                              context_instance = RequestContext(request))

def index(request):
    return render_to_response('index.html',
                              {},
                              context_instance = RequestContext(request))
    
def stat_oktato_badge(request):
    
    oktatok = Felhasznalo.objects.filter(szerep='O')
    badgeek = Badge.objects.all()
    
    stat = u'['
    
    for oktato in oktatok:
        count_badge = 0
        for badge in badgeek:
            if (badge.letrehozta == oktato):
                count_badge = count_badge + 1
        o_stat = u"['{0}',{1}],".format(oktato.nev, count_badge)
        stat = stat + o_stat
    stat = stat[0:len(stat)-1] + ']'
    
    return render_to_response('stat-oktato-badge.html',
                              {'stat' : stat},
                              context_instance = RequestContext(request))