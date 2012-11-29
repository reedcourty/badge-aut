from django.conf.urls import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'badge_out.views.home', name='home'),
    # url(r'^badge_out/', include('badge_out.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^$', 'badge.views.index'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'badge.views.kilepes'),
    url(r'^start/$', 'badge.views.start'),
    
    url(r'^stat/oktato-badge/$', 'badge.views.stat_oktato_badge'),
    
    url(r'^manage/tipusok/(?P<id>\d+)/edit$', 'badge.views.manage_tipusok_edit'),
    url(r'^manage/tipusok/(?P<id>\d+)/delete$', 'badge.views.manage_tipusok_delete'),
    url(r'^manage/tipusok/new$', 'badge.views.manage_tipusok_new'),
    url(r'^manage/tipusok/$', 'badge.views.manage_tipusok_list'),
    
    url(r'^manage/feladatok/(?P<id>\d+)/edit$', 'badge.views.manage_feladatok_edit'),
    url(r'^manage/feladatok/(?P<id>\d+)/delete$', 'badge.views.manage_feladatok_delete'),
    url(r'^manage/feladatok/new$', 'badge.views.manage_feladatok_new'),
    url(r'^manage/feladatok/$', 'badge.views.manage_feladatok_list'),
    
    url(r'^manage/celok/(?P<id>\d+)/delete$', 'badge.views.manage_celok_delete'),
    url(r'^manage/celok/new$', 'badge.views.manage_celok_new'),
    url(r'^manage/celok/$', 'badge.views.manage_celok_list'),
    
    url(r'^manage/badge/(?P<id>\d+)/edit$', 'badge.views.manage_badge_edit'),
    url(r'^manage/badge/(?P<id>\d+)/delete$', 'badge.views.manage_badge_delete'),
    url(r'^manage/badge/new$', 'badge.views.manage_badge_new'),
    url(r'^manage/badge/$', 'badge.views.manage_badge_list'),
    
    url(r'^badge/all$', 'badge.views.badge_list_all'),
    url(r'^badge/own$', 'badge.views.badge_list_user'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
