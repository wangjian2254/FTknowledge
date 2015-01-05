# coding=utf-8
#Date:14-6-17
#Email:wangjian2254@gmail.com
import datetime
import json
from django.db.models import Q
from FTknowledge.projectsettings import YSX_URL_SET_RIGHT_ZT, YSX_URL, YSX_URL_UPLOAD_YZPZ, YSX_URL_GO_RIGHT_ZT
from util.tools import getResult, MyEncoder
from taxcreate.forms import PaperForm
from taxcreate.models import Paper, Subject, PZSubjest, PaperSubject

__author__ = u'王健'


def getAllPaperUnGuan(request):
    '''
    获取所有未关联关卡的试卷
    '''
    paperlist = MyEncoder.default(Paper.objects.filter(guan=None).order_by('-id'))
    return getResult(True, u'获取所有未关联关卡的试卷', {"result": paperlist})


def getAllPaper(request):
    '''
    获取所有试卷
    '''
    paperlist = []

    is_pub = request.REQUEST.get('is_pub', '')

    title = request.REQUEST.get('title', '')
    all = request.REQUEST.get('all', '')

    limit = int(request.REQUEST.get('limit', '40'))
    start = int(request.REQUEST.get('start', '0'))
    paperquery = Paper.objects.all().order_by('title')

    if is_pub:
        if is_pub == 'true':
            paperquery = paperquery.filter(is_pub=True)
        else:
            paperquery = paperquery.filter(is_pub=False)

    if title:
        paperquery = paperquery.filter(title__icontains=title)

    totalnum = paperquery.count()
    if not all:
        paperquery = paperquery[start:start + limit]
    for p in paperquery:
        paperlist.append({"id": p.pk, 'title': p.title, 'kmkind': p.kmkind_id, 'flag': p.flag, 'content': p.content,
                          'right_ztdm': p.right_ztdm, 'is_pub': p.is_pub, 'guan_id': p.guan_id, 'time': p.time})
    return getResult(True, '', {'result': paperlist, 'limit': limit, 'start': start,
                                'total': totalnum})


def updatePaper(request):
    '''
    修改一个试卷
    '''

    pk = request.REQUEST.get('id', '')
    if pk:
        paperform = PaperForm(request.POST, instance=Paper.objects.get(pk=pk))
    else:
        paperform = PaperForm(request.POST)
    if not paperform.is_valid():
        msg = paperform.json_error()
        return getResult(False, msg, None)
    if not pk:
        paperform.instance.author = request.user
    paper = paperform.save()
    return getResult(True, u'保存分类信息成功', paper.pk)


def getSubjectByPaper(request):
    pid = request.REQUEST.get('pid')
    if pid:
        paper = Paper.objects.get(pk=pid)
        subjects = MyEncoder.default(paper.subjects.order_by('papersubject'))

        return getResult(True, u'获取到试题成功', subjects)
    else:
        return getResult(False, u'获取试题失败，请提供试卷id', None)


def getPaperByKind(request):
    kind = request.REQUEST.get('kind', None)
    if kind:
        paperlist = []
        query = Paper.objects.filter(Q(title__icontains=kind) | Q(flag__icontains=kind)).order_by('title')
        for p in query:
            paperlist.append({"id": p.pk, 'title': p.title, 'kmkind': p.kmkind_id, 'flag': p.flag, 'content': p.content,
                              'right_ztdm': p.right_ztdm, 'is_pub': p.is_pub, 'guan_id': p.guan_id, 'time': p.time})
        return getResult(True, '', {'result': paperlist, 'limit': query.count(), 'start': 0, 'total': query.count()})
    else:
        return getResult(False, u'请提供关键字', None)


def doPaperSubject(request):
    '''
    管理试卷的试题
    '''
    subjectid = request.REQUEST.get('sid')
    paperid = request.REQUEST.get('pid')
    do = request.REQUEST.get('do')
    paper = Paper.objects.get(pk=paperid)
    if do == 'add':
        if paper.subjects.filter(id=subjectid).count() > 0:
            return getResult(False, u'已经添加过了。', None)
        ps, c = PaperSubject.objects.get_or_create(paper=paper, subject_id=subjectid)
        ps.save()
        # paper.subjects.add(*Subject.objects.filter(pk=subjectid))
        return getResult(True, u'添加试题成功', subjectid)
    else:
        PaperSubject.objects.filter(paper=paper, subject_id=subjectid).delete()
        # paper.subjects.remove(*Subject.objects.filter(pk=subjectid))
        return getResult(True, u'移除试题成功', subjectid)


def delPaper(request):
    '''
    删除一个试卷，设置为不公开
    '''
    id = request.REQUEST.get('id', '')
    if id:
        paper = Paper.objects.get(pk=id)
        paper.delete()
    else:
        return getResult(False, u'试卷不存在', id)

    return getResult(True, '', id)


def getPaper(request):
    '''
    根据 id 获取一张试卷的完整信息，包括题目
    '''
    id = request.REQUEST.get('id', '')
    if id:
        paper = Paper.objects.get(pk=id)
        pdict = MyEncoder.default(paper)
        return getResult(True, u'获取试卷成功', pdict)
    else:
        return getResult(False, u'试卷不存在', id)


    # def uploadYZPZ(request):
    #     '''
    #     向云实训 上传，预制凭证、原始凭证
    #     '''
    #     import urllib
    #     import urllib2
    #     id = request.REQUEST.get('id', '')
    #     if id:
    #         paper = Paper.objects.get(pk=id)
    #
    #         url = YSX_URL_UPLOAD_YZPZ
    #         values =[]
    #         for s in paper.subjects.all().filter(type=2).order_by('id'):
    #             values.append({"id":s.pk,'imgurl':'http://%s/tax/showTaxImage?ruleid=%s'%(request.environ['HTTP_HOST'],s.rule_id),'ztdm':paper.right_ztdm,'ssq':datetime.datetime.strftime('%Y%m%d'),'discription':s.title})
    #         req = urllib2.Request(url, json.dumps(values))
    #         response = urllib2.urlopen(req)
    #         html = response.read()
    #         if html:
    #             result = json.loads(html)
    #             for k,v in result:
    #                 pzsubject = PZSubjest.objects.get_or_create(subject=k,paper=paper)
    #                 pzsubject.yzpzid = v
    #                 pzsubject.save()
    #             return getResult(True,u'创建标准账套成功',paper.right_ztdm)
    #
    #     return getResult(False,u'创建标准账套失败',None)