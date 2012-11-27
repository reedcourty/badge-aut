#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from badge.models import Felhasznalo, Badge, Tipus, Feladat

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


def is_oktato(request):
    user = User.objects.get(username=request.user)
    felhasznalo = Felhasznalo.objects.get(user = user)
    
    if (felhasznalo.szerep == 'O'):
        return True
    else:
        return False

@login_required    
def manage_tipusok_list(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
    
        tipusok = Tipus.objects.all()
        
        content = {
            'tipusok' : tipusok,
            'operation': 'list',
            'request': request, 
        }
        
        return render_to_response('manage-tipus.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))
        
@login_required    
def manage_tipusok_new(request):
    
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        
        content = {
            'operation': 'new',
            'error' : None,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            tipus = Tipus()
            tipus.nev = request.POST['nev']
            tipus.save()
            return HttpResponseRedirect('/manage/tipusok/')
        
        return render_to_response('manage-tipus.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))
        
@login_required    
def manage_tipusok_edit(request, id):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        tipus = Tipus.objects.get(pk=id)
        content = {
            'operation': 'edit',
            'error' : None,
            'tipus' : tipus,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            tipus.nev = request.POST['nev']
            tipus.save()
            return HttpResponseRedirect('/manage/tipusok/')
        
        return render_to_response('manage-tipus.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))
    
@login_required    
def manage_tipusok_delete(request, id):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        tipus = Tipus.objects.get(pk=id)
        
        content = {
            'tipus' : tipus,
            'operation': 'delete',
            'error' : None,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            if (request.POST['button'] == "Nem"):
                return HttpResponseRedirect('/manage/tipusok/')
            
            if (request.POST['button'] == "Igen"):                
                TOROLHETO = True
                
                for feladat in Feladat.objects.all():
                    if (feladat.tipus == tipus):
                        TOROLHETO = False
                        content['error'] = u"Feladathoz rendelt típus. Nem törölhető." 
                
                if TOROLHETO:
                    tipus.delete()
                    return HttpResponseRedirect('/manage/tipusok/')            
        
        return render_to_response('manage-tipus.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def manage_feladatok_list(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
    
        feladatok = Feladat.objects.all()
        
        content = {
            'feladatok' : feladatok,
            'operation': 'list',
            'request': request, 
        }
        
        return render_to_response('manage-feladat.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))
