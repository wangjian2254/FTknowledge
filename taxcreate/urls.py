#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'

from django.conf.urls import patterns, url


urlpatterns = patterns('taxcreate',
                       # Examples:
                       url(r'^getTuZhangList', 'views.getTuZhangList'),
                       url(r'^deleteTuZhang', 'views.deleteTuZhang'),
                       url(r'^taxTuZhangUploaded', 'views.taxTuZhangUploaded'),
                       url(r'^saveTuZhang', 'views.saveTuZhang'),

                       url(r'^showTaxImage', 'views.showTaxImage'),
                       url(r'^saveRuleItem', 'views.saveRuleItem'),
                       url(r'^copyRuleItem', 'views.copyRuleItem'),
                       url(r'^taxTemplateUploaded', 'views.taxTemplateUploaded'),
                       url(r'^deleteTemplate', 'views.deleteTemplate'),
                       url(r'^getTemplateList', 'views.getTemplateList'),
                       url(r'^getRuleByTemplateList', 'views.getRuleByTemplateList'),
                       url(r'^getRuleItemByRuleList', 'views.getRuleItemByRuleList'),
                       url(r'^delRuleItemByids', 'views.delRuleItemByids'),
                       url(r'^saveRule', 'views.saveRule'),
                       url(r'^deleteRule', 'views.deleteRule'),
                       url(r'^saveTemplate', 'views.saveTemplate'),

                       url(r'^updateSubject', 'view_subject.updateSubject'),
                       url(r'^getSubjectByKind', 'view_subject.getSubjectByKind'),
                       url(r'^getSubjectAll', 'view_subject.getSubjectAll'),
                       url(r'^getSubjectById', 'view_subject.getSubjectById'),
                       url(r'^getOptionBySubject', 'view_subject.getOptionBySubject'),
                       url(r'^delSubject', 'view_subject.delSubject'),
                       url(r'^delOption', 'view_subject.delOption'),

                       url(r'^getPZ', 'view_subject.getPZ'),



                       url(r'^updatePaper', 'view_shijuan.updatePaper'),
                       url(r'^getAllPaperUnGuan', 'view_shijuan.getAllPaperUnGuan'),
                       url(r'^getSubjectByPaper', 'view_shijuan.getSubjectByPaper'),
                       url(r'^getPaperByKind', 'view_shijuan.getPaperByKind'),

                       url(r'^getPaper$', 'view_shijuan.getPaper'),
                       url(r'^doPaperSubject', 'view_shijuan.doPaperSubject'),
                       url(r'^getAllPaper', 'view_shijuan.getAllPaper'),
                       url(r'^delPaper', 'view_shijuan.delPaper'),

                       url(r'^getAllGuan', 'view_guan.getAllGuan'),
                       url(r'^updateGuan', 'view_guan.updateGuan'),
                       url(r'^getPaperByGuan', 'view_guan.getPaperByGuan'),
                       url(r'^doGuanPaper', 'view_guan.doGuanPaper'),
                       url(r'^delGuan', 'view_guan.delGuan'),
                       url(r'^getGuan$', 'view_guan.getGuan'),
                       url(r'^getGuanData', 'view_guan.getGuanData'),

                       url(r'^getPaperListData', 'view_guan.getPaperListData'),
                       url(r'^getGuanById', 'view_guan.getGuanById'),

                       #科目管理
                       url(r'^updateKjkmKind', 'view_kjkm.updateKJKMKind'),
                       url(r'^updateKJKM', 'view_kjkm.updateKJKM'),
                       url(r'^delKJKM', 'view_kjkm.delKJKM'),
                       url(r'^delKjkmKind', 'view_kjkm.delKjkmKind'),
                       url(r'^getAllKind', 'view_kjkm.getAllKind'),
                       url(r'^getAllKMByKind', 'view_kjkm.getAllKMByKind'),
                       url(r'^getAllKMLabelByKind', 'view_kjkm.getAllKMLabelByKind'),
                       url(r'^exportKJKM', 'view_kjkm.exportKJKM'),

)
