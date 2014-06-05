#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'


from django.conf.urls import patterns, url


urlpatterns = patterns('taxcreate',
    # Examples:

    url(r'^taxTemplateUploaded', 'views.taxTemplateUploaded'),
    url(r'^getTemplateList', 'views.getTemplateList'),
    url(r'^getRuleByTemplateList', 'views.getRuleByTemplateList'),
    url(r'^getRuleItemByRuleList', 'views.getRuleItemByRuleList'),
    url(r'^saveRule', 'views.saveRule'),
    url(r'^saveTemplate', 'views.saveTemplate'),




)
