# coding=utf-8
# Date:14-6-17
# Email:wangjian2254@gmail.com
from weixin.models import WeiXinUser, WeiXinMessage, Subject

__author__ = u'王健'

import httplib
import json, base64
from django.contrib.auth.models import User

__author__ = u'王健'

from django.http import HttpResponse
from django.utils.encoding import smart_str, smart_unicode

import xml.etree.ElementTree as ET
import urllib, urllib2, time, hashlib

TOKEN = "fd45f84c6edf272"


def handleRequest(request):
    if request.method == 'GET':
        #response = HttpResponse(request.GET['echostr'],content_type="text/plain")
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    elif request.method == 'POST':
        #c = RequestContext(request,{'result':responseMsg(request)})
        #t = Template('{{result}}')
        #response = HttpResponse(t.render(c),content_type="application/xml")
        response = HttpResponse(responseMsg(request), content_type="application/xml")
        return response
    else:
        return None


def checkSignature(request):
    global TOKEN
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr", None)

    token = TOKEN
    tmpList = [token, timestamp, nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return None


def responseMsg(request):
    rawStr = smart_str(request.body)
    #rawStr = smart_str(request.POST['XML'])
    msg = paraseMsgXml(ET.fromstring(rawStr))
    msgtype = msg.get('MsgType')
    msgid = msg.get('MsgId')
    content = msg.get('Content', '')
    picurl = msg.get('PicUrl', '')
    fuid = msg['FromUserName']
    result_msg = u''
    person = isReg(fuid)

    if msgtype == 'event':
        return eventMsg(msg, person)
    else:
        weixinmsg, created = WeiXinMessage.objects.get_or_create(messageid=msgid)
        if created:
            weixinmsg.content = content
            weixinmsg.imgurl = picurl
            weixinmsg.weixinuser = person
            weixinmsg.save()
        return ''
    return getReplyXml(msg, result_msg.encode('utf-8'))


def paraseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg


def getReplyXml(msg, replyContent):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    extTpl = extTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), 'text', replyContent)
    return extTpl

def getReplyXmlImg(msg, replyContent,url):
    extTpl='''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>1</ArticleCount>
<Articles>
<item>
<Title><![CDATA[手机号实名]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[]]></Url>
</item>
</Articles>
</xml> '''
    extTpl = extTpl % (msg['FromUserName'], msg['ToUserName'], str(int(time.time())), replyContent, url)
    return extTpl

def eventMsg(msg, person):
    eventtype = msg.get('Event')
    eventkey = msg.get('EventKey', '')
    if eventtype == 'CLICK':
        if eventkey == 'user':
            # 注册
            pass
        elif eventkey == 'shiming':
            # 实名
            pass
    elif eventtype == 'subscribe':
        if eventkey.find('qrscene_') == 0:
            return getReplyXml(msg, join_subject(eventkey[8:], person).encode('utf-8'))
    elif eventtype == 'unsubscribe':
        u, c = WeiXinUser.objects.get_or_create(weixinid=msg['FromUserName'])
        if not c:
            u.is_active = False
            u.save()
        return getReplyXml(msg, u'退订成功'.encode('utf-8'))
    elif eventtype == 'SCAN ':
        return getReplyXml(msg, join_subject(eventkey, person).encode('utf-8'))


def join_subject(code, person):
    subject, created = Subject.objects.get_or_create(code=int(code))
    if created:
        return u'参与的活动存在或已经结束'
    if subject.status:
        subject.weixinusers.add(person)
        return u'欢迎参与：%s' % subject.name
    else:
        return u'%s 活动已经结束' % subject.name


def isReg(weixinid):
    person, created = WeiXinUser.objects.get_or_create(weixinid=weixinid)
    if created:
        person.save()
        getUserInfo(person.weixinid)
    return person


def getUserInfo(weixinid):
    pass
