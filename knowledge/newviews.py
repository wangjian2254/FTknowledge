#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
import json
from django.http import HttpResponse
from knowledge.models import Rule, Ticket, Relation, Business, KM, KJZD, SF, FL, PZ
from knowledge.tools import getResult
from django.core.cache import cache

__author__ = u'王健'


def getAllTicket(request):
    cachename = 'allticket'
    taxkindstr = cache.get(cachename)
    if taxkindstr:
        return HttpResponse(taxkindstr)
    kindlist = []
    kindidlist = []
    kinddict = {}
    for ticket in Ticket.objects.all().order_by('id'):
        kinddict['%s' % ticket.pk] = {'id': ticket.pk, 'type': 'ticket', 'fatherid': ticket.fatherTicket_id,
                                      'imgs':ticket.getImgs(),  'name': ticket.name, 'desc':ticket.desc, 'children': []}
        kindidlist.append(ticket.pk)
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherid'))]['children'].append(kind)
    for kind in kinddict.values():
        if len(kind['children']) == 0:
            del kind['children']
    return getResult(True, '', kindlist, cachename=cachename)


def saveTicket(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    desc = request.REQUEST.get('desc', '')
    taxkindid = request.REQUEST.get('fatherid', '')
    if id:
        taxTicket = Ticket.objects.get(pk=id)
    else:
        taxTicket = Ticket()
    taxTicket.name = name.strip()
    taxTicket.desc = desc.strip()
    if taxkindid:
        taxTicket.fatherTicket = Ticket.objects.get(pk=taxkindid)
    taxTicket.save()
    cache.delete('allticket')
    return getResult(True, '', taxTicket.pk)


def delTicket(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = Ticket.objects.get(pk=id)
        cache.delete('allticket')
        taxTicket.delete()
    else:
        getResult(False, u'票据不存在', None)

    return getResult(True, '', None)


def getAllBusiness(request):
    cachename = 'allbussiness'
    taxkindstr = cache.get(cachename)
    if taxkindstr:
        return HttpResponse(taxkindstr)
    kindlist = []
    kindidlist = []
    kinddict = {}
    for business in Business.objects.all().order_by('num'):
        kinddict['%s' % business.pk] = {'id': business.pk, 'num': business.num, 'ywbh': business.ywbh(),
                                        'businessname': '[%s] %s' % (business.ywbh(), business.name) , 'type': 'business',
                                        'fatherid': business.fatherBusiness_id,
                                        'name': business.name, 'children': []}
        # pzlist = []
        # for pz in business.pz_set.filter(is_active=True).all():
        #     pzlist.append(pz.pk)
        # kinddict['%s' % business.pk]['pzlist']=pzlist
        kindidlist.append(business.pk)
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherid'))]['children'].append(kind)
    for kind in kinddict.values():
        if len(kind['children']) == 0:
            del kind['children']
    return getResult(True, '', kindlist, cachename=cachename)


def saveBusiness(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    num = request.REQUEST.get('num', '')
    taxkindid = request.REQUEST.get('fatherid', '')
    if id:
        taxTicket = Business.objects.get(pk=id)
    else:
        taxTicket = Business()
    taxTicket.name = name.strip()
    taxTicket.num = num.strip()
    if taxkindid:
        taxTicket.fatherBusiness = Business.objects.get(pk=taxkindid)
    taxTicket.save()
    cache.delete('allbussiness')
    return getResult(True, '', taxTicket.pk)


def delBusiness(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = Business.objects.get(pk=id)
        cache.delete('allbussiness')
        taxTicket.delete()
    else:
        getResult(False, u'票据不存在', None)

    return getResult(True, '', None)


def getAllKM(request):
    cachename = 'allkm'
    taxkindstr = cache.get(cachename)
    if taxkindstr:
        return HttpResponse(taxkindstr)
    kindlist = []
    kindidlist = []
    kinddict = {}
    for km in KM.objects.all().order_by('id'):
        # kinddict['%s' % km.pk] =
        kindlist.append({'id': km.pk, 'type': 'km', 'name': km.name})
    # for kid in kindidlist:
    #     kind = kinddict.get(str(kid))
    #     if not kind.has_key('fatherid'):
    #         kindlist.append(kind)
    #     else:
    #         kinddict[str(kind.get('fatherid'))]['children'].append(kind)
    # for kind in kinddict.values():
    #     if len(kind['children']) == 0:
    #         del kind['children']
    return getResult(True, '', kindlist, cachename=cachename)


def saveKM(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    # taxkindid = request.REQUEST.get('fatherid', '')
    if id:
        taxTicket = KM.objects.get(pk=id)
    else:
        taxTicket = KM()
    taxTicket.name = name.strip()
    # if taxkindid:
    #     taxTicket.fatherKM = KM.objects.get(pk=taxkindid)
    taxTicket.save()
    cache.delete('allkm')
    return getResult(True, '', taxTicket.pk)


def delKM(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = KM.objects.get(pk=id)
        cache.delete('allkm')
        taxTicket.delete()
    else:
        getResult(False, u'票据不存在', None)

    return getResult(True, '', None)


def getRule(request):
    l = []
    for u in Rule.objects.all():
        l.append({'name': u.name, 'id': u.pk})

    return getResult(True, '', l)


def saveRule(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')

    if id:
        rule = Rule.objects.get(pk=id)
    else:
        rule = Rule()
    rule.name = name.strip()

    rule.save()
    return getResult(True, '', rule.pk)


def delRule(request):
    id = request.REQUEST.get('id', '')
    if id:
        rule = Rule.objects.get(pk=id)
        rule.delete()
    else:
        getResult(False, u'行业不存在', None)

    return getResult(True, '', None)


def getTicketByRule(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ids = []
    for t in Relation.objects.filter(rule=ruleid):
        ids.append(t.ticket_id)
    l = []
    for u in Ticket.objects.filter(pk__in=ids):
        l.append({'name': u.name, 'id': u.pk})

    return getResult(True, '', l)


def getBusinessByTicket(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ticketid = request.REQUEST.get('ticketid', '')
    ids = []
    for t in Relation.objects.filter(rule=ruleid, ticket=ticketid):
        ids.append(t.business_id)
    l = []
    for u in Business.objects.filter(pk__in=ids):
        l.append({'name': u.name, 'id': u.pk})
    return getResult(True, '', l)


def getKMByBusiness(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ticketid = request.REQUEST.get('ticketid', '')
    businessid = request.REQUEST.get('businessid', '')
    ids = []
    for t in Relation.objects.filter(rule=ruleid, ticket=ticketid, business=businessid):
        ids.append(t.km_id)
    l = []
    for u in KM.objects.filter(pk__in=ids):
        l.append({'name': u.name, 'id': u.pk})

    return getResult(True, '', l)


def getKJZDByKM(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ticketid = request.REQUEST.get('ticketid', '')
    businessid = request.REQUEST.get('businessid', '')


    if Relation.objects.filter(rule=ruleid, ticket=ticketid, business=businessid).count() != 0:
        r = Relation.objects.get(rule=ruleid, ticket=ticketid, business=businessid)
        kjzdlist = []
        sflist = []
        # pzlist = []
        for kjzd in r.kjzds.all():
            kjzdlist.append(kjzd.name)
        for sf in r.sf.all():
            sflist.append(sf.name)
        # for pz in r.pz_set.all():
        #     pzlist.append(pz.pk)
        return getResult(True, '', {'kjzd': '\n'.join(kjzdlist), 'sf': '\n'.join(sflist), 'id':r.pk})
    else:
        return getResult(True, '', {'kjzd': '', 'sf': ''})


def saveRelation(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ticketid = request.REQUEST.get('ticketid', '')
    businessid = request.REQUEST.get('businessid', '')
    kjzdstr = request.REQUEST.get('kjzd', '')
    sfstr = request.REQUEST.get('sf', '')
    if Relation.objects.filter(rule=ruleid, ticket=ticketid, business=businessid).count() != 0:
        r = Relation.objects.get(rule=ruleid, ticket=ticketid, business=businessid)
        kjzdlist = []
        sflist = []

        for kjzd in r.kjzds.all():
            kjzd.name=kjzdstr
            kjzd.save()
        if r.kjzds.count()==0:
            kjzd = KJZD()
            kjzd.name = kjzdstr
            kjzd.save()
            r.kjzds.add(kjzd)
            r.save()
        for sf in r.sf.all():
            sf.name=sfstr
            sf.save()
        if r.sf.count()==0:
            sf = SF()
            sf.name = sfstr
            sf.save()
            r.sf.add(sf)
            r.save()
        return getResult(True, u'修改成功',r.pk)
    else:
        r = Relation()
        r.rule = Rule.objects.get(pk=ruleid)

        r.ticket = Ticket.objects.get(pk=ticketid)
        r.business = Business.objects.get(pk=businessid)
        r.save()

        kjzd = KJZD()
        kjzd.name = kjzdstr
        kjzd.save()
        r.kjzds.add(kjzd)

        sf = SF()
        sf.name = sfstr
        sf.save()
        r.sf.add(sf)
        r.save()

        return getResult(True, u'保存成功',r.pk)

def delRelation(request):
    ruleid = request.REQUEST.get('ruleid', '')
    ticketid = request.REQUEST.get('ticketid', '')
    businessid = request.REQUEST.get('businessid', '')
    kjzdstr = request.REQUEST.get('kjzd', '')
    sfstr = request.REQUEST.get('sf', '')
    if Relation.objects.filter(rule=ruleid, ticket=ticketid, business=businessid).count() != 0:
        r = Relation.objects.get(rule=ruleid, ticket=ticketid, business=businessid)
        r.delete()
        return getResult(True, u'删除成功')
    else:


        return getResult(True, u'关系不存在')

def ticketFather(ticket,ticketdict,ticketlist):
    ticketdict['%s' % ticket.pk] = {'id': ticket.pk, 'type': 'ticket', 'fatherid': ticket.fatherTicket_id,
                                      'imgs':ticket.getImgs(),  'name': ticket.name, 'desc':ticket.desc, 'children': []}
    ticketlist.add(ticket.pk)
    if ticket.fatherTicket:
        ticketFather(ticket.fatherTicket,ticketdict,ticketlist)

def getTicketByUserRule(request):
    ruleid = request.REQUEST.get('ruleid','')
    if not ruleid:
        return getResult(True,'',[])
    kindlist = []
    kindidlist = set()
    kinddict = {}
    tids = set()
    for r in Relation.objects.filter(rule=ruleid).order_by('id'):
        tids.add(r.ticket_id)
    for ticket in Ticket.objects.filter(id__in=tids).order_by('id'):
        ticketFather(ticket, kinddict, kindidlist)
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherid'))]['children'].append(kind)
    for kind in kinddict.values():
        if len(kind['children']) == 0:
            del kind['children']
    l=[]
    for k in kinddict.values():
        if not hasattr(k,'children'):
            l.append(k)
    return getResult(True, '', {"kindlist":kindlist,"kindalllist":l})



def businessFather(business,bussinessdict,businesslist):

    bussinessdict['%s' % business.pk] = {'id': business.pk, 'num': business.num, 'ywbh': business.ywbh(), 'businessText':business.name,
                                        'businessname': '[%s] %s' % (business.ywbh(), business.name) , 'type': 'business',
                                        'fatherid': business.fatherBusiness_id,
                                        'name': business.name, 'children': []}
    businesslist.add(business.pk)
    if business.fatherBusiness:
        businessFather(business.fatherBusiness,bussinessdict,businesslist)

def getBusinessByUserRule(request):
    ruleid = request.REQUEST.get('ruleid','')
    ticketid = request.REQUEST.get('ticketid','')
    if not ruleid:
        return getResult(True,'',[])
    kindlist = []
    kindidlist = set()
    kinddict = {}
    tids = set()
    for r in Relation.objects.filter(rule=ruleid,ticket=ticketid).order_by('id'):
        tids.add(r.business_id)
    for business in Business.objects.filter(pk__in=tids).order_by('id'):
        businessFather(business,kinddict,kindidlist)
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherid'))]['children'].append(kind)
    for kind in kinddict.values():
        if len(kind['children']) == 0:
            del kind['children']
    return getResult(True, '', kindlist)

def getPZbyBusiness(request):
    bid = request.REQUEST.get('bid')
    pzlist = []
    for pz in PZ.objects.filter(business=bid):
        pzlist.append(pz.pk)
    return getResult(True,'',pzlist)

def getPZ(request):
    pzid = request.REQUEST.get('pzid','')
    result = {'fllist':[],'pzdesc':''}
    if pzid:
        fllist=[]
        for fl in FL.objects.filter(pz=pzid).order_by('id'):
            f={'kjkm':fl.kmmc_id, 'fx':fl.fx, 'id':fl.pk, 'zy':fl.zy}
            if fl.fx:
                f['jje'] = str(fl.num)
                if not fl.num:
                    f['jje']=0
            else:
                f['dje'] = str(fl.num)
                if not fl.num:
                    f['dje']=0
            fllist.append(f)
        result['fllist']=fllist
        pz=PZ.objects.get(pk=pzid)
        result['pzdesc']= pz.desc
        # result['imgurl']= pz.getImg()
        return getResult(True,'',result)
    else:
        return getResult(True,'',result)

def savePZ(request):
    cache.delete('allbussiness')
    bid = request.REQUEST.get('bid','')
    pzid = request.REQUEST.get('pzid','')
    fl = request.REQUEST.get('fl','')
    fllist = json.loads(fl)
    if bid:
        if pzid:
            if len(fllist)==0:
                FL.objects.filter(pz=PZ.objects.get(pk=pzid)).delete()
                PZ.objects.get(pk=pzid).delete()
                return getResult(True,'')
            else:
                pz = PZ.objects.get(pk=pzid)
        else:
            pz = PZ()
            pz.business = Business.objects.get(pk=bid)
            pz.user = request.user
            pz.save()
        pz.desc = request.REQUEST.get('desc','')
        pz.save()

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
        return getResult(True,'',{'pzid':pz.pk,'bid':pz.business_id})
