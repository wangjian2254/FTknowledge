#coding=utf-8
# Create your views here.
import datetime
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import Q
from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import render_to_response
from tools import getResult, clearTicketCache
from models import Group, TaxKind, TaxTicket, BBField, BB, KJKMTicket, KJKM, BBFieldValue


def index(request):
    url = 'http://' + request.META['HTTP_HOST'] + '/static/swf/'
    return render_to_response('index.html', {'url': url, 'p': datetime.datetime.now()})


def menu(request):
    '''
     <menuitem label='分类管理' mod='taxkind'></menuitem>
				    <menuitem label='报表管理' mod='bbedit'></menuitem>

				    <menuitem label='知识库编辑' mod='knowledgeedit'></menuitem>
				    <menuitem label='知识库查询' mod='knowledgequery'></menuitem>
    '''
    if request.user.is_staff:
        menuxml = '''
        <?xml version='1.0' encoding='utf-8'?>
                <root>
                    <menu mod='myMenu1' label='基础管理'>

                        <menuitem label='票据管理' mod='ticketedit'></menuitem>
                        <menuitem label='业务管理' mod='businessedit'></menuitem>

                        <menuitem label='用户管理' mod='people'></menuitem>

                    </menu>
                    <menu mod='myMenu2' label='知识库'>

                        <menuitem label='查询' mod='autokjquery'></menuitem>
                        <menuitem label='定义' mod='autokjedit'></menuitem>

                    </menu>

                    <menu mod='myMenu3' label='票据生成'>

                        <menuitem label='票据定义' mod='taximagecreate'></menuitem>

                    </menu>

                </root>
        '''
    else:
        menuxml = '''
        <?xml version='1.0' encoding='utf-8'?>
                <root>
                    <menu mod='myMenu2' label='知识库'>
                        <menuitem label='查询' mod='autokjquery'></menuitem>
                    </menu>

                </root>
        '''
    return HttpResponse(menuxml)


def logout(request):
    auth_logout(request)
    return getResult(True, '')


def login(request):
    username = request.REQUEST.get('username')
    if username:
        userlist = User.objects.filter(username=username)[:1]
        if len(userlist) > 0:
            user = userlist[0]
            if not user.is_active:
                return getResult(False, u'用户已经停止使用。')
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():


        # Okay, security checks complete. Log the user in.
        auth_login(request, form.get_user())

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        return getResult(True, u'登录成功')
    else:
        return getResult(False, u'用户名密码错误')


def regUser(request):
    result = saveUser(request)
    if result.get('success'):
        auth_login(request, User.objects.get(pk=result.get('result').get('pk')))

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return getResult(True, '', None)
    else:
        return getResult(False, '注册失败', None)


def saveUser(request):
    id = request.REQUEST.get('id', '')
    if id:
        user = User.objects.get(pk=id)
    else:
        user = User()
        user.set_password('111111')
        user.username = request.REQUEST.get('username', '')
        if not user.username or User.objects.filter(username=user.username).count() > 0:
            return getResult(False, u'用户名已经存在', None)
    is_active = request.REQUEST.get('isaction', '')
    if is_active:
        if is_active == 'true':
            user.is_active = True
        else:
            user.is_active = False
    is_staff = request.REQUEST.get('ismanager', '')
    if is_staff:
        if is_staff == 'true':
            user.is_staff = True
        else:
            user.is_staff = False
    user.first_name = request.REQUEST.get('truename', u'游客')
    if request.REQUEST.has_key('password'):
        user.set_password(request.REQUEST.get('password'))
    user.save()
    return getResult(True, '', {'username': user.username, 'truename': user.first_name, 'ismanager': user.is_staff,
                                'isaction': user.is_active, 'id': user.pk})


def allmanager(request):
    uq = User.objects.filter(is_staff=True).filter(is_active=True)
    l = []
    for u in uq:
        l.append({'username': u.username, 'truename': u.first_name, 'ismanager': u.is_staff, 'isaction': u.is_active,
                  'id': u.pk})

    return getResult(True, '', l)


def currentUser(request):
    if isinstance(request.user, AnonymousUser):
        return getResult(True, '', None)
    else:
        return getResult(True, '', {'username': request.user.username, 'truename': request.user.first_name,
                                    'ismanager': request.user.is_staff, 'isaction': request.user.is_active,
                                    'id': request.user.pk})


def getHyList(request):
    l = []
    for g in Group.objects.filter(is_active=True).order_by('id'):
        l.append({'id': g.pk, 'name': g.name})
    return getResult(True, '', l)


def getTaxKind(request):
    group = request.REQUEST.get('groupid', '')
    cachename = 'taxkindstr%s' % group
    taxkindstr = cache.get(cachename)
    if taxkindstr:
        return HttpResponse(taxkindstr)
    groupquery = Group.objects.filter(is_active=True)
    if group:
        groupquery = groupquery.filter(pk=group)

    kindlist = []
    kindidlist = []
    kinddict = {}

    kjkmdict = {}
    for kjkm in KJKMTicket.objects.all():
        if not kjkmdict.has_key(str(kjkm.tickets_id)):
            kjkmdict[str(kjkm.tickets_id)] = []
        kjkmdict[str(kjkm.tickets_id)].append(
            {'type': 'kjkm', 'name': kjkm.kjkm.name, 'id': kjkm.pk, 'kjkmid': kjkm.kjkm_id,
             'ticketid': kjkm.tickets_id})
    for kind in TaxKind.objects.all().order_by('id'):
        kinddict['%s' % kind.pk] = {'id': kind.pk, 'type': 'kind', 'fatherKindid': kind.fatherKind_id,
                                    'name': kind.name, 'is_active': kind.is_active, 'children': []}
        kindidlist.append(kind.pk)
    kind = None
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherKindid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherKindid'))]['children'].append(kind)
    for ticket in TaxTicket.objects.filter(group__in=groupquery).order_by('id'):
        tdict = {'name': ticket.name, 'id': ticket.pk, 'type': 'ticket', 'fatherKindid': ticket.taxkind_id}
        if kjkmdict.has_key(str(ticket.id)):
            tdict['children'] = kjkmdict[str(ticket.id)]
        kinddict['%s' % ticket.taxkind_id]['children'].append(tdict)
    for kind in kinddict.values():
        if len(kind['children']) == 0:
            del kind['children']
    return getResult(True, '', kindlist, cachename=cachename)


def saveTaxKind(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    kindFatherId = request.REQUEST.get('kindFatherId', '')
    is_active = request.REQUEST.get('is_active', '')

    if id:
        taxKind = TaxKind.objects.get(pk=id)
    else:
        taxKind = TaxKind()
    taxKind.name = name.strip()
    if kindFatherId:
        taxKind.fatherKind = TaxKind.objects.get(pk=kindFatherId)
    if is_active == 'true':
        taxKind.is_active = True
    else:
        taxKind.is_active = False
    taxKind.save()
    clearTicketCache()
    return getResult(True, '', taxKind.pk)


def saveTaxTicket(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    taxkindid = request.REQUEST.get('taxkindid', '')
    groupid = request.REQUEST.get('groupid', '')

    if id:
        taxTicket = TaxTicket.objects.get(pk=id)
    else:
        if 0 < TaxTicket.objects.filter(taxkind=taxkindid, group=groupid, name=name).count():
            return getResult(False, u'票据已经存在', None)
        taxTicket = TaxTicket()
    taxTicket.name = name.strip()
    if taxkindid:
        taxTicket.taxkind = TaxKind.objects.get(pk=taxkindid)
    if groupid:
        taxTicket.group = Group.objects.get(pk=groupid)
    taxTicket.save()
    clearTicketCache(groupid)
    return getResult(True, '', taxTicket.pk)


def delTaxTicket(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = TaxTicket.objects.get(pk=id)
        clearTicketCache(taxTicket.group_id)
        taxTicket.delete()
    else:
        getResult(False, u'票据不存在', None)

    return getResult(True, '', None)


def getBB(request):
    bblist = []
    for bb in BB.objects.all().order_by('id'):
        bd = {'children': [], 'id': bb.pk, 'name': bb.name, 'type': 'bb'}
        bblist.append(bd)

        for field in BBField.objects.filter(bb=bb).order_by('id'):
            bd['children'].append({'id': field.pk, 'name': field.fieldname, 'type': 'field'})
    return getResult(True, '', bblist)


def saveBB(request):
    id = request.REQUEST.get('id', '')
    name = request.REQUEST.get('name', '')
    if id:
        bb = BB.objects.get(pk=id)
    else:
        bb = BB()
    bb.name = name
    bb.save()
    return getResult(True, '', bb.pk)


def delBB(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = BB.objects.get(pk=id)
        taxTicket.delete()
    else:
        getResult(False, u'报表不存在', None)

    return getResult(True, '', None)


def saveBBField(request):
    id = request.REQUEST.get('id', '')
    bbid = request.REQUEST.get('bbid', '')
    name = request.REQUEST.get('name', '')
    if id:
        bbf = BBField.objects.get(pk=id)
    else:
        bbf = BBField()
    bbf.bb = BB.objects.get(pk=bbid)
    bbf.fieldname = name
    bbf.save()
    return getResult(True, '', bbf.pk)


def delBBField(request):
    id = request.REQUEST.get('id', '')
    if id:
        taxTicket = BBField.objects.get(pk=id)
        taxTicket.delete()
    else:
        getResult(False, u'报表字段不存在', None)

    return getResult(True, '', None)


def getKJKM(request):
    cachename = 'kjkmstr'
    jsontr = cache.get(cachename)
    if jsontr:
        return HttpResponse(jsontr)
    l = []
    for kjkm in KJKM.objects.all().order_by('name'):
        l.append({'name': kjkm.name, 'id': kjkm.pk})
    return getResult(True, '', l, cachename=cachename)


def getKJKMbyTicket(request):
    ticketid = request.REQUEST.get('ticketid','')
    l = []
    for kjkm in KJKMTicket.objects.filter(tickets_id=ticketid).order_by('kjkm'):
        l.append({'name': kjkm.kjkm.name, 'id': kjkm.kjkm_id})
    return getResult(True, '', l)


def saveKJKM(request):
    name = request.REQUEST.get("kjkm","")
    if name and KJKM.objects.filter(name = name).count()==0:
        kjkm = KJKM()
        kjkm.name = name
        kjkm.save()
        return getResult(True,'',kjkm.pk)
    return getResult(False,u'会计科目已存在')


def saveKJKMByTicket(request):
    ticketid = request.REQUEST.get('ticketid','')
    kjkmids = request.REQUEST.get("kjkms","").split(',')
    kjkmids.remove('')

    if ticketid:
        ticket = TaxTicket.objects.get(pk = ticketid)
        KJKMTicket.objects.filter(tickets=ticket).exclude(kjkm__in=kjkmids).delete()
        clearTicketCache(ticket.group_id)
        for kjkm in  KJKM.objects.filter(pk__in=kjkmids):
            if KJKMTicket.objects.filter(tickets=ticket,kjkm=kjkm).count()==0:
                kt=KJKMTicket()
                kt.tickets =ticket
                kt.kjkm = kjkm
                kt.save()
        return getResult(True,'',kjkm.pk)
    return getResult(False,u'会计科目已存在')

def getBBFieldValuebyTicketKjkm(request):
    kjkmticketid = request.REQUEST.get('id','')
    if kjkmticketid:
        o ={'kjkmticketid':kjkmticketid}
        for v in BBFieldValue.objects.filter(kjkmticket=kjkmticketid):
            o['%s'%v.bbfield_id]=v.value

        return getResult(True,'',o)
    return getResult(False,u'请选择一个会计科目')

def saveBBFieldValuebyTicketKjkm(request):
    kjkmticketid = request.REQUEST.get('kjkmticketid','')
    if kjkmticketid:
        kjkmticket = KJKMTicket.objects.get(pk=kjkmticketid)
        datafield = request.REQUEST.getlist('datafield')
        BBFieldValue.objects.filter(kjkmticket=kjkmticketid).exclude(bbfield__in=datafield).delete()
        # for fieldvalue in BBFieldValue.objects.filter(kjkmticket=kjkmticketid,bbfield__in=datafield):
        for fieldname in datafield:
            v = request.REQUEST.get(fieldname)
            if BBFieldValue.objects.filter(kjkmticket=kjkmticketid,bbfield=fieldname).count()==0:
                fieldvalue = BBFieldValue()
                fieldvalue.bbfield = BBField.objects.get(pk=fieldname)
                fieldvalue.kjkmticket = kjkmticket
            else:
                fieldvalue = BBFieldValue.objects.get(kjkmticket=kjkmticketid,bbfield=fieldname)
                if not v:
                    v.delete()
            if v:
                fieldvalue.value = request.REQUEST.get(fieldname)
                fieldvalue.save()
        return getResult(True,'')

    return getResult(False,u'请选择一个会计科目')


def queryKnowledge(request):
    hy = request.REQUEST.get('hy','')
    key = request.REQUEST.get('key','')
    kind = request.REQUEST.get('kind','')
    ticket = request.REQUEST.get('ticket','')
    kjkm = request.REQUEST.get('kjkm','')
    keyQ =None
    keyNameQ =None
    if key:
        for k in key.split(' '):
            if keyQ:
                keyQ = Q(value__contains=k)&keyQ
                keyNameQ = Q(name__contains=k)&keyNameQ
            else:
                keyQ = Q(value__contains=k)
                keyNameQ = Q(name__contains=k)
    ticketquery = TaxTicket.objects.all()

    #第一种情况 模糊查询：
    if not kind and not ticket and not kjkm:
        kindquery = TaxKind.objects.filter(is_active=True).filter(keyNameQ)
        ticketquery = ticketquery.filter( Q(taxkind__in=kindquery)|keyNameQ)
        kjkmquery = KJKM.objects.filter(keyNameQ)
        kjkmticketyquery = KJKMTicket.objects.filter(Q(kjkm__in=kjkmquery)|Q(tickets__in=ticketquery))

    else:
        #第二种情况 高级模糊查询
        if kind:
            kindquery = TaxKind.objects.filter(is_active=True).filter(name__contains=kind)
        else:
            kindquery = TaxKind.objects.filter(is_active=True).filter(keyNameQ)
        if ticket:
            ticketquery = ticketquery.filter(Q(taxkind__in=kindquery)|Q(name__contains=ticket))
        else:
            ticketquery = ticketquery.filter( Q(taxkind__in=kindquery)|keyNameQ)
        if kjkm:
            kjkmquery = KJKM.objects.filter(keyNameQ)
        else:
            kjkmquery = KJKM.objects.filter(Q(name__contains=kjkm))

        kjkmticketyquery = KJKMTicket.objects.filter(Q(kjkm__in=kjkmquery)&Q(tickets__in=ticketquery))
    bbFieldValuequery = BBFieldValue.objects.filter(keyQ)
    if hy:
        kjkmticketyquery = kjkmticketyquery.filter(tickets__in=TaxTicket.objects.filter(group=hy))
        bbFieldValuequery = bbFieldValuequery.filter(kjkmticket__in=KJKMTicket.objects.filter(tickets__in=TaxTicket.objects.filter(group=hy)))

    kjkmticketids = []
    for b in bbFieldValuequery:
        kjkmticketids.append(b.kjkmticket_id)
    for k in kjkmticketyquery:
        kjkmticketids.append(k.id)

    l = []
    datadict = {}
    maxkind=0
    for bbvalue in BBFieldValue.objects.filter(kjkmticket__in=kjkmticketids):
        if datadict.has_key(str(bbvalue.kjkmticket_id)):
            d = datadict[str(bbvalue.kjkmticket_id)]
        else:
            d = {'kjkmticketid':bbvalue.kjkmticket_id }
            d['kjkm']= bbvalue.kjkmticket.kjkm.name
            d['ticket'] = bbvalue.kjkmticket.tickets.name
            d['groupid'] = bbvalue.kjkmticket.tickets.group_id
            d['group'] = bbvalue.kjkmticket.tickets.group.name
            num = doKindCeng(bbvalue.kjkmticket.tickets.taxkind,d)
            if num > maxkind:
                maxkind = num
            datadict[str(bbvalue.kjkmticket_id)] = d
            l.append(d)
        d['%s'%bbvalue.bbfield_id]=bbvalue.value
    result ={'kindnum':maxkind, 'result':l}

    return getResult(True, '', result)

def doKindCeng(kind,d):
    if kind.fatherKind:
        c = doKindCeng(kind.fatherKind,d)
        d['kind%s'%(c+1,)]=kind.name
        return c+1
    else:
        d['kind%s'%0]=kind.name
        return 0