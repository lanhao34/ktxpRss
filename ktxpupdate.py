# -*- coding: utf-8 -*-
import urllib
from pyquery import PyQuery as pq
import sys
import re
import sqlite3
import os
import dbwrite

def update():      
    dirNow=os.getcwd()
    tLast="2013/03/05 00:00"
    strfile=os.path.join(dirNow,'list.txt')
    try:
        f2 = file(strfile, 'rb')
    except:
        print "请在目录下创建list.txt，并以行为分隔写入关键词".decode('utf').encode('gbk')
        os.system('pause')
        sys.exit(0)

    # strfile=os.path.join(dirNow,'time.txt')
    # try:
    #     f3 = file(strfile, 'rb')
    #     tTemp=f3.readlines()
    #     tLast=tTemp[0]
    #     f3.close()    
    # except:
    #     try:
    #         f3.close()
    #     except:
    #         None
    #     print 'time.txt不存在或为空，默认起始时间为2012/04/05 00:00，你可以编辑time.txt修改起始时间，格式为"yyyy/mm/dd hh:mm"'.decode('utf').encode('gbk')
    ##    os.system('pause')

    print "正在更新中……".decode('utf').encode('gbk')

    hasNew=0
    finish=0
    cx = sqlite3.connect("ktxp.db")
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
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
    cu.execute("select * from t1 Order by subTime desc")
    res = cu.fetchall()
    f = file('index.html', 'w')
    f.write('''
    <html>
        <head>
            <meta charset="utf-8">
            <title>团子极影动漫更新列表</title>
            <link href="css/bootstrap.css" rel="stylesheet">
        <head>
        <body>

      <div class="navbar">
        <div class="navbar-inner">
        <div class="container" style="width: auto;">
        
        <!-- .btn-navbar is used as the toggle for collapsed navbar content -->
        <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        </a>
        <a class="brand" href="#"><strong>极影动漫更新列表</strong></a>
          <div class="nav-collapse">
            <ul class="nav">
                <li>
                    <a href="http://bt.ktxp.com" style="font-size:20">极影官网</a>
                </li>
            </ul>

            <ul class="nav pull-right">
                <a><h2><span class="label label-info" style="font-size:20">BY 叉烧团子</span></h2></a>
            </ul>
            <ul class="nav pull-right">
                <a><h2  style="color:#AAAAAA;margin: 0 40 0 0">有 <span class="label label-important" style="font-size:20">%s</span> 个更新</h2></a>
            </ul>
        </div>
        </div>
        </div>
        </div>
        
    <div class="container-fluid">
    <div class="row-fluid">
    <div class="span" style="margin: 0 0 0 10;">
            '''%str(hasNew))
    j=0;
    for (dbid,dbtime,dbname,dbadd) in res:
        if dbtime>tLast:
                tLast=dbtime
        strTemp='''
        <div class="row show-grid">
            <div class="span" style="background-color: #EEEEEE;border-radius: 8;margin: 5;padding: 5">
                <a href=\"%s\"><h3><strong>%s %s</strong></h3></a>
            </div>
        </div>'''%(dbadd,dbtime,dbname)
        f.write(strTemp)
    f.write('''
                    </div>
                </div>
            </div>
        </body>
    </html>
            ''')
    f.close()

    cu.close()
    cx.close()

    return hasNew
if __name__ == '__main__':
    update()
    print "请输入下载动漫数：".decode('utf')
    from download import downNew
    downNew(int(raw_input()))
    os.system('pause')
