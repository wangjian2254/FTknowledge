# coding=utf-8
#Date:2014/10/10
#Email:wangjian2254@gmail.com
import httplib
import urllib2

__author__ = u'王健'

xmlstr = '''
<xml><ToUserName><![CDATA[gh_25fb94732975]]></ToUserName> <FromUserName><![CDATA[o6gPLjp0KqqpWp_gVpe4_NWN3rvU]]></FromUserName> <CreateTime>1412755821</CreateTime> <MsgType><![CDATA[image]]></MsgType> <PicUrl><![CDATA[http://mmbiz.qpic.cn/mmbiz/wNib3thBcfwYGEHUHPKYy233chI5GVCkGQDWdVVPWpzPXicEAlAStFg1wzTTOuM1O5iaBbibQ3Tia0fyDuw9FOicopNg/0]]></PicUrl> <MsgId>6067740048629213802</MsgId> <MediaId><![CDATA[IKg3BX9kvROiE-kR7IQqILNgnAn5__acozHf4lGU2HTtDtw_kWlLUoa_ITNTINco]]></MediaId> </xml>
 '''


req = urllib2.Request('http://192.168.101.18:8100/weixin/weixinapi')
req.add_header('User-agent', 'Mozilla/5.0')
connection = httplib.HTTPConnection(req.get_host())
connection.request('POST', req.get_selector(), xmlstr.replace('\n',''))
response = connection.getresponse()

print response.read()