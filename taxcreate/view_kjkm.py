# coding=utf-8
#Date:2014/8/6
#Email:wangjian2254@gmail.com
from taxcreate.forms import KMForm
from taxcreate.models import KM
from util.tools import getResult, MyEncoder

__author__ = u'王健'



def updateKJKM(request):
    pk = request.REQUEST.get('id', '')
    if pk:
        kindForm = KMForm(request.POST, instance=KM.objects.get(pk=pk))
    else:
        kindForm = KMForm(request.POST)


    if not kindForm.is_valid():
        msg = kindForm.json_error()
        return getResult(False, msg, None)
    #if not kindForm.instance.accuracy:
    #    kindForm.instance.accuracy = 0.0
    # if not pk:
    #     kindForm.instance.author=request.user
    kmquery = KM.objects.filter(kmbh=request.POST.get('kmbh'),paper_id=request.POST.get('paper'))
    if pk:
        kmquery = kmquery.exclude(pk=pk)
    if kmquery.count()>0:
        return getResult(False, u'科目编号不能重复', None)
    kind = kindForm.save()
    return getResult(True, u'保存试题信息成功', kind.pk)


def getAllPaperKM(request):
    '''
    获取所有未关联关卡的试卷
    '''
    paperlist = MyEncoder.default(KM.objects.filter(paper_id=request.REQUEST.get('paperid')).order_by('kmbh'))
    return getResult(True,u'获取科目列表',{"result":paperlist})
