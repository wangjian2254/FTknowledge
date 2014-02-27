#coding=utf-8
# Create your views here.
import datetime
from django.contrib.auth import  login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, AnonymousUser
from django.http import HttpResponse
from django.shortcuts import render_to_response
from tools import getResult
from models import Group, TaxKind, TaxTicket, BBField, BB


def index(request):
    url='http://'+request.META['HTTP_HOST']+'/static/swf/'
    return render_to_response('index.html',{'url':url,'p':datetime.datetime.now()})

def menu(request):
    menuxml='''
    <?xml version='1.0' encoding='utf-8'?>
			<root>
				<menu mod='myMenu1' label='基础管理'>

				    <menuitem label='分类管理' mod='taxkind'></menuitem>
				    <menuitem label='报表管理' mod='bbedit'></menuitem>
				    <menuitem label='用户管理' mod='people'></menuitem>

				</menu>
				<menu mod='myMenu2' label='知识库'>
				    <menuitem label='知识库编辑' mod='knowledgeedit'></menuitem>
				    <menuitem label='知识库查询' mod='knowledgesearch'></menuitem>

				</menu>

			</root>
    '''
    return HttpResponse(menuxml)

def logout(request):
    auth_logout(request)
    return getResult(True,'')

def login(request):
    username = request.REQUEST.get('username')
    if username:
        userlist = User.objects.filter(username=username)[:1]
        if len(userlist)>0:
            user=userlist[0]
            if not user.is_active:
                return getResult(False,u'用户已经停止使用。')
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():


        # Okay, security checks complete. Log the user in.
        auth_login(request, form.get_user())

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        return getResult(True,u'登录成功')
    else:
        return getResult(False,u'用户名密码错误')
def regUser(request):
    result = saveUser(request)
    if result.get('success'):
        auth_login(request, User.objects.get(pk=result.get('result').get('pk')))

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return getResult(True,'',None)
    else:
        return getResult(False,'注册失败',None)
def saveUser(request):
    id = request.REQUEST.get('id','')
    if id:
        user = User.objects.get(pk=id)
    else:
        user = User
        user.set_password('111111')
        user.username = request.REQUEST.get('username','')
        if not user.username or User.objects.filter(username=user.username).count()>0:
            return getResult(False,u'用户名已经存在',None)
    is_active = request.REQUEST.get('isaction','')
    if is_active:
        if is_active == 'true':
            user.is_active=True
        else:
            user.is_active=False
    is_staff = request.REQUEST.get('ismanager','')
    if is_staff:
        if is_staff == 'true':
            user.is_staff = True
        else:
            user.is_staff = False
    user.first_name = request.REQUEST.get('truename',u'游客')
    if request.REQUEST.has_key('password'):
        user.set_password(request.REQUEST.get('password'))
    user.save()
    return getResult(True,'',{'username':user.username,'truename':user.first_name,'ismanager':user.is_staff,'isaction':user.is_active,'id':user.pk})

def allmanager(request):
    uq=User.objects.filter(is_staff=True).filter(is_active=True)
    l=[]
    for u in uq:
        l.append({'username':u.username,'truename':u.first_name,'ismanager':u.is_staff,'isaction':u.is_active,'id':u.pk})

    return getResult(True,'',l)

def currentUser(request):
    if  isinstance(request.user,AnonymousUser):
        return getResult(True,'',None)
    else:
        return getResult(True,'',{'username':request.user.username,'truename':request.user.first_name,'ismanager':request.user.is_staff,'isaction':request.user.is_active,'id':request.user.pk})

def getHyList(request):
    l=[]
    for g in Group.objects.filter(is_active=True).order_by('id'):
        l.append({'id':g.pk, 'name':g.name})
    return getResult(True,'',l)


def getTaxKind(request):
    group = request.REQUEST.get('groupid','')
    groupquery = Group.objects.filter(is_active=True)
    if group:
        groupquery=groupquery.filter(pk=group)

    kindlist=[]
    kindidlist=[]
    kinddict={}
    for kind in TaxKind.objects.all().order_by('id'):
        kinddict['%s'%kind.pk]={'id':kind.pk, 'type':'kind', 'fatherKindid':kind.fatherKind_id,'name':kind.name,'is_active':kind.is_active,'children':[]}
        kindidlist.append(kind.pk)
    kind = None
    for kid in kindidlist:
        kind = kinddict.get(str(kid))
        if not kind['fatherKindid']:
            kindlist.append(kind)
        else:
            kinddict[str(kind.get('fatherKindid'))]['children'].append(kind)
    for ticket in TaxTicket.objects.filter(group__in=groupquery).order_by('id'):
        kinddict['%s'%ticket.taxkind_id]['children'].append({'name':ticket.name, 'id':ticket.pk, 'type':'ticket', 'fatherKindid':ticket.taxkind_id})
    for kind in kinddict.values():
        if len(kind['children'])==0:
            del kind['children']
    return getResult(True,'',kindlist)


def saveTaxKind(request):
    id = request.REQUEST.get('id','')
    name = request.REQUEST.get('name','')
    kindFatherId = request.REQUEST.get('kindFatherId','')
    is_active = request.REQUEST.get('is_active','')

    if id:
        taxKind = TaxKind.objects.get(pk=id)
    else:
        taxKind = TaxKind()
    taxKind.name = name.strip()
    if kindFatherId:
        taxKind.fatherKind = TaxKind.objects.get(pk=kindFatherId)
    if is_active == 'true':
        taxKind.is_active=True
    else:
        taxKind.is_active=False
    taxKind.save()

    return getResult(True,'',taxKind.pk)





def saveTaxTicket(request):
    id = request.REQUEST.get('id','')
    name = request.REQUEST.get('name','')
    taxkindid = request.REQUEST.get('taxkindid','')
    groupid = request.REQUEST.get('groupid','')

    if id:
        taxTicket = TaxTicket.objects.get(pk=id)
    else:
        taxTicket = TaxTicket()
    taxTicket.name = name.strip()
    if taxkindid:
        taxTicket.taxkind = TaxKind.objects.get(pk=taxkindid)
    if groupid:
        taxTicket.group = Group.objects.get(pk=groupid)
    taxTicket.save()

    return getResult(True,'',taxTicket.pk)




def delTaxTicket(request):
    id = request.REQUEST.get('id','')
    if id:
        taxTicket = TaxTicket.objects.get(pk=id)
        taxTicket.delete()
    else:
        getResult(False,u'票据不存在',None)

    return getResult(True,'',None)


def getBB(request):
    bblist=[]
    for bb in BB.objects.all().order_by('id'):
        bd={'children':[], 'id':bb.pk, 'name':bb.name, 'type':'bb'}
        bblist.append(bd)

        for field in BBField.objects.filter(bb=bb).order_by('id'):
            bd['children'].append({'id':field.pk, 'name':field.fieldname, 'type':'field'})
    return getResult(True,'',bblist)

def saveBB(request):
    id = request.REQUEST.get('id','')
    name = request.REQUEST.get('name','')
    if id:
        bb = BB.objects.get(pk=id)
    else:
        bb = BB()
    bb.name = name
    bb.save()
    return getResult(True,'',bb.pk)


def delBB(request):
    id = request.REQUEST.get('id','')
    if id:
        taxTicket = BB.objects.get(pk=id)
        taxTicket.delete()
    else:
        getResult(False,u'报表不存在',None)

    return getResult(True,'',None)

def saveBBField(request):
    id = request.REQUEST.get('id','')
    bbid = request.REQUEST.get('bbid','')
    name = request.REQUEST.get('name','')
    if id:
        bbf=BBField.objects.get(pk=id)
    else:
        bbf = BBField()
    bbf.bb = BB.objects.get(pk=bbid)
    bbf.fieldname = name
    bbf.save()
    return getResult(True,'',bbf.pk)


def delBBField(request):
    id = request.REQUEST.get('id','')
    if id:
        taxTicket = BBField.objects.get(pk=id)
        taxTicket.delete()
    else:
        getResult(False,u'报表字段不存在',None)

    return getResult(True,'',None)