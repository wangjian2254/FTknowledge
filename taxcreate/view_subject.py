#coding=utf-8
#Date:14-6-17
#Email:wangjian2254@gmail.com
import json
from django.db.models import Q
from taxcreate.forms import SubjectForm, PZForm
from taxcreate.models import Subject, Option, PZ, FL, KM
from util.tools import getResult, MyEncoder

__author__ = u'王健'


def updateSubject(request):
    pk = request.REQUEST.get('id', '')
    if pk:
        kindForm = SubjectForm(request.POST, instance=Subject.objects.get(pk=pk))
    else:
        kindForm = SubjectForm(request.POST)

    if not kindForm.is_valid():
        msg = kindForm.json_error()
        return getResult(False, msg, None)
    #if not kindForm.instance.accuracy:
    #    kindForm.instance.accuracy = 0.0
    if not pk:
        kindForm.instance.author=request.user
    kind = kindForm.save()

    if kind.type == 1:
        for i in range(20):
            id = request.REQUEST.get("option_id_%s" % i, None)
            content = request.REQUEST.get("option_content_%s" % i, None)
            is_right = request.REQUEST.get("option_is_right_%s" % i, None)
            if id or content or is_right:
                if is_right == 'true':
                    is_right = True
                else:
                    is_right = False
                if id:
                    option = Option.objects.get(pk=id)
                else:
                    option = Option()
                option.content = content
                option.is_right = is_right
                option.subject = kind
                option.save()
    else:
        #保存凭证信息
        pzpk = request.REQUEST.get('pzid', '')
        if pzpk:
            pzform = PZForm(request.POST, instance=PZ.objects.get(pk=pzpk))
        else:
            pzform = PZForm(request.POST)
        if not pzform.is_valid():
            msg = pzform.json_error()
            return getResult(False, msg, None)
        pz = pzform.save()
        fl = request.REQUEST.get('fl','')
        fllist = json.loads(fl)
        if len(fllist)==0:
            FL.objects.filter(pz=pz).delete()
            PZ.objects.get(pk=pz).delete()
            return getResult(True,'')
        flids=[]
        for fl in fllist:
            if fl.has_key('id'):
                f = FL.objects.get(pk=fl.get('id'))
            else:
                f = FL()
                f.pz = pz
            f.kmmc = KM.objects.get(pk=fl.get('kjkm'))
            f.fx = fl.get('fx')
            f.zy = fl.get('zy')
            if fl.get('fx'):
                f.num = fl.get('jje',0)
            else:
                f.num = fl.get('dje',0)
            f.save()
            flids.append(f.pk)
        if len(flids)>0:
            FL.objects.exclude(pk__in=flids).filter(pz=pz).delete()

    return getResult(True, u'保存试题信息成功', kind.pk)


def getOptionBySubject(request):
    sid = request.REQUEST.get('sid',None)
    if sid:
        subject = Subject.objects.get(pk=sid)
        options = MyEncoder.default(subject.option_set.all())
        if subject.rule_id:
            templateid = subject.rule.taxtemplate_id
            ruleid = subject.rule_id
        else:
            templateid =None
            ruleid = None
        return getResult(True,u'获取试题信息',{'sid':sid,'options':options,'templateid':templateid,'ruleid':ruleid})
    else:
        return getResult(False,u'获取试题信息失败，需要试题id',None)


def getSubjectByKind(request):
    kind = request.REQUEST.get('kind', None)
    if kind:
        sl = []
        for subject in Subject.objects.filter(Q(title__icontains=kind)):
            sl.append(MyEncoder.default(subject))
        return getResult(True, '', sl)
    else:
        return getResult(False, u'请提供关键字', None)


def getSubjectAll(request):
    limit = int(request.REQUEST.get('limit', '60'))
    start = int(request.REQUEST.get('start', '0'))
    all = request.REQUEST.get('all','')
    sl = []
    subjectquery = Subject.objects.all().order_by('-id')
    totalnum = subjectquery.count()
    if not all:
        subjectquery = subjectquery[start:start + limit]

    for subject in subjectquery:
        sl.append(MyEncoder.default(subject))
    return getResult(True, '', {'result': sl, 'limit': limit, 'start': start, 'total': totalnum})


def getSubjectById(request):
    id = request.REQUEST.get('id', '')
    if id:
        kind = Subject.objects.get(pk=id)
        k=MyEncoder.default(kind)
        k ['options']= []
        for o in Option.objects.filter(subject=kind):
            k['options'].append(MyEncoder.default(o))

        return getResult(True, u'获取考题成功', k)
    else:
        return getResult(False, u'考题不存在', None)


def delSubject(request):
    id = request.REQUEST.get('id', '')
    if id:
        kind = Subject.objects.get(pk=id)
        kind.delete()
    else:
        return getResult(False, u'考题不存在', None)

    return getResult(True, u'考题删除成功', id)


def delOption(request):
    id = request.REQUEST.get('id', '')
    if id:
        kind = Option.objects.get(pk=id)
        kind.delete()
    else:
        getResult(False, u'选项不存在', None)

    return getResult(True, u'选项删除成功', id)
