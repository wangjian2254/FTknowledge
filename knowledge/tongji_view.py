#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from django.http import HttpResponse
from knowledge.models import Relation, Rule, PZ

__author__ = u'王健'



def tongji(request):

    allrelation = Relation.objects.all()
    msg = [u'总规则数量：%s'%allrelation.count()]
    msg.append(u'总行业数量:%s'%Rule.objects.all().count())
    for rule in Rule.objects.all():
        rq = allrelation.filter(rule=rule)
        rn = rq.count()
        pzn = PZ.objects.filter(business__in=rq.values_list('business',flat=True)).count()

        m= u'%s : %s 条规则，%s 条凭证, %s 条财务, %s 条税务, %s 条涉税'%(rule.name,rn,pzn,rn,rn,rn)
        msg.append(m)
    return HttpResponse('\n<br/>'.join(msg))


