from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'服务行业', help_text=u'会计服务行业')
    is_active = models.BooleanField(default=True, verbose_name=u'可用')


class TaxKind(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=u'分类名称', help_text=u'多级分类')
    fatherKind = models.ForeignKey('TaxKind', blank=True, null=True, verbose_name=u'父类', help_text=u'多级分类')
    is_active = models.BooleanField(default=True, verbose_name=u'可用')


class TaxTicket(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name=u'票据名称')
    group = models.ForeignKey(Group)
    taxkind = models.ForeignKey(TaxKind)


class ZZBB(models.Model):
    taxticket = models.ForeignKey(TaxTicket)
    glzzsbbzb = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联增值税报表主表')
    glzzsbbzby = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联增值税报表主表一')
    glzzsbbzbe = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联增值税报表主表二')
    gdzcdk = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'固定资产抵扣')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'可用')


class CZZS(models.Model):
    taxticket = models.ForeignKey(TaxTicket)
    glqysdszb = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联企业所得税主表')
    glssyhmxb = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联税收优惠明细表')
    glsdsylzsdbb = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联所得税与流转税对比表')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'可用')


class CWBB(models.Model):
    taxticket = models.ForeignKey(TaxTicket)
    glcwbblrb = models.CharField(max_length=200, db_index=True, blank=True, null=True, verbose_name=u'关联财务报表利润表')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'可用')


class PZ(models.Model):
    taxticket = models.ForeignKey(TaxTicket)
    user = models.ForeignKey(User, verbose_name=u'创建者')
    name = models.CharField(max_length=20, db_index=True, blank=True, null=True, verbose_name=u'凭证名称')
    desc = models.CharField(max_length=1000, db_index=True, blank=True, null=True, verbose_name=u'凭证备注')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'可用')


class FL(models.Model):
    FX = ((u'借', True), (u'贷', False))
    pz = models.ForeignKey(PZ)
    kmmc = models.CharField(max_length=300, db_index=True, blank=True, null=True, verbose_name=u'科目名称',
                            help_text=u'分录科目名称')
    zy = models.CharField(max_length=100, db_index=True, blank=True, null=True, verbose_name=u'摘要')
    fx = models.BooleanField(default=True, choices=FX, verbose_name=u'方向', help_text=u'借正贷负')
    desc = models.CharField(max_length=1000, db_index=True, blank=True, null=True, verbose_name=u'凭证备注')


class Replay(models.Model):
    replayId = models.IntegerField(verbose_name=u'主键', db_index=True)
    replayType = models.CharField(max_length=20, db_index=True, verbose_name=u'提问实体')
    user = models.ForeignKey(User)
    content = models.CharField(max_length=2000, db_index=True, verbose_name=u'内容')
    is_first = models.BooleanField(default=True, db_index=True, verbose_name=u'是否第一条', help_text=u'由第一条来决定是否讨论结束')
    is_close = models.BooleanField(default=False, db_index=True, verbose_name=u'是否结束')


class ImageInfo(models.Model):
    img = models.ImageField(upload_to='upload/')
    index = models.IntegerField(default=0, blank=True, null=True, db_index=True, verbose_name=u'排序')
    modelId = models.IntegerField(verbose_name=u'主键', db_index=True)
    modelType = models.CharField(max_length=20, db_index=True, verbose_name=u'使用图片的实体')
