# coding=utf-8
# Date:2014/10/10
#Email:wangjian2254@gmail.com
import datetime
from django.shortcuts import render_to_response
from util.tools import getResult
from weixin.models import WeiXinMessage, Subject

__author__ = u'王健'


def subjecthtml(request):
    limit = request.REQUEST.get('limit', '1')
    time = request.REQUEST.get('time', '3')
    subjectcode = request.REQUEST.get('subjectcode', '')
    return render_to_response('weixin/subject2.html', {'limit': limit, 'time': time, 'subjectcode': subjectcode})


def get_new_weixinmessage(request):
    last_id = request.REQUEST.get('last_id', '')
    subjectcode = request.REQUEST.get('subjectcode', '')
    limit = request.REQUEST.get('limit', '1')
    if not last_id:
        t = datetime.datetime.now()
        last_day = datetime.datetime(t.year, t.month, t.day - 1)
    messagequery = WeiXinMessage.objects
    if subjectcode:
        subject, c = Subject.objects.get_or_create(code=int(subjectcode))
        if not c:
            messagequery = messagequery.filter(code=subject.code)
            if subject.is_check:
                messagequery = messagequery.filter(is_check=True)

    if last_id:
        messagequery = messagequery.filter(pk__gt=last_id)
    else:
        messagequery = messagequery.filter(create_time__gte=last_day)
    l = []
    for m in messagequery[:int(limit)]:
        l.append(
            {'id': m.pk, 'content': m.content, 'imgurl': m.imgurl, 'create_time': m.create_time.strftime('%H:%M:%S')})
    return getResult(True, '', l)
