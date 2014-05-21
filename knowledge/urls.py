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
    url(r'^saveUser', 'views.saveUser'),
    # url(r'^getTaxKind', 'views.getTaxKind'),
    # url(r'^saveTaxKind', 'views.saveTaxKind'),
    # url(r'^saveTaxTicket', 'views.saveTaxTicket'),
    # url(r'^delTaxTicket', 'views.delTaxTicket'),
    # url(r'^getBB$', 'views.getBB'),
    # url(r'^saveBB$', 'views.saveBB'),
    # url(r'^delBB$', 'views.delBB'),
    # url(r'^saveBBField$', 'views.saveBBField'),
    # url(r'^delBBField$', 'views.delBBField'),
    url(r'^initData$', 'importExcel.initData'),
    # url(r'^getKJKM$', 'views.getKJKM'),
    # url(r'^getKJKMbyTicket$', 'views.getKJKMbyTicket'),
    # url(r'^saveKJKM$', 'views.saveKJKM'),
    # url(r'^saveKJKMByTicket$', 'views.saveKJKMByTicket'),
    # url(r'^getBBFieldValuebyTicketKjkm$', 'views.getBBFieldValuebyTicketKjkm'),
    # url(r'^saveBBFieldValuebyTicketKjkm$', 'views.saveBBFieldValuebyTicketKjkm'),
    # url(r'^queryKnowledge$', 'views.queryKnowledge'),
    url(r'^initKJKM$', 'importData.initKJKM'),
    url(r'^getKJZDByKM', 'newviews.getKJZDByKM'),
    url(r'^getKMByBusiness', 'newviews.getKMByBusiness'),
    url(r'^getBusinessByTicket', 'newviews.getBusinessByTicket'),
    url(r'^getTicketByRule', 'newviews.getTicketByRule'),
    url(r'^getRule', 'newviews.getRule'),
    url(r'^saveRule', 'newviews.saveRule'),
    url(r'^delRule', 'newviews.delRule'),
    url(r'^getAllTicket', 'newviews.getAllTicket'),
    url(r'^saveTicket', 'newviews.saveTicket'),
    url(r'^delTicket', 'newviews.delTicket'),
    url(r'^getPZbyBusiness$', 'newviews.getPZbyBusiness'),
    url(r'^getAllBusiness', 'newviews.getAllBusiness'),
    url(r'^saveBusiness', 'newviews.saveBusiness'),
    url(r'^delBusiness', 'newviews.delBusiness'),
    url(r'^getAllKM', 'newviews.getAllKM'),
    url(r'^saveKM', 'newviews.saveKM'),
    url(r'^delKM', 'newviews.delKM'),
    url(r'^getPZ$', 'newviews.getPZ'),
    url(r'^savePZ$', 'newviews.savePZ'),
    url(r'^saveRelation', 'newviews.saveRelation'),
    url(r'^delRelation', 'newviews.delRelation'),
    url(r'^getBusinessByUserRule$', 'newviews.getBusinessByUserRule'),
    url(r'^getTicketByUserRule$', 'newviews.getTicketByUserRule'),
    url(r'^imgUploaded', 'imgviews.imgUploaded'),
    url(r'^delImg', 'imgviews.delImg'),


    url(r'^tongji', 'tongji_view.tongji'),

    # url(r'^FTknowledge/', include('FTknowledge.foo.urls')),


)
