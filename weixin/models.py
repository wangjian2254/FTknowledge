# coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
import datetime

__author__ = u'王健'
from django.db import models

# Create your models here.

class WeiXinUser(models.Model):
    weixinid = models.CharField(max_length=50, unique=True, db_index=True, verbose_name=u'微信openid')
    nickname = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'昵称')
    sex = models.IntegerField(null=True, blank=True, verbose_name=u'性别')
    headimgurl = models.URLField(null=True, blank=True, verbose_name=u'头像地址')
    current_subject_code = models.IntegerField(null=True, blank=True, verbose_name=u'活动标记')
    is_active = models.BooleanField(default=True, verbose_name=u'是否关注')
    unionid = models.CharField(max_length=50,null=True, blank=True, unique=True, db_index=True, verbose_name=u'用户标示')
    def __unicode__(self):
        return u'%s' % (self.nickname,)

class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name=u'活动名称')
    create_time = models.DateTimeField(auto_created=True, auto_now=True, verbose_name=u'活动开始时间')
    code = models.IntegerField(unique=True, db_index=True, verbose_name=u'活动标记')
    is_check = models.BooleanField(default=False, verbose_name=u'客户发言是否经过审核')
    status = models.BooleanField(default=True, verbose_name=u'活动状态，是否结束')
    weixinusers = models.ManyToManyField(WeiXinUser, verbose_name=u'参与微信用户')


class WeiXinMessage(models.Model):
    weixinuser = models.ForeignKey(WeiXinUser, verbose_name=u'作者')
    messageid = models.CharField(max_length=50, unique=True, verbose_name=u'微信messageid')
    content = models.CharField(max_length=100, null=True, blank=True,  db_index=True, verbose_name=u'微信内容')
    imgurl = models.URLField(null=True, blank=True, verbose_name=u'微信图片')
    create_time = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'发送信息的时间')
    code = models.IntegerField(db_index=True, null=True, blank=True, verbose_name=u'活动标记')
    is_check = models.NullBooleanField(default=None, verbose_name=u'客户发言是否经过审核')

    def __unicode__(self):
        return u'%s' % (self.content,)