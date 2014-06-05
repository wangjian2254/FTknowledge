#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28

__author__ = u'王健'
from django.db import models

# Create your models here.

class TaxTemplate(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'票据模板', help_text=u'票据模板名称')
    img = models.ImageField(upload_to='tax/',verbose_name=u'票据模板位置')


    def __unicode__(self):
        return u'%s'%(self.name,)

class TaxRule(models.Model):
    taxtemplate = models.ForeignKey(TaxTemplate,verbose_name=u'票据模板')
    name = models.CharField(max_length=50,verbose_name=u'生成票据条件')

    def __unicode__(self):
        return u'%s-%s'%(self.name,self.taxtemplate.name)

class RuleItem(models.Model):
    rule = models.ForeignKey(TaxRule,verbose_name=u'票据条件')
    index = models.IntegerField(verbose_name=u'索引')
    x = models.IntegerField(verbose_name=u'模板位置x')
    y = models.IntegerField(verbose_name=u'模板位置y')
    size = models.IntegerField(verbose_name=u'字体大小')
    color = models.IntegerField(verbose_name=u'字体颜色')
    family = models.IntegerField(verbose_name=u'字体类型')
    word = models.CharField(max_length=200,verbose_name=u'文字')
