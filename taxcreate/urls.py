#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('taxcreate',
                       # Examples:
                       url(r'^showTaxImage', 'views.showTaxImage'),
                       url(r'^saveRuleItem', 'views.saveRuleItem'),
                       url(r'^taxTemplateUploaded', 'views.taxTemplateUploaded'),
                       url(r'^getTemplateList', 'views.getTemplateList'),
                       url(r'^getRuleByTemplateList', 'views.getRuleByTemplateList'),
                       url(r'^getRuleItemByRuleList', 'views.getRuleItemByRuleList'),
                       url(r'^saveRule', 'views.saveRule'),
                       url(r'^saveTemplate', 'views.saveTemplate'),

                       (r'^updateSubject', 'view_subject.updateSubject'),
                       (r'^getSubjectByKind', 'view_subject.getSubjectByKind'),
                       (r'^getSubjectAll', 'view_subject.getSubjectAll'),
                       (r'^getSubjectById', 'view_subject.getSubjectById'),
                       (r'^delSubject', 'view_subject.delSubject'),
                       (r'^delOption', 'view_subject.delOption'),

                       (r'^updatePaper', 'view_shijuan.updatePaper'),
                       (r'^getPaper', 'view_shijuan.getPaper'),
                       (r'^getMyPaper', 'view_shijuan.getMyPaper'),
                       (r'^answerPaper', 'view_shijuan.answerPaper'),
                       (r'^doPaperSubject', 'view_shijuan.doPaperSubject'),
                       (r'^getAllPaper', 'view_shijuan.getAllPaper'),
                       (r'^delPaper', 'view_shijuan.delPaper'),
                       (r'^copyPaper', 'view_shijuan.copyPaper'),


)
