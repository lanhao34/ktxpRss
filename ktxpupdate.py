# -*- coding: utf-8 -*-
import urllib
from pyquery import PyQuery as pq
import sys
import re
import sqlite3
import os
import dbwrite
        
dirNow=os.path.dirname(sys.argv[0])

tLast="2012/04/05 00:00"
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
for keywords in f2:
    print keywords
    times  = []
    titles = []
    btAdds = []
    k=0
    s_utf=keywords.decode(sys.stdin.encoding).encode("utf-8")
    url_str='http://bt.ktxp.com/search.php?keyword=%s'%urllib.quote(s_utf)
    d = pq(url=url_str)
    div=d('tbody tr')
    diva=div('.ttitle')
    for i in div(":contains(':')"):
        times.append(pq(i).attr('title'))
    for i in diva("[href^='/html']"):
        titles.append(re.sub(r'amp;','',re.sub(r'(?=\<).*?(?<=>)','', pq(i).html())))
    for i in diva("[href$='.torrent']"):
        btAdds.append(r'http://bt.ktxp.com'+pq(i).attr('href'))
    hasNew+=dbwrite.dbwrite(times,titles,btAdds)
print hasNew
os.system('pause')
