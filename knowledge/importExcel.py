#coding=utf-8
#Date: 11-12-8
#Time: 下午10:28
from knowledge.models import Ticket
from util.tools import getResult

__author__ = u'王健'

import xlrd

def countRows(start,end,colnum,sh):
    f=True
    s = 0
    l = []
    for i in range(start,end):
        if f and sh.cell_value(i,colnum):
            f=False
            s = i
        elif not f and sh.cell_value(i,colnum):
            l.append((s,i-1))
            f = False
            s = i
    if not f and sh.cell_value(s,colnum):
        l.append((s,end-1))
    print l
    return l


def initData(request):
    if not request:
        xls = '../static/data.xls'
    else:
        from FTknowledge.settings import STATIC_ROOT
        from models import Group, TaxKind, TaxTicket, BBField, BBFieldValue, KJKM, KJKMTicket
        xls = '%s/data.xls'%STATIC_ROOT
        bbdict = {}
        s=u'关联增值税报表主表 关联增值税报表主表一 关联增值税报表主表二 固定资产抵扣 关联企业所得税主表 关联税收优惠明细表 关联所得税与流转税对比表 关联财务报表利润表'
        for ss in s.split(' '):
            if not bbdict.has_key(ss):
                bbdict[ss]=BBField.objects.get(fieldname=ss)

    bk = xlrd.open_workbook(xls)



    for sheetname in bk.sheet_names():
        if 'Sheet3' == sheetname:
            continue
        if request:
            if Group.objects.filter(name=sheetname).count()==0:
                group = Group()
                group.name = sheetname
                group.is_active = True
                group.save()
            else:
                group = Group.objects.get(name=sheetname)

        startrow = 2
        # if u'商业类' != sheetname:
        #     continue
        print sheetname
        sh = bk.sheet_by_name(sheetname)

        nrows = sh.nrows
        nclos = sh.ncols
        l = countRows(2,nrows,0,sh)
        for s,e in l:
            print '(%s,%s):%s'%(s,0,sh.cell_value(s,0))

            if request:
                sname=sh.cell_value(s,0)
                if TaxKind.objects.filter(name=sname).count()==0:
                    tax = TaxKind()
                    tax.name = sname
                    tax.fatherKind = None
                    tax.is_active = True
                    tax.save()
                else:
                    tax = TaxKind.objects.get(name=sname)
            zl = countRows(s,e+1,1,sh)
            for ss,ee in zl:
                print '(%s,%s):%s'%(ss,1,sh.cell_value(ss,1))

                if request:
                    ssname = sh.cell_value(ss,1)
                    if TaxKind.objects.filter(name=ssname,fatherKind=tax).count()==0:
                        sstax = TaxKind()
                        sstax.name = ssname
                        sstax.fatherKind = tax
                        sstax.is_active = True
                        sstax.save()
                    else:
                        sstax = TaxKind.objects.get(name =ssname,fatherKind=tax)

                pl = countRows(ss,ee+1,2,sh)
                for ps,pe in pl:
                    print '(%s,%s):%s'%(ps,2,sh.cell_value(ps,2))
                    if request:
                        psname = sh.cell_value(ps,2)
                        if TaxTicket.objects.filter(name=psname,group=group,taxkind=sstax).count()==0:
                            ticket = TaxTicket()
                            ticket.name = psname
                            ticket.group = group
                            ticket.taxkind = sstax
                            ticket.save()
                        else:
                            ticket = TaxTicket.objects.get(name=psname,group=group,taxkind=sstax)

                        try:
                            t = Ticket()
                            t.name = psname
                            t.save()
                        except:
                            pass


                    print '(%s,%s):%s'%(ps,3,sh.cell_value(ps,3))
                    if request:
                        kjkmname = sh.cell_value(ps,3)
                        if KJKM.objects.filter(name = kjkmname).count()==0:
                            kjkm = KJKM()
                            kjkm.name = kjkmname
                            kjkm.save()
                        else:
                            kjkm = KJKM.objects.get(name=kjkmname)

                        if KJKMTicket.objects.filter(kjkm=kjkm,tickets=ticket).count()==0:
                            kjkmticket = KJKMTicket()
                            kjkmticket.kjkm = kjkm
                            kjkmticket.tickets = ticket
                            kjkmticket.save()
                        else:
                            kjkmticket = KJKMTicket.objects.get(kjkm=kjkm,tickets=ticket)
                        for j in range(nclos):
                            if bbdict.has_key(sh.cell_value(1,j)):
                                v = sh.cell_value(ps,j)
                                if BBFieldValue.objects.filter(kjkmticket=kjkmticket,bbfield=bbdict[sh.cell_value(1,j)]).count()==0:
                                    bbv = BBFieldValue()
                                else:
                                    bbv = BBFieldValue.objects.get(kjkmticket=kjkmticket,bbfield=bbdict[sh.cell_value(1,j)])
                                if v and v!=u'无':

                                    bbv.value = v
                                    bbv.kjkmticket = kjkmticket
                                    bbv.bbfield = bbdict[sh.cell_value(1,j)]
                                    bbv.save()
                                elif bbv.pk:
                                    bbv.delete()


        # print sh.cell_value(11,0)
    if request:
        return  getResult(True,u'success')

if __name__=='__main__':
    initData(None)