#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.http import HttpResponse
from knowledge.models import Rule, Ticket, Relation, Business, KM
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
                                      'imgs':ticket.getImgs(),  'name': ticket.name, 'children': []}
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
    taxkindid = request.REQUEST.get('fatherid', '')
    if id:
        taxTicket = Ticket.objects.get(pk=id)
    else:
        taxTicket = Ticket()
    taxTicket.name = name.strip()
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
    for business in Business.objects.all().order_by('id'):
        kinddict['%s' % business.pk] = {'id': business.pk, 'num': business.num, 'ywbh': business.ywbh(),
                                        'businessname': '[%s] %s' % (business.ywbh(), business.name) , 'type': 'business',
                                        'fatherid': business.fatherBusiness_id,
                                        'name': business.name, 'children': []}
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
        kinddict['%s' % km.pk] = {'id': km.pk, 'type': 'km', 'fatherid': km.fatherKM_id,
                                  'name': km.name, 'children': []}
        kindidlist.append(km.pk)
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


def saveKM(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    taxkindid = request.REQUEST.get('fatherid', '')
    if id:
        taxTicket = KM.objects.get(pk=id)
    else:
        taxTicket = KM()
    taxTicket.name = name.strip()
    if taxkindid:
        taxTicket.fatherKM = KM.objects.get(pk=taxkindid)
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
    kjkmid = request.REQUEST.get('kjkmid', '')

    if Relation.objects.filter(rule=ruleid, ticket=ticketid, business=businessid, km=kjkmid).count() != 0:
        r = Relation.objects.get(rule=ruleid, ticket=ticketid, business=businessid, km=kjkmid)
        kjzdlist = []
        sflist = []

        for kjzd in r.kjzds.all():
            kjzdlist.append(kjzd.name)
        for sf in r.sf.all():
            sflist.append(sf.name)
        return getResult(True, '', {'kjzd': '\n'.join(kjzdlist), 'sf': '\n'.join(sflist)})
    else:
        return getResult(True, '', {'kjzd': '无', 'sf': '无'})