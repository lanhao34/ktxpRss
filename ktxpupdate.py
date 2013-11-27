# -*- coding: utf-8 -*-
import urllib
from pyquery import PyQuery as pq
import sys
import re
import sqlite3
import os
import dbwrite

def update():      
    dirNow=os.path.dirname(sys.argv[0])

    tLast="2013/03/05 00:00"
    dirNow='D:\Anime\ktxpRss'
    strfile=dirNow+'\list.txt'
    try:
        f2 = file(strfile, 'rb')
    except:
        print "请在目录下创建list.txt，并以行为分隔写入关键词".decode('utf').encode('gbk')
        os.system('pause')
        sys.exit(0)

    strfile=dirNow+'\\time.txt'
    try:
        f3 = file(strfile, 'rb')
        tTemp=f3.readlines()
        tLast=tTemp[0]
        f3.close()    
    except:
        try:
            f3.close()
        except:
            None
        print 'time.txt不存在或为空，默认起始时间为2012/04/05 00:00，你可以编辑time.txt修改起始时间，格式为"yyyy/mm/dd hh:mm"'.decode('utf').encode('gbk')
    ##    os.system('pause')

    print "正在更新中……".decode('utf').encode('gbk')

    hasNew=0
    finish=0
    for keywords in f2:
        while(1):
            try:
                # print keywords
                times  = []
                titles = []
                btAdds = []
                s_utf=keywords.decode(sys.stdin.encoding).encode("utf-8")
                url_str='http://bt.ktxp.com/search.php?keyword=%s'%urllib.quote(s_utf)
                d = pq(url_str)
                break
            except Exception , e:
                print e
        for j in d('tbody tr'):
            div=pq(j)
            if div('td').eq(1).text()=="完整动画".decode('utf'):
                diva=div('.ttitle')
                for i in div("[title]"):
                    time=pq(i).attr('title')
                for i in diva("[href^='/html']"):
                    title=re.sub(r'amp;','',re.sub(r'(?=\<).*?(?<=>)','', pq(i).html()))
                for i in diva("[href$='.torrent']"):
                    btAdd=r'http://bt.ktxp.com'+pq(i).attr('href')
                cx = sqlite3.connect("ktxp.db")
                cx.isolation_level = None
                cx.text_factory = str
                cu = cx.cursor()
                cu.execute('create table if not exists t2(id integer primary key,subTime string,title string UNIQUE,btAdd string)')
                try:
                    cu.execute("insert into t2(subTime,title,btAdd) values('%s','%s','%s')"%(time,title,btAdd))
                    finish+=1
                    print time,title,"已完结".decode('utf')
                    f3 = file('Finish.log', 'a')
                    f3.write("%s %s 已完结\n".decode('utf').encode('gbk')%(time.encode('gbk'),title.encode('gbk')))
                    f3.close()
                except:
                    pass
                cx.commit()
                cu.close()
                cx.close()
            elif div('td').eq(1).text()=="新番连载".decode('utf'):
                diva=div('.ttitle')
                for i in div("[title]"):
                    times.append(pq(i).attr('title'))
                for i in diva("[href^='/html']"):
                    titles.append(re.sub(r'amp;','',re.sub(r'(?=\<).*?(?<=>)','', pq(i).html())))
                for i in diva("[href$='.torrent']"):
                    btAdds.append(r'http://bt.ktxp.com'+pq(i).attr('href'))
        hasNew+=dbwrite.dbwrite(times,titles,btAdds)
    print "更新了%s部动漫".decode('utf')%hasNew
    print "完结了%s部动漫".decode('utf')%finish
    return hasNew

if __name__ == '__main__':
    update()
    print "请输入下载动漫数：".decode('utf')
    from download import downNew
    downNew(raw_input())
    os.system('pause')
