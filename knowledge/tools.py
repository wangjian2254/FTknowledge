#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
import json
from django.http import HttpResponse
from django.core.cache import cache
from knowledge.models import Group

__author__ = u'王健'

def getResult(success,message,result=None,status_code=200,cachename=None):
    '''
    200 正常返回 code
    404 登录过期，需要重新登录
    '''
    map={'success':success,'message':message, 'status_code':status_code}
    if result:
        map['result']=result
    jsonstr=json.dumps(map)
    if cachename:
        cache.set(cachename,jsonstr,3600*24*31)
    return HttpResponse(jsonstr)


def clearTicketCache(id=None):
    if id:
        cache.delete('taxkindstr%s' % id)
    else:
        for group in Group.objects.all():
            cache.delete('taxkindstr%s' % group.pk)