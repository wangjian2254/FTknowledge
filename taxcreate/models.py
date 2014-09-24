# coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.contrib.auth.models import User
from model_history.history import ModelWithHistory

__author__ = u'王健'
from django.db import models

# Create your models here.

class TaxTuZhang(ModelWithHistory):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'图章名字', help_text=u'图章名字')
    img = models.ImageField(upload_to='tuzhang/', verbose_name=u'图章图片')


    def __unicode__(self):
        return u'%s' % (self.name,)



class TaxTemplate(ModelWithHistory):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'票据模板', help_text=u'票据模板名称')
    img = models.ImageField(upload_to='tax/', verbose_name=u'票据模板位置')


    def __unicode__(self):
        return u'%s' % (self.name,)

    class Meta():
        verbose_name = u'票据分组'
        verbose_name_plural = u'票据分组列表'

    class History:
        model = True
        fields = ('name',)


class TaxRule(ModelWithHistory):
    taxtemplate = models.ForeignKey(TaxTemplate, verbose_name=u'票据模板')
    name = models.CharField(max_length=50, verbose_name=u'生成票据条件')

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.taxtemplate.name)

    class Meta():
        verbose_name = u'票据分组'
        verbose_name_plural = u'票据分组列表'

    class History:
        model = True
        fields = ('taxtemplate', 'name')


class RuleItem(ModelWithHistory):
    rule = models.ForeignKey(TaxRule, verbose_name=u'票据条件')
    index = models.IntegerField(verbose_name=u'索引')
    x = models.IntegerField(verbose_name=u'模板位置x')
    y = models.IntegerField(verbose_name=u'模板位置y')
    size = models.IntegerField(verbose_name=u'字体大小')
    color = models.IntegerField(verbose_name=u'字体颜色')
    family = models.IntegerField(verbose_name=u'字体类型')
    word = models.CharField(max_length=200, verbose_name=u'文字')
    tuzhang = models.ForeignKey(TaxTuZhang, null=True, blank=True, verbose_name=u'图章位置')


    def __unicode__(self):
        return u'%s' % (self.word,)

    class Meta():
        verbose_name = u'票据打印参数'
        verbose_name_plural = u'票据打印参数列表'

    class History:
        model = True
        fields = ('rule', 'index', 'x', 'y', 'size', 'color', 'family', 'word')


class Guan(ModelWithHistory):
    """
    关卡管理
    """
    flag = models.IntegerField(verbose_name=u'关卡标记', unique=True, help_text=u'标记隶属于某一关')
    name = models.CharField(max_length=30, verbose_name=u'关卡名字')
    point = models.IntegerField(default=10, verbose_name=u'关卡积分', help_text=u'关卡积分或金币')
    # paper = models.ManyToManyField(Paper,blank=True, null=True,verbose_name=u'包含试卷',help_text=u'如只有一个，则必选，如果有多个，则随机选择')

    def __unicode__(self):
        return self.name

    class Meta():
        verbose_name = u'关卡'
        verbose_name_plural = u'关卡管理'


    class History:
        model = True
        fields = ('name', 'flag', 'point')


class Paper(ModelWithHistory):
    """
    试卷，可以指定考试人员范围也可以不指定
    """
    choices = ((True, u'已发布'), (False, u'未发布'))

    title = models.CharField(max_length=200, verbose_name=u'标题', help_text=u'考卷名字')
    flag = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'标记', help_text=u'录入者的标记')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name=u'作者')
    content = models.TextField(verbose_name=u'内容', help_text=u'考卷描述', blank=True, null=True)
    subjects = models.ManyToManyField("Subject", through='PaperSubject', null=True, blank=True, verbose_name=u'试题')
    right_ztdm = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'标准答案账套', help_text=u'标准答案账套id')
    is_pub = models.BooleanField(choices=choices, default=True, verbose_name=u'是否发布', help_text=u'发布后不可修改')
    guan = models.ForeignKey(Guan, verbose_name=u'隶属关卡', help_text=u'隶属的关卡', null=True, blank=True)
    time = models.IntegerField(verbose_name=u'考试时间', help_text=u'考试允许使用时间')
    kmkind = models.ForeignKey('KMKind',  null=True, blank=True, verbose_name=u'使用的会计科目类型')

    def __unicode__(self):
        return self.title

    class Meta():
        verbose_name = u'试卷'


    class History:
        model = True
        fields = ('title', 'content', 'subjects', 'right_ztdm', 'is_pub', 'guan', 'time')


class PaperSubject(models.Model):
    paper = models.ForeignKey(Paper)
    subject = models.ForeignKey('Subject')
    class Meta:
        db_table = 'taxcreate_paper_subjects'
        ordering = ('id',)
        pass
        # ordering = ('id')

class PaperResult(ModelWithHistory):
    """
    人员考试的答题结果
    """
    paper = models.ForeignKey(Paper)
    user = models.ForeignKey(User, verbose_name=u'操作人', help_text=u'参与考试的人员')
    editDate = models.DateTimeField(verbose_name=u'答卷时间')
    accuracy = models.FloatField(default=0.0, verbose_name=u'正确率', help_text=u'试卷正确率')
    result = models.TextField(blank=True, null=True, verbose_name=u'做题结果，json数据')

    def __unicode__(self):
        return u'%s 答题: %s' % (self.user.first_name, self.paper.title)


    class Meta():
        verbose_name = u'答题'


    class History:
        model = True
        fields = ('paper', 'user', 'editDate', 'accuracy', 'result')


class Subject(ModelWithHistory):
    """
    试题信息，有记录正确次数和错误次数，方便计算试题的正确率，未来可以衡量难度
    """
    title = models.CharField(max_length=2000, verbose_name=u'题目', help_text=u'选择题题目')
    flag = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'标记', help_text=u'录入者的标记')
    author = models.ForeignKey(User, blank=True, null=True, verbose_name=u'作者')
    bz = models.CharField(max_length=1000, blank=True, null=True, verbose_name=u'备注', help_text=u'正确答案的解释')
    type = models.IntegerField(default=1, verbose_name=u'题型', help_text=u'1:选择题,2:凭证录入题')
    rule = models.ForeignKey(TaxRule, null=True, blank=True, verbose_name=u'自定义票据', help_text=u'自定义票据规则')

    kmkind = models.ForeignKey('KMKind',  null=True, blank=True, verbose_name=u'使用的会计科目类型')

    def __unicode__(self):
        return self.title


    class Meta():
        verbose_name = u'题目'


    class History:
        model = True
        fields = ('title', 'bz', 'type', 'rule')


class Option(ModelWithHistory):
    """
    试题的选项
    """
    subject = models.ForeignKey(Subject, verbose_name=u'题目', help_text=u'隶属于哪一个题目')
    content = models.CharField(max_length=500, verbose_name=u'选项内容', help_text=u'投票选项')
    is_right = models.BooleanField(default=False, verbose_name=u'正确', help_text=u'是否是正确选项')

    def __unicode__(self):
        return self.content

    class Meta():
        verbose_name = u'选项'
        verbose_name_plural = u'选项列表'


    class History:
        model = True
        fields = ('subject', 'content', 'is_active')


class PZSubjest(ModelWithHistory):
    """
    试题的选项
    """
    subject = models.ForeignKey(Subject, verbose_name=u'题目', help_text=u'隶属于哪一个题目')
    paper = models.ForeignKey(Paper, verbose_name=u'试卷', help_text=u'隶属试卷')
    yzpzid = models.CharField(max_length=100, verbose_name=u'预制凭证id')

    def __unicode__(self):
        return self.content

    class Meta():
        verbose_name = u'选项'
        verbose_name_plural = u'选项列表'
        unique_together = [('subject', 'paper')]


    class History:
        model = True
        fields = ('subject', 'paper', 'yzpzid')

class KMKind(ModelWithHistory):
    name = models.CharField(max_length=200,unique=True, verbose_name=u'会计科目类型')
    desc = models.TextField(verbose_name=u'会计科目类型')
    class Meta():
        verbose_name = u'会计科目'
        verbose_name_plural = u'会计科目列表'

    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'desc')

class KM(ModelWithHistory):
    kind = models.ForeignKey(KMKind, verbose_name=u'会计科目类型')
    kmbh = models.CharField(max_length=10, db_index=True, verbose_name=u'科目编号')
    name = models.CharField(max_length=200, verbose_name=u'会计科目')
    # fatherKM = models.ForeignKey('KM', blank=True, null=True)
    class Meta():
        verbose_name = u'会计科目'
        verbose_name_plural = u'会计科目列表'
        unique_together = [('kind', 'kmbh')]

    def __unicode__(self):
        return u'%s' % (self.name,)

    class History:
        model = True
        fields = ('name', 'kmbh', 'kind')


class PZ(ModelWithHistory):
    subject = models.ForeignKey(Subject)
    desc = models.TextField(verbose_name=u'凭证解释')

    class Meta():
        verbose_name = u'凭证'
        verbose_name_plural = u'凭证列表'

    def __unicode__(self):
        return u'%s 凭证' % (self.subject,)

    class History:
        model = True
        fields = ('desc')


class FL(ModelWithHistory):
    FX = ((u'借', True), (u'贷', False))
    pz = models.ForeignKey(PZ)
    kmmc = models.ForeignKey(KM, db_index=True, blank=True, null=True, verbose_name=u'科目名称',
                             help_text=u'分录科目名称')
    # zy = models.CharField(max_length=100, db_index=True, blank=True, null=True, verbose_name=u'摘要')
    fx = models.BooleanField(default=True, choices=FX, verbose_name=u'方向', help_text=u'借正贷负')
    num = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    zy = models.TextField(blank=True, null=True, verbose_name=u'摘要')
    # desc = models.CharField(max_length=1000,  blank=True, null=True, verbose_name=u'凭证备注')
    class Meta():
        verbose_name = u'分录'
        verbose_name_plural = u'分录列表'

    def __unicode__(self):
        return u'%s' % (self.pz,)

    class History:
        model = True
        fields = ('pz', 'kmmc', 'fx', 'num', 'zy')
