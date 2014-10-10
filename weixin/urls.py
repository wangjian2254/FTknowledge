#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('weixin',
                       # Examples:
                       url(r'^weixinapi', 'view.handleRequest'),
                       url(r'^subjecthtml', 'views_qiang.subjecthtml'),
                       url(r'^get_new_weixinmessage', 'views_qiang.get_new_weixinmessage'),


)
