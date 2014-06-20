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
                       url(r'^delRuleItemByids', 'views.delRuleItemByids'),
                       url(r'^saveRule', 'views.saveRule'),
                       url(r'^saveTemplate', 'views.saveTemplate'),

                       url(r'^updateSubject', 'view_subject.updateSubject'),
                       url(r'^getSubjectByKind', 'view_subject.getSubjectByKind'),
                       url(r'^getSubjectAll', 'view_subject.getSubjectAll'),
                       url(r'^getSubjectById', 'view_subject.getSubjectById'),
                       url(r'^getOptionBySubject', 'view_subject.getOptionBySubject'),
                       url(r'^delSubject', 'view_subject.delSubject'),
                       url(r'^delOption', 'view_subject.delOption'),

                       url(r'^updatePaper', 'view_shijuan.updatePaper'),
                       url(r'^getSubjectByPaper', 'view_shijuan.getSubjectByPaper'),
                       url(r'^getPaper', 'view_shijuan.getPaper'),
                       url(r'^getMyPaper', 'view_shijuan.getMyPaper'),
                       url(r'^answerPaper', 'view_shijuan.answerPaper'),
                       url(r'^doPaperSubject', 'view_shijuan.doPaperSubject'),
                       url(r'^getAllPaper', 'view_shijuan.getAllPaper'),
                       url(r'^delPaper', 'view_shijuan.delPaper'),
                       url(r'^copyPaper', 'view_shijuan.copyPaper'),


)
