#coding=utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from model_history.history import ModelWithHistory


class Group(ModelWithHistory):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'服务行业', help_text=u'会计服务行业')
    is_active = models.BooleanField(default=True, verbose_name=u'可用')
    class Meta():
        verbose_name=u'票据分组'
        verbose_name_plural=u'票据分组列表'
    def __unicode__(self):
        return u'%s'%(self.name,)

    class History:
        model = True
        fields = ('name', 'is_active')


class TaxKind(ModelWithHistory):
    name = models.CharField(max_length=100, verbose_name=u'分类名称', help_text=u'多级分类')
    fatherKind = models.ForeignKey('TaxKind', blank=True, null=True, verbose_name=u'父类', help_text=u'多级分类')
    is_active = models.BooleanField(default=True, verbose_name=u'可用')
    class Meta():
        verbose_name=u'票据分类'
        verbose_name_plural=u'票据分类列表'
    def __unicode__(self):
        return u'%s' % (self.name,)
    class Meta():
        unique_together =(('name','fatherKind'),)

    class History:
        model = True
        fields = ('name', 'fatherKind','is_active')



class TaxTicket(ModelWithHistory):

    name = models.CharField(max_length=1000, verbose_name=u'票据名称')
    group = models.ForeignKey(Group)
    taxkind = models.ForeignKey(TaxKind)
    class Meta():
        verbose_name=u'票据'
        verbose_name_plural=u'票据列表'
    def __unicode__(self):
        return u'%s' % (self.name,)
    class History:
        model = True
        fields = ('name', 'group','taxkind')


class KJKM(ModelWithHistory):
    name = models.CharField(max_length=100,db_index=True,verbose_name=u'会计科目名称')
    def __unicode__(self):
        return u'%s' % (self.name,)
    class Meta():
        verbose_name=u'会计科目'
        verbose_name_plural=u'会计科目列表'
    class History:
        model = True
        fields = ('name')

class KJKMTicket(ModelWithHistory):
    kjkm = models.ForeignKey(KJKM,verbose_name=u'会计科目')
    tickets = models.ForeignKey(TaxTicket,verbose_name=u'关联票据')
    class Meta():
        verbose_name=u'会计科目关联票据'
        verbose_name_plural=u'会计科目关联票据列表'
    def __unicode__(self):
        return u'%s_%s' % (self.kjkm.name,self.tickets.name)
    class History:
        model = True
        fields = ('kjkm', 'tickets')

class BB(models.Model):
    name = models.CharField(max_length=20,db_index=True,verbose_name=u'报表名称')



class BBField(models.Model):
    bb = models.ForeignKey(BB,verbose_name=u'隶属报表')
    fieldname = models.CharField(max_length=20,verbose_name=u'字段名称')



class BBFieldValue(models.Model):
    kjkmticket = models.ForeignKey(KJKMTicket,verbose_name=u'会计科目票据')
    bbfield = models.ForeignKey(BBField,verbose_name=u'对应表字段')
    value = models.CharField(max_length=200,verbose_name=u'字段对应值')


    class Meta():
        unique_together =(('kjkmticket','bbfield'),)



class PZ(ModelWithHistory):

    business = models.ForeignKey('Business')
    user = models.ForeignKey(User, verbose_name=u'创建者')
    desc = models.TextField(verbose_name=u'简介')
    is_active = models.BooleanField(default=True, db_index=True, verbose_name=u'可用')
    class Meta():
        verbose_name=u'凭证'
        verbose_name_plural=u'凭证列表'
    def __unicode__(self):
        return u'%s 凭证' % (self.business,)
    def getImg(self):
        for img in ImageInfo.objects.filter(modelType='pz',modelId=self.pk).order_by('id')[:1]:
            return img.img.url
        return ''

    class History:
        model = True
        fields = ('business', 'user','desc','is_right')

class FL(ModelWithHistory):
    FX = ((u'借', True), (u'贷', False))
    pz = models.ForeignKey(PZ)
    kmmc = models.ForeignKey('KM', db_index=True, blank=True, null=True, verbose_name=u'科目名称',
                            help_text=u'分录科目名称')
    # zy = models.CharField(max_length=100, db_index=True, blank=True, null=True, verbose_name=u'摘要')
    fx = models.BooleanField(default=True, choices=FX, verbose_name=u'方向', help_text=u'借正贷负')
    num=models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)
    zy=models.TextField(blank=True,null=True,verbose_name=u'摘要')
    # desc = models.CharField(max_length=1000,  blank=True, null=True, verbose_name=u'凭证备注')
    class Meta():
        verbose_name=u'分录'
        verbose_name_plural=u'分录列表'
    def __unicode__(self):
        return u'%s' % (self.pz,)
    class History:
        model = True
        fields = ('pz', 'kmmc','fx','num','zy')


class Replay(models.Model):
    replayId = models.IntegerField(verbose_name=u'主键', db_index=True)
    replayType = models.CharField(max_length=20, db_index=True, verbose_name=u'提问实体')
    user = models.ForeignKey(User)
    content = models.CharField(max_length=1000,  verbose_name=u'内容')
    is_first = models.BooleanField(default=True, db_index=True, verbose_name=u'是否第一条', help_text=u'由第一条来决定是否讨论结束')
    is_close = models.BooleanField(default=False, db_index=True, verbose_name=u'是否结束')


class ImageInfo(models.Model):
    img = models.ImageField(upload_to='upload/')
    index = models.IntegerField(default=0, blank=True, null=True, db_index=True, verbose_name=u'排序')
    modelId = models.IntegerField(verbose_name=u'主键', db_index=True)
    modelType = models.CharField(max_length=20, db_index=True, verbose_name=u'使用图片的实体')




class Rule(ModelWithHistory):
    name = models.CharField(max_length=30,db_index=True,verbose_name=u'规则名')
    class Meta():
        verbose_name=u'行业'
        verbose_name_plural=u'行业列表'

    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name')

class Ticket(ModelWithHistory):
    name = models.CharField(max_length=200,db_index=True, unique=True,verbose_name=u'票据名称')
    desc = models.CharField(max_length=4000, blank=True, null=True, verbose_name=u'票据名称')
    fatherTicket = models.ForeignKey('Ticket', blank=True, null=True)

    def getImgs(self):
        l = []
        for img in ImageInfo.objects.filter(modelType='ticket',modelId=self.pk).order_by('id'):
            l.append(img.img.url)
        return l

    class Meta():
        verbose_name=u'票据'
        verbose_name_plural=u'票据列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'desc','fatherTicket')

class Business(ModelWithHistory):
    name = models.CharField(max_length=200,db_index=True, verbose_name=u'业务名称')
    num = models.CharField(max_length=3,verbose_name=u'业务号')
    fatherBusiness = models.ForeignKey('Business', blank=True, null=True)

    def ywbh(self):
        if self.fatherBusiness:
            return '%s%s'%(self.fatherBusiness.ywbh(),self.num)
        else:
            return '%s'%self.num

    class Meta():
        verbose_name=u'业务'
        verbose_name_plural=u'业务列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'num','fatherBusiness')

class KM(ModelWithHistory):
    name = models.CharField(max_length=200,db_index=True, unique=True,verbose_name=u'会计科目')
    # fatherKM = models.ForeignKey('KM', blank=True, null=True)
    class Meta():
        verbose_name=u'会计科目'
        verbose_name_plural=u'会计科目列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name')

class KJZD(ModelWithHistory):
    name = models.CharField(max_length=2000, verbose_name=u'会计制度')
    fatherKJZD = models.ForeignKey('KJZD', blank=True, null=True)
    class Meta():
        verbose_name=u'会计制度'
        verbose_name_plural=u'会计制度列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'fatherKJZD')

class SF(ModelWithHistory):
    name = models.CharField(max_length=2000, verbose_name=u'税法')
    fatherSF = models.ForeignKey('SF', blank=True, null=True)
    class Meta():
        verbose_name=u'税法'
        verbose_name_plural=u'税法列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'fatherSF')


class SSTS(ModelWithHistory):
    name = models.CharField(max_length=2000, verbose_name=u'税法')
    fatherSSTS = models.ForeignKey('SSTS', blank=True, null=True)
    class Meta():
        verbose_name=u'涉税提示'
        verbose_name_plural=u'涉税提示列表'
    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'fatherSSTS')


class Relation(ModelWithHistory):
    rule = models.ForeignKey(Rule)
    ticket = models.ForeignKey(Ticket)
    business = models.ForeignKey(Business)
    # km = models.ForeignKey(KM)
    kjzds = models.ManyToManyField(KJZD)
    sf = models.ManyToManyField(SF)
    ssts = models.ManyToManyField(SSTS,blank=True,null=True)

    class Meta():
        verbose_name=u'关系'
        verbose_name_plural=u'关系列表'
        unique_together =(('rule','ticket','business'),)

    def __unicode__(self):
        return u'%s_%s_%s_%s' % (self.rule.name,self.ticket.name,self.business.name,self.km.name,)

    class History:
        model = True
        fields = ('rule', 'ticket','business','kjzds','sf','ssts')
