#coding=utf-8
#Date:14-6-17
#Email:wangjian2254@gmail.com
from util.tools import getResult, MyEncoder
from taxcreate.forms import GuanForm
from taxcreate.models import Guan, Subject, Paper

__author__ = u'王健'




def getAllGuan(request):
    '''
    获取所有关卡
    '''
    guanlist = []
    guanquery = Guan.objects.all().order_by('flag')
    guanlist = MyEncoder.default(guanquery)
    return getResult(True, '', {'result':guanlist})



def updateGuan(request):
    '''
    修改一个关卡
    '''

    pk = request.REQUEST.get('id', '')
    if pk:
        guanform = GuanForm(request.POST, instance = Guan.objects.get(pk=pk))
    else:
        guanform = GuanForm(request.POST)
    if not guanform.is_valid():
        msg = guanform.json_error()
        return getResult(False,msg,None)
    guan = guanform.save()
    return getResult(True,u'保存关卡信息成功', guan.pk)


def getPaperByGuan(request):
    '''
    获取关卡下的所有试卷
    '''
    pid = request.REQUEST.get('pid')
    if pid:
        guan = Guan.objects.get(pk=pid)
        subjects = MyEncoder.default(guan.paper_set.all())

        return getResult(True,u'获取到关卡成功',subjects)
    else:
        return getResult(False,u'获取关卡失败，请提供关卡id',None)

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

        if paper.guan_id==guanid:
            return getResult(False,u'已经关联过了',None)
        else:
            paper.guan = guan
            paper.save()
        return getResult(True,u'添加试题成功',paperid)
    else:
        paper.guan=None
        paper.save()
        return getResult(True,u'移除试题成功',paperid)


def delGuan(request):
    '''
    删除一个关卡，设置为不公开
    '''
    id = request.REQUEST.get('id', '')
    if id:
        guan = Guan.objects.get(pk=id)
        for paper in guan.paper_set.all():
            paper.guan=None
            paper.save()
        guan.delete()
    else:
        return getResult(False, u'关卡不存在', id)

    return getResult(True,'', id)



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



