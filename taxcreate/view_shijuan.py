#coding=utf-8
#Date:14-6-17
#Email:wangjian2254@gmail.com
from util.tools import getResult, MyEncoder
from taxcreate.forms import PaperForm
from taxcreate.models import Paper, Subject

__author__ = u'王健'

def getAllPaperUnGuan(request):
    '''
    获取所有未关联关卡的试卷
    '''
    paperlist = MyEncoder.default(Paper.objects.filter(guan=None).order_by('-id'))
    return getResult(True,u'获取所有未关联关卡的试卷',{"result":paperlist})


def getAllPaper(request):
    '''
    获取所有试卷
    '''
    paperlist = []

    is_pub = request.REQUEST.get('is_pub', '')

    title = request.REQUEST.get('title', '')


    limit = int(request.REQUEST.get('limit', '40'))
    start = int(request.REQUEST.get('start', '0'))
    paperquery = Paper.objects.all().order_by('-id')

    if is_pub:
        if is_pub=='true':
            paperquery = paperquery.filter(is_pub=True)
        else:
            paperquery = paperquery.filter(is_pub=False)

    if title:
        paperquery = paperquery.filter(title__icontains = title)





    totalnum = paperquery.count()
    for p in paperquery[start:start+limit]:
        paperlist.append({"id":p.pk, 'title':p.title,'content':p.content,'right_ztdm':p.right_ztdm,'is_pub':p.is_pub,'guan_id':p.guan_id})
    return getResult(True, '', {'result':paperlist, 'limit': limit, 'start': start,
                                'total': totalnum})



def updatePaper(request):
    '''
    修改一个试卷
    '''

    pk = request.REQUEST.get('id', '')
    if pk:
        paperform = PaperForm(request.POST, instance = Paper.objects.get(pk=pk))
    else:
        paperform = PaperForm(request.POST)
    if not paperform.is_valid():
        msg = paperform.json_error()
        return getResult(False,msg,None)
    paper = paperform.save()
    return getResult(True,u'保存分类信息成功', paper.pk)


def getSubjectByPaper(request):
    pid = request.REQUEST.get('pid')
    if pid:
        paper = Paper.objects.get(pk=pid)
        subjects = MyEncoder.default(paper.subjects.all())

        return getResult(True,u'获取到试题成功',subjects)
    else:
        return getResult(False,u'获取试题失败，请提供试卷id',None)

def doPaperSubject(request):
    '''
    管理试卷的试题
    '''
    subjectid = request.REQUEST.get('sid')
    paperid = request.REQUEST.get('pid')
    do = request.REQUEST.get('do')
    paper = Paper.objects.get(pk=paperid)
    if do == 'add':
        if paper.subjects.filter(id=subjectid).count()>0:
            return getResult(False,u'已经添加过了。',None)
        paper.subjects.add(*Subject.objects.filter(pk=subjectid))
        return getResult(True,u'添加试题成功',subjectid)
    else:
        paper.subjects.remove(*Subject.objects.filter(pk=subjectid))
        return getResult(True,u'移除试题成功',subjectid)


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

    return getResult(True,'', id)



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





def getMyPaper(request):
    '''
    type ：need、do 两个值
    need:获取所有需要我做的试卷
    do:获取我做过的所有试卷
    '''
    return getResult(True, '', None)



def answerPaper(request):
    '''
    提交某个试卷的答案，计算结果并返回
    '''
    return getResult(True, '', None)




def copyPaper(request):
    '''
    根据指定试卷，复制一份试卷包括 考题
    '''
    return getResult(True, '', None)

def doRightPaper(request):
    '''
    生成标准账套
    '''

    return getResult(True,u'结果',None)