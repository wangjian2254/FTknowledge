# coding=utf-8
#Date:14-6-17
#Email:wangjian2254@gmail.com
import json
from django.http import HttpResponse
from util.tools import getResult, MyEncoder
from taxcreate.forms import GuanForm
from taxcreate.models import Guan, Subject, Paper, PZSubjest

__author__ = u'王健'


def getAllGuan(request):
    '''
    获取所有关卡
    '''
    guanlist = []
    guanlist.append(1)
    guanquery = Guan.objects.all().order_by('flag')
    guanlist = MyEncoder.default(guanquery)
    return getResult(True, '', {'result': guanlist})


def updateGuan(request):
    '''
    修改一个关卡
    '''

    pk = request.REQUEST.get('id', '')
    if pk:
        guanform = GuanForm(request.POST, instance=Guan.objects.get(pk=pk))
    else:
        guanform = GuanForm(request.POST)
    if not guanform.is_valid():
        msg = guanform.json_error()
        return getResult(False, msg, None)
    guan = guanform.save()
    return getResult(True, u'保存关卡信息成功', guan.pk)


def getPaperByGuan(request):
    '''
    获取关卡下的所有试卷
    '''
    pid = request.REQUEST.get('pid')
    if pid:
        guan = Guan.objects.get(pk=pid)
        subjects = MyEncoder.default(guan.paper_set.all())

        return getResult(True, u'获取到关卡成功', subjects)
    else:
        return getResult(False, u'获取关卡失败，请提供关卡id', None)


def doGuanPaper(request):
    '''
    管理关卡的试卷
    '''
    paperid = request.REQUEST.get('pid')
    guanid = request.REQUEST.get('gid')
    do = request.REQUEST.get('do')
    guan = Guan.objects.get(pk=guanid)
    paper = Paper.objects.get(pk=paperid)
    if do == 'add':

        if paper.guan_id == guanid:
            return getResult(False, u'已经关联过了', None)
        else:
            paper.guan = guan
            paper.save()
        return getResult(True, u'添加试题成功', paperid)
    else:
        paper.guan = None
        paper.save()
        return getResult(True, u'移除试题成功', paperid)


def delGuan(request):
    '''
    删除一个关卡，设置为不公开
    '''
    id = request.REQUEST.get('id', '')
    if id:
        guan = Guan.objects.get(pk=id)
        for paper in guan.paper_set.all():
            paper.guan = None
            paper.save()
        guan.delete()
    else:
        return getResult(False, u'关卡不存在', id)

    return getResult(True, '', id)


def getGuan(request):
    '''
    根据 id 获取一张关卡的完整信息，包括试卷
    '''
    id = request.REQUEST.get('id', '')
    if id:
        guan = Guan.objects.get(pk=id)
        pdict = MyEncoder.default(guan)
        return getResult(True, u'获取关卡成功', pdict)
    else:
        return getResult(False, u'关卡不存在', id)


def getGuanData(request):
    '''
    根据关卡id，获取关卡的 js 数据
    '''
    flag = request.REQUEST.get('flag', '')
    if flag:
        flag = int(flag)
        guanquery = Guan.objects.filter(flag=flag)
        if guanquery.count() == 1:
            guan = guanquery[0]
            total = guan.paper_set.all().count()
            if total > 1:
                import random

                paper = guan.paper_set.all()[random.randint(0, total)]
            elif total == 1:
                paper = guan.paper_set.all()[0]
            else:
                paper = None
        else:
            paper = None
        return HttpResponse(paper2js(paper, request))


def paper2js(paper, request):
    js = "var paper = %s;"
    if not paper:
        return 'var paper=null;'
    else:
        data = {}
        data['id'] = paper.pk;
        data['name'] = paper.guan.name;
        data['content'] = paper.content;
        data['right_ztdm'] = paper.right_ztdm;
        data['point'] = paper.guan.point
        data['time'] = paper.time
        if not data['time']:
            data['time']=1
        data['subject'] = []
        for i, s in enumerate(paper.subjects.all()):
            subject = {'sid': s.id, 'title': s.title, 'bz': s.bz, 'type': s.type, 'imgurl': [], 'option': []}
            if s.type == 2:
                pzlist = PZSubjest.objects.filter(subject=s, paper=paper)[:1]
                if len(pzlist) > 0:
                    subject['yzpzid'] = pzlist[0].yzpzid
            if s.rule_id:
                subject['imgurl'].append(
                    'http://%s/tax/showTaxImage?ruleid=%s' % (request.environ['HTTP_HOST'], s.rule_id))
            for o in s.option_set.all():
                subject['option'].append({'id': o.pk, 'content': o.content, 'is_right': o.is_right})
            data['subject'].append(subject)
        return js % json.dumps(data)



