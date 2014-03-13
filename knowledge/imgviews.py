#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from knowledge.models import ImageInfo
from knowledge.tools import getResult
from django.core.cache import cache
import datetime
__author__ = u'王健'

def delImg(request):
    imgurl = request.REQUEST.get('imgurl','')
    if imgurl:
        if ImageInfo.objects.filter(img__iendswith = imgurl.split('/')[-1]).count()==0:
            return getResult(True,'')
        else:
            for img in  ImageInfo.objects.filter(img__iendswith = imgurl.split('/')[-1]):
                cache.delete('all%s'%img.modelType)
                img.img.delete()
                img.delete()
            return getResult(True,'')
    return getResult(False,'')

def imgUploaded(request):
    img = request.FILES.get('file','')
    if img:
        imginfo=ImageInfo()
        imginfo.img = img
        imginfo.index = 0
        imginfo.modelId = request.REQUEST.get('mid')
        imginfo.modelType = request.REQUEST.get('mtype')
        imginfo.save()
        cache.delete('all%s'%imginfo.modelType)

    return getResult(True,u'上传成功',imginfo.img.url)