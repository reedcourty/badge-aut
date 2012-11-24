#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# using UTF-8 charset

from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

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