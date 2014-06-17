#coding=utf-8
#author:u'王健'
#Date: 14-5-21
#Time: 上午8:00
from taxcreate.models import Paper, PaperResult, Subject, Option
from util.CustomForm import CustomModelForm

__author__ = u'王健'



class PaperForm(CustomModelForm):
    class Meta:
        model = Paper
        fields = ('title', 'content','subjects','is_pub','right_ztdm')


class PaperResultForm(CustomModelForm):
    class Meta:
        model = PaperResult
        fields = ('paper', 'user', 'editDate', 'result')


class SubjectForm(CustomModelForm):
    class Meta:
        model = Subject
        fields = ('title','bz', 'type')


class OptionForm(CustomModelForm):
    class Meta:
        model = Option
        fields = ('subject', 'content', 'is_right')

