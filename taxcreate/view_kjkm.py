# coding=utf-8
# Date:2014/8/6
#Email:wangjian2254@gmail.com
import json
from FTknowledge.settings import STATIC_URL, STATIC_ROOT
from knowledge.models import KJKM
from taxcreate.forms import KMForm, KMKindForm
from taxcreate.models import KM, KMKind
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
    kmquery = KM.objects.filter(kmbh=request.POST.get('kmbh'), kind_id=request.POST.get('kind'))
    if pk:
        kmquery = kmquery.exclude(pk=pk)
    if kmquery.count() > 0:
        return getResult(False, u'科目编号不能重复', None)
    kind = kindForm.save()
    return getResult(True, u'保存试题信息成功', kind.pk)


def getAllKMByKind(request):
    """
    获取完整会计科目
    """
    paperlist = MyEncoder.default(KM.objects.filter(kind_id=request.REQUEST.get('kind')).order_by('kmbh'))
    return getResult(True, u'获取科目列表', {"result": paperlist})


def getAllKMLabelByKind(request):
    """
    获取完整会计科目
    """
    paperlist = []
    for km in KM.objects.filter(kind_id=request.REQUEST.get('kind')).order_by('kmbh'):
        paperlist.append({"id" : km.pk, "name" : "%s:%s" % (km.kmbh, km.name)})
    return getResult(True, u'获取科目列表', {"result": paperlist})



def getAllKind(request):
    """
    获取完整会计科目
    """
    paperlist = MyEncoder.default(KMKind.objects.all().order_by('-id'))
    return getResult(True, u'获取科目列表', {"result": paperlist})

def delKjkmKind(request):
    pk = request.REQUEST.get('id', '')
    kind = KMKind.objects.get(pk=pk)
    if 0==kind.subject_set.count():
        kind.subject_set.all().delete()
        kind.km_set.all().delete()
        kind.delete()
        return getResult(True, u'会计科目分类删除成功',None)
    return getResult(False, u'会计科目分类删除失败，还有题目使用此会计科目', None)


def delKJKM(request):
    pk = request.REQUEST.get('id', '')
    kind = KM.objects.get(pk=pk)
    if 0==kind.fl_set.count():
        kind.fl_set.all().delete()
        kind.delete()
        return getResult(True, u'会计科目删除成功',None)
    return getResult(False, u'会计科目删除失败，还有题目使用此会计科目', None)


def updateKJKMKind(request):
    pk = request.REQUEST.get('id', '')
    if pk:
        kindForm = KMKindForm(request.POST, instance=KMKind.objects.get(pk=pk))
    else:
        kindForm = KMKindForm(request.POST)

    if not kindForm.is_valid():
        msg = kindForm.json_error()
        return getResult(False, msg, None)
    kind = kindForm.save()
    # l=[]
    if not pk:
        k = json.load(open("%skjkm.json"%STATIC_ROOT))
        for oldkm in k:
            try:
                # l.append({'kmbh':km.name.split(":")[0],'name':km.name.split(":")[1]})
                km = KM()
                km.kind = kind
                km.kmbh = oldkm.get("kmbh", "")
                km.name = oldkm.get("name", "")
                km.save()
            except:
                pass
    return getResult(True, u'保存会计科目信息成功', kind.pk)


def exportKJKM(request):
    pk = request.REQUEST.get('id', '')
    kind = KMKind.objects.get(pk=pk)
    l=[]
    if pk:

        for oldkm in KM.objects.filter(kind=kind):
            l.append({"kmbh":oldkm.kmbh,"name":oldkm.name})
        f=open("%skjkm.json"%STATIC_ROOT,"w")
        f.write(json.dumps(l))
        f.close()
    return getResult(True, u'保存会计科目信息成功')
