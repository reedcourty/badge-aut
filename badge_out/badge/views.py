#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth.models import User

from badge.models import Felhasznalo, Badge, Tipus, Feladat, Cel

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

def is_oktato(request):
    user = User.objects.get(username=request.user)
    felhasznalo = Felhasznalo.objects.get(user = user)
    
    if (felhasznalo.szerep == 'O'):
        return True
    else:
        return False

def stat_oktato_badge(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
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

@login_required    
def manage_feladatok_new(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        
        tipusok = Tipus.objects.all()
        
        content = {
            'operation': 'new',
            'tipusok' : tipusok,
            'error' : None,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            # Form ellenőrzése:
            
            if (request.POST['nev'] == "") or (request.POST['leiras'] == "") or (request.POST['tipus'] == ""):
                content['error'] = u"Nem adtál meg minden adatot! :("
            else:
                feladat = Feladat()
                feladat.nev = request.POST['nev']
                feladat.leiras = request.POST['leiras']
                feladat.tipus = Tipus.objects.get(pk=request.POST['tipus'])
                
                feladat.save()
                return HttpResponseRedirect('/manage/feladatok/')
            
        return render_to_response('manage-feladat.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def manage_feladatok_edit(request, id):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        feladat = Feladat.objects.get(pk=id)
        
        tipusok = Tipus.objects.all()
        
        content = {
            'operation': 'edit',
            'error' : None,
            'feladat' : feladat,
            'tipusok' : tipusok,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            if (request.POST['nev'] == "") or (request.POST['leiras'] == "") or (request.POST['tipus'] == ""):
                content['error'] = u"Nem adtál meg minden adatot! :("
            else:
                feladat.nev = request.POST['nev']
                feladat.leiras = request.POST['leiras']
                feladat.tipus = Tipus.objects.get(pk=request.POST['tipus'])
                
                feladat.save()
                return HttpResponseRedirect('/manage/feladatok/')
        
        return render_to_response('manage-feladat.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def manage_feladatok_delete(request, id):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        feladat = Feladat.objects.get(pk=id)
        
        content = {
            'feladat' : feladat,
            'operation': 'delete',
            'error' : None,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            if (request.POST['button'] == "Nem"):
                return HttpResponseRedirect('/manage/feladatok/')
            
            if (request.POST['button'] == "Igen"):                
                feladat.delete()
                return HttpResponseRedirect('/manage/feladatok/')            
        
        return render_to_response('manage-feladat.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def manage_celok_list(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
    
        celok = Cel.objects.all()
        
        content = {
            'celok' : celok,
            'operation': 'list',
            'request': request, 
        }
        
        return render_to_response('manage-cel.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def manage_celok_new(request):
    
    if (not is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        
        feladatok = Feladat.objects.all()
        badgeek = Badge.objects.all()
        
        content = {
            'operation': 'new',
            'badgeek' : badgeek,
            'feladatok' : feladatok,
            'cel_form' : None,
            'error' : None,
            'request': request, 
        }
        
        if (request.method == 'POST'):
            
            try:
                rovid_leiras = request.POST['rovid_leiras']
                leiras = request.POST['leiras']
                feladatok_checkbox = request.POST.getlist('feladatok')
                badge_select = request.POST['badge']
            except MultiValueDictKeyError:
                feladatok_checkbox = None
            
            content['POST'] = request.POST
            
            content['cel_form'] = {
                'rovid_leiras' : rovid_leiras,
                'leiras' : leiras,
                'feladatok' : feladatok_checkbox, 
            }
            
            if (rovid_leiras == "") or (leiras == "") or (badge_select == ""):
                content['error'] = u"Nem adtál meg minden adatot! :("
            else:
                badge = Badge.objects.get(pk=badge_select)
                print(badge)
                cel = Cel.objects.create(rovid_leiras=rovid_leiras, leiras=leiras, badge=badge)
                                
                if (feladatok_checkbox != None):
                    for feladat_id in feladatok_checkbox:
                        feladat = Feladat.objects.get(pk=feladat_id)
                        cel.feladatok.add(feladat)
                
                cel.save()
                return HttpResponseRedirect('/manage/celok/')
            
        return render_to_response('manage-cel.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))


def set_badge(username):
    
    celok = Cel.objects.all()
    
    user = User.objects.get(username=username)
    felhasznalo = Felhasznalo.objects.get(user = user)
    
    felhasznalo.badge.clear()
    
    for cel in celok:
        minden_megvan = True
        cel_feladatai = cel.feladatok.all()
        for feladat in cel_feladatai:
            if felhasznalo.teljesitett.filter(pk=feladat.pk):
                pass
            else:
                minden_megvan = False
                break
        if minden_megvan:
            felhasznalo.badge.add(cel.badge)
            felhasznalo.save()
        else:
            felhasznalo.badge.remove(cel.badge)
            felhasznalo.save()

@login_required    
def badge_list_all(request):
    
    if (is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        
        set_badge(request.user)
        
        badge_all = Badge.objects.all()
    
        content = {
            'badge_all' : badge_all,
            'operation': 'list_all',
            'request': request, 
        }
        
        return render_to_response('hallgato-badge.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))

@login_required    
def badge_list_user(request):
    
    if (is_oktato(request)):
        return HttpResponseRedirect('/start')
    else:
        
        set_badge(request.user)
        
        badge_all = Badge.objects.all()
        
        user = User.objects.get(username=request.user)
        felhasznalo = Felhasznalo.objects.get(user = user)
        
        badge_user = felhasznalo.badge.all()
    
        content = {
            'badge_all' : badge_all,
            'badge_user' : badge_user,
            'operation': 'list_user',
            'request': request, 
        }
        
        return render_to_response('hallgato-badge.html',
                                  {'content' : content},
                                  context_instance = RequestContext(request))
