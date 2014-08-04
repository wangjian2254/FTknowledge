#coding=utf-8
#author:u'王健'
#Date: 14-5-21
#Time: 上午8:00
from django import forms
from taxcreate.models import Paper, PaperResult, Subject, Option, Guan
from util.CustomForm import CustomModelForm

__author__ = u'王健'



class PaperForm(CustomModelForm):
    right_ztdm = forms.CharField(required=False)
    flag = forms.CharField(required=False)
    is_pub = forms.BooleanField()
    guan = forms.ModelChoiceField(required=False,queryset=Guan.objects.all())
    class Meta:
        model = Paper
        fields = ('title','flag', 'content','is_pub','right_ztdm','guan','time')


class GuanForm(CustomModelForm):
    class Meta:
        model = Guan
        fields = ('flag', 'name','point')



class PaperResultForm(CustomModelForm):
    class Meta:
        model = PaperResult
        fields = ('paper', 'user', 'editDate', 'result')


class SubjectForm(CustomModelForm):
    ruleitem = forms.IntegerField(required=False)
    flag = forms.CharField(required=False)
    class Meta:
        model = Subject
        fields = ('title','flag','bz', 'type','rule')


class OptionForm(CustomModelForm):
    class Meta:
        model = Option
        fields = ('subject', 'content', 'is_right')

