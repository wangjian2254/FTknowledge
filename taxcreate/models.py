#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.contrib.auth.models import User

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




class Guan(models.Model):
    '''
    关卡管理
    '''
    flag = models.IntegerField(verbose_name=u'关卡标记',unique=True,help_text=u'标记隶属于某一关')
    name = models.CharField(max_length=30,verbose_name=u'关卡名字')
    point = models.IntegerField(default=10,verbose_name=u'关卡积分',help_text=u'关卡积分或金币')
    # paper = models.ManyToManyField(Paper,blank=True, null=True,verbose_name=u'包含试卷',help_text=u'如只有一个，则必选，如果有多个，则随机选择')

    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = u'关卡'
        verbose_name_plural = u'关卡管理'




class Paper(models.Model):
    '''
    试卷，可以指定考试人员范围也可以不指定
    '''
    choices = ((True, u'已发布'), (False, u'未发布'))

    title = models.CharField(max_length=200,verbose_name=u'标题', help_text=u'考卷名字')
    content = models.TextField(verbose_name=u'内容', help_text=u'考卷描述', blank=True, null=True)
    subjects = models.ManyToManyField("Subject",null=True,blank=True,verbose_name=u'试题')
    right_ztdm = models.CharField(max_length=200,null=True,blank=True,verbose_name=u'标准答案账套', help_text=u'标准答案账套id')
    is_pub = models.BooleanField(choices=choices, default=True, verbose_name=u'是否发布', help_text=u'发布后不可修改')
    guan = models.ForeignKey(Guan,verbose_name=u'隶属关卡',help_text=u'隶属的关卡',null=True,blank=True)

    def __unicode__(self):
        return self.title

    class Meta():
        verbose_name = u'试卷'

class PaperResult(models.Model):
    '''
    人员考试的答题结果
    '''
    paper = models.ForeignKey(Paper)
    user = models.ForeignKey(User, verbose_name=u'操作人', help_text=u'参与考试的人员')
    editDate = models.DateTimeField(verbose_name=u'答卷时间')
    accuracy = models.FloatField(default=0.0, verbose_name=u'正确率',help_text=u'试卷正确率')
    result = models.TextField(blank=True, null=True, verbose_name=u'做题结果，json数据')

    def __unicode__(self):
        return u'%s 答题: %s'%(self.user.first_name,self.paper.title)


    class Meta():
        verbose_name = u'答题'

class Subject(models.Model):
    '''
    试题信息，有记录正确次数和错误次数，方便计算试题的正确率，未来可以衡量难度
    '''
    title = models.CharField(max_length=2000, verbose_name=u'题目', help_text=u'选择题题目')
    bz = models.CharField(max_length=1000,blank=True, null=True,verbose_name=u'备注',help_text=u'正确答案的解释')
    type = models.IntegerField(default=1,verbose_name=u'题型',help_text=u'1:选择题,2:凭证录入题')
    rule = models.ForeignKey(TaxRule,null=True,blank=True,verbose_name=u'自定义票据',help_text=u'自定义票据规则')

    def __unicode__(self):
        return self.title


    class Meta():
        verbose_name = u'题目'




class Option(models.Model):
    '''
    试题的选项
    '''
    subject = models.ForeignKey(Subject, verbose_name=u'题目', help_text=u'隶属于哪一个题目')
    content = models.CharField(max_length=500, verbose_name=u'选项内容', help_text=u'投票选项')
    is_right = models.BooleanField(default=False, verbose_name=u'正确',help_text=u'是否是正确选项')

    def __unicode__(self):
        return self.content

    class Meta():
        verbose_name = u'选项'
        verbose_name_plural = u'选项列表'



class PZSubjest(models.Model):
    '''
    试题的选项
    '''
    subject = models.ForeignKey(Subject, verbose_name=u'题目', help_text=u'隶属于哪一个题目')
    paper = models.ForeignKey(Paper, verbose_name=u'试卷',help_text=u'隶属试卷')
    yzpzid = models.CharField(max_length=100,verbose_name=u'预制凭证id')

    def __unicode__(self):
        return self.content

    class Meta():
        verbose_name = u'选项'
        verbose_name_plural = u'选项列表'
        unique_together = [('subject','paper')]


