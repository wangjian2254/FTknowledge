#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.http import HttpResponse
from util.tools import getResult
from taxcreate.models import TaxTemplate, TaxRule, RuleItem

__author__ = u'王健'


def taxTemplateUploaded(request):
    img = request.FILES.get('file','')
    name = request.REQUEST.get('name','')
    if img:
        imginfo=TaxTemplate()
        imginfo.img = img
        imginfo.name = name

        imginfo.save()

        return getResult(True,u'上传成功',{'imgurl':imginfo.img.url,'id':imginfo.pk,'name':imginfo.name})
    else:
        return getResult(False,'',None)

def saveRule(request):
    templateid = request.REQUEST.get('templateid','')
    name = request.REQUEST.get('name','')
    id = request.REQUEST.get('id','')
    if id:
        rule = TaxRule.objects.get(pk=id)
    else:
        rule = TaxRule()
    rule.name = name
    rule.taxtemplate = TaxTemplate.objects.get(pk=templateid)
    rule.save()
    return getResult(True,u'保存规则成功',{'id':rule.pk,'templateid':rule.taxtemplate_id,'name':rule.name})


def saveTemplate(request):
    name = request.REQUEST.get('name','')
    id = request.REQUEST.get('id','')
    if id:
        rule = TaxTemplate.objects.get(pk=id)
    else:
        rule = TaxTemplate()
    rule.name = name
    rule.save()
    return getResult(True,u'保存规则成功',{'id':rule.pk,'name':rule.name})


def saveRuleItem(request):
    ruleid = request.REQUEST.get('ruleid','')
    if ruleid:
        rule = TaxRule.objects.get(pk=ruleid)
        ids =[]
        for i in range(int(request.REQUEST.get('num',0))):
            id = request.REQUEST.get('id%s'%i)
            index = request.REQUEST.get('index%s'%i)
            x = request.REQUEST.get('x%s'%i)
            y = request.REQUEST.get('y%s'%i)
            size = request.REQUEST.get('size%s'%i)
            color = request.REQUEST.get('color%s'%i)
            family = request.REQUEST.get('family%s'%i)
            word = request.REQUEST.get('word%s'%i)
            if id:
                ruleitem = RuleItem.objects.get(pk=id)
            else:
                ruleitem = RuleItem()
            ruleitem.rule=rule
            ruleitem.index = int(index)
            ruleitem.x = int(x)
            ruleitem.y = int(y)
            ruleitem.size = int(size)
            ruleitem.color = int(color)
            ruleitem.family = int(family)
            ruleitem.word = word
            ruleitem.save()
            ids.append(ruleitem.pk)


        return getResult(True,u'保存规则成功',{'ids':ids})
    return getResult(False,u'保存失败，请提供规则id')


def getTemplateList(request):
    l=[]
    for t in TaxTemplate.objects.all().order_by('id'):
        l.append({'id':t.pk,'name':t.name,'imgurl':t.img.url})
    return getResult(True,u'获取模板成功',l)

def getRuleByTemplateList(request):
    tempid = request.REQUEST.get('templateid','')
    l=[]
    for t in TaxRule.objects.filter(taxtemplate=tempid).order_by('id'):
        l.append({'id':t.pk,'templateid':t.taxtemplate_id,'name':t.name})
    return getResult(True,u'获取规则成功',l)

def getRuleItemByRuleList(request):
    tempid = request.REQUEST.get('ruleid','')
    l=[]
    for t in RuleItem.objects.filter(rule=tempid).order_by('index'):
        l.append({'id':t.pk,'ruleid':t.rule_id,'index':t.index,'x':t.x,'y':t.y,'size':t.size,'color':t.color,'family':t.family,'word':t.word})

    return getResult(True,u'获取规则细则成功',l)

def showTaxImage(request):
    from PIL import Image,ImageDraw,ImageFont
    ruleid = request.REQUEST.get('ruleid','')
    if ruleid:
        rule = TaxRule.objects.get(pk=ruleid)
        temp = rule.taxtemplate
        tempimg = Image.open(temp.img.path)
        d = ImageDraw.Draw(tempimg)
        for r in RuleItem.objects.filter(rule=rule).order_by('index'):
            font = ImageFont.truetype('msyh.ttf',r.size)
            c =('%06x'%r.color)
            cr = int(c[-6:-4],16)
            cg = int(c[-4:-2],16)
            cb = int(c[-2:],16)
            d.text((r.x,r.y),r.word,(cr,cg,cb),font=font)
        response = HttpResponse(mimetype="image/jpg")
        tempimg.save(response, "JPEG")
        return response
    return HttpResponse('', mimetype="image/jpg")