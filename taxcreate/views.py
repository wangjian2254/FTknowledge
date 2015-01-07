# coding=utf-8
# Date: 11-12-8
#Time: 下午10:28
from django.http import HttpResponse
from FTknowledge.settings import STATIC_ROOT
from util.tools import getResult
from taxcreate.models import TaxTemplate, TaxRule, RuleItem, TaxTuZhang, Subject, Guan, Paper

__author__ = u'王健'


def taxTuZhangUploaded(request):
    img = request.FILES.get('file', '')
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    if img:
        if id:
            imginfo = TaxTuZhang.objects.get(pk=id)
        else:
            imginfo = TaxTuZhang()
        if imginfo.img:
            imginfo.img.delete()
        imginfo.img = img
        imginfo.name = name
        imginfo.save()

        return getResult(True, u'上传成功', {'imgurl': imginfo.img.url, 'id': imginfo.pk, 'name': imginfo.name})
    else:
        return getResult(False, '', None)


def deleteTuZhang(request):
    if not request.user.is_staff:
        return getResult(False, u'权限不足', None)
    id = request.REQUEST.get('tuzhangid')
    try:
        if not TaxTuZhang.objects.filter(pk=id).exists():
            raise 'err'
        t = TaxTuZhang.objects.get(pk=id)
        if not t.ruleitem_set.exists():
            if t.img:
                t.img.delete()
            t.delete()
            return getResult(True, u'删除成功', None)
        else:
            raise 'err'
    except Exception, e:
        return getResult(False, u'模板被使用，无法删除', None)


def getTuZhangList(request):
    l = []
    for t in TaxTuZhang.objects.all().order_by('id'):
        if t.img:
            l.append({'id': t.pk, 'name': t.name, 'imgurl': t.img.url})
    return getResult(True, u'获取图章模板成功', l)


def saveTuZhang(request):
    name = request.REQUEST.get('name', '')
    id = request.REQUEST.get('id', '')
    if id:
        rule = TaxTuZhang.objects.get(pk=id)
    else:
        if TaxTuZhang.objects.filter(name=name).count() > 0:
            return getResult(False, u'图章模板名称不能重复', None)
        rule = TaxTuZhang()
    rule.name = name
    rule.save()
    return getResult(True, u'保存图章模板成功', {'id': rule.pk, 'name': rule.name})


def taxTemplateUploaded(request):
    img = request.FILES.get('file', '')
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    if img:
        if id:
            imginfo = TaxTemplate.objects.get(pk=id)
        else:
            imginfo = TaxTemplate()
        if imginfo.img:
            imginfo.img.delete()
        imginfo.img = img
        imginfo.name = name
        imginfo.save()

        return getResult(True, u'上传成功', {'imgurl': imginfo.img.url, 'id': imginfo.pk, 'name': imginfo.name})
    else:
        return getResult(False, '', None)


def deleteTemplate(request):
    if not request.user.is_staff:
        return getResult(False, u'权限不足', None)
    id = request.REQUEST.get('templateid')
    t = TaxTemplate.objects.get(pk=id)
    try:
        if not t.taxrule_set.exists():
            if t.img:
                t.img.delete()
            t.delete()
            return getResult(True, u'删除成功', None)
        else:
            raise 'error'
    except Exception, e:
        return getResult(False, u'模板被使用，无法删除', None)


def saveRule(request):
    templateid = request.REQUEST.get('templateid', '')
    name = request.REQUEST.get('name', '')
    id = request.REQUEST.get('id', '')
    if id:
        rule = TaxRule.objects.get(pk=id)
    else:
        rule = TaxRule()
    rule.name = name
    rule.taxtemplate = TaxTemplate.objects.get(pk=templateid)
    rule.save()
    return getResult(True, u'保存规则成功', {'id': rule.pk, 'templateid': rule.taxtemplate_id, 'name': rule.name})


def deleteRule(request):
    ruleid = request.REQUEST.get('ruleid')
    rule = TaxRule.objects.get(pk=ruleid)
    try:
        if not rule.subject_set.exists():
            rule.delete()
            return getResult(True, u'删除成功', None)
        else:
            raise 'error'

    except Exception, e:
        return getResult(False, u'规则被使用，无法删除', None)


def saveTemplate(request):
    name = request.REQUEST.get('name', '')
    id = request.REQUEST.get('id', '')
    if id:
        rule = TaxTemplate.objects.get(pk=id)
    else:
        if TaxTemplate.objects.filter(name=name).count() > 0:
            return getResult(False, u'票据模板名称不能重复', None)
        rule = TaxTemplate()
    rule.name = name
    rule.save()
    return getResult(True, u'保存票据模板成功', {'id': rule.pk, 'name': rule.name})


def saveRuleItem(request):
    ruleid = request.REQUEST.get('ruleid', '')
    if ruleid:
        rule = TaxRule.objects.get(pk=ruleid)
        ids = []
        for i in range(int(request.REQUEST.get('num', 0))):
            id = request.REQUEST.get('id%s' % i)
            index = request.REQUEST.get('index%s' % i)
            x = request.REQUEST.get('x%s' % i)
            y = request.REQUEST.get('y%s' % i)
            size = request.REQUEST.get('size%s' % i)
            color = request.REQUEST.get('color%s' % i)
            family = request.REQUEST.get('family%s' % i)
            word = request.REQUEST.get('word%s' % i)
            tuzhang_id = request.REQUEST.get('tuzhang%s' % i)
            if id:
                ruleitem = RuleItem.objects.get(pk=id)
            else:
                ruleitem = RuleItem()
            if tuzhang_id:
                ruleitem.size = 0
                ruleitem.family = 1
                tuzhang = TaxTuZhang.objects.get(pk=tuzhang_id)
                ruleitem.tuzhang = tuzhang
            else:
                ruleitem.tuzhang = None
                ruleitem.size = int(size)
                ruleitem.family = int(family)
            ruleitem.rule = rule
            ruleitem.index = int(index)
            ruleitem.x = int(x)
            ruleitem.y = int(y)

            ruleitem.color = int(color)

            ruleitem.word = word
            ruleitem.save()
            ids.append(ruleitem.pk)

        return getResult(True, u'保存规则成功', {'ids': ids})
    return getResult(False, u'保存失败，请提供规则id')


def copyRuleItem(request):
    ruleid = request.REQUEST.get('ruleid', '')
    if ruleid:
        rule = TaxRule.objects.get(pk=ruleid)
        newrule = TaxRule()
        newrule.name = u'复制_%s' % rule.name
        newrule.taxtemplate = rule.taxtemplate
        newrule.save()
        for ruleitem in rule.ruleitem_set.all():
            ri = RuleItem()
            ri.rule = newrule
            ri.tuzhang = ruleitem.tuzhang
            ri.index = ruleitem.index
            ri.x = ruleitem.x
            ri.y = ruleitem.y
            ri.size = ruleitem.size
            ri.color = ruleitem.color
            ri.family = ruleitem.family
            ri.word = ruleitem.word
            ri.save()
        return getResult(True, u'复制规则成功', None)
    return getResult(False, u'复制失败，请提供规则id')


def getTemplateList(request):
    l = []
    for t in TaxTemplate.objects.all().order_by('id'):
        l.append({'id': t.pk, 'name': t.name, 'imgurl': t.img.url})
    return getResult(True, u'获取模板成功', l)


def getRuleByTemplateList(request):
    tempid = request.REQUEST.get('templateid', '')
    l = []
    for t in TaxRule.objects.filter(taxtemplate=tempid).order_by('id'):
        l.append({'id': t.pk, 'templateid': t.taxtemplate_id, 'name': t.name})
    return getResult(True, u'获取规则成功', l)


def getRuleItemByRuleList(request):
    tempid = request.REQUEST.get('ruleid', '')
    l = []
    for t in RuleItem.objects.filter(rule=tempid).order_by('index'):
        l.append(
            {'id': t.pk, 'ruleid': t.rule_id, 'index': t.index, 'x': t.x, 'y': t.y, 'size': t.size, 'color': t.color,
             'family': t.family, 'word': t.word, 'tuzhang': t.tuzhang_id})

    return getResult(True, u'获取规则细则成功', l)


def delRuleItemByids(request):
    ruleitemids = request.REQUEST.getlist('ruleitemids')
    RuleItem.objects.filter(pk__in=ruleitemids).delete()

    return getResult(True, u'删除成功', ruleitemids)


def showTaxImage(request):
    from PIL import Image, ImageDraw, ImageFont

    ruleid = request.REQUEST.get('ruleid', '')
    flag = request.REQUEST.get('flag', '0')
    rule = TaxRule.objects.get(pk=ruleid)
    temp = rule.taxtemplate
    tempimg = Image.open(temp.img.path)
    d = ImageDraw.Draw(tempimg)
    if flag == '1':
        w, h = tempimg.size
        f = ImageFont.truetype('msyh.ttf', 15)
        for x in range(50, w, 50):
            d.line([(x, 0), (x, h)], 0, 2)
            d.text((x, 0), '%s' % x, (0, 0, 0), font=f)
        for y in range(50, h, 50):
            d.line([(0, y), (w, y)], 0, 2)
            d.text((0, y), '%s' % y, (0, 0, 0), font=f)

    for r in RuleItem.objects.filter(rule=rule).order_by('index'):
        if not r.tuzhang:
            font = ImageFont.truetype('%smsyh.ttf' % STATIC_ROOT, r.size)
            c = ('%06x' % r.color)
            cr = int(c[-6:-4], 16)
            cg = int(c[-4:-2], 16)
            cb = int(c[-2:], 16)
            d.text((r.x, r.y), r.word, (cr, cg, cb), font=font)
        else:
            mark_img = Image.open(r.tuzhang.img.path)
            tempimg.paste(mark_img, (r.x, r.y), mark_img.convert('RGBA'))
    response = HttpResponse(mimetype="image/jpg")
    tempimg.save(response, "JPEG")
    return response


def tongji_tax(request):
    subjectcount = Subject.objects.filter(type=1).count()
    pzsubjectcount = Subject.objects.filter(type=2).count()
    templatecount = TaxTemplate.objects.count()
    rulecount = TaxRule.objects.count()
    tuzhangcount = TaxTuZhang.objects.count()

    guancount = Guan.objects.count()
    papercount = Paper.objects.count()

    return HttpResponse(u'选择题试题数量：%s<br/>凭证题试题数量：%s<br/>所有试题数量：%s<br/>关卡数量：%s<br/>试卷数量：%s<br/>票据模板数量：%s<br/>规则数量：%s<br/>图章数量：%s<br/>' % (
        subjectcount, pzsubjectcount, subjectcount + pzsubjectcount, guancount, papercount, templatecount, rulecount, tuzhangcount))
