#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'

from django.conf.urls import patterns, include, url


urlpatterns = patterns('knowledge',
    # Examples:
    url(r'^menu.xml$', 'views.menu'),
    url(r'^allmanager$', 'views.allmanager'),
    url(r'^currentUser', 'views.currentUser'),
    url(r'^getHyList', 'views.getHyList'),
    url(r'^regUser', 'views.regUser'),
    url(r'^login', 'views.login'),
    url(r'^logout', 'views.logout'),
    url(r'^getTaxKind', 'views.getTaxKind'),
    url(r'^saveTaxKind', 'views.saveTaxKind'),
    url(r'^saveTaxTicket', 'views.saveTaxTicket'),
    url(r'^delTaxTicket', 'views.delTaxTicket'),
    url(r'^getBB$', 'views.getBB'),
    url(r'^saveBB$', 'views.saveBB'),
    url(r'^delBB$', 'views.delBB'),
    url(r'^saveBBField$', 'views.saveBBField'),
    url(r'^delBBField$', 'views.delBBField'),
    # url(r'^FTknowledge/', include('FTknowledge.foo.urls')),


)
