# -*- coding: utf-8 -*-
import feedparser
import os
import sys
import jft
import re
import time
import download,dbwrite

def rssUpdata():
    print time.strftime("%Y/%m/%d %X",time.localtime(time.time()))
    times=[]
    titles=[]
    btAdds=[]
    dirNow=os.path.dirname(sys.argv[0])
    strfile=dirNow+'\list.txt'
    try:
        f2 = file(strfile, 'rb')
    except:
        print "请在目录下创建list.txt，并以行为分隔写入关键词".decode('utf').encode('gbk')
        os.system('pause')
        sys.exit(0)
    keywordList=f2.readlines()
    d = feedparser.parse(r'http://bt.ktxp.com/rss-sort-12.xml')
    for j in range(len(d.entries)):
        title=re.sub(r'amp;','',d.entries[j].title.encode('utf8'))
##        print title.decode('utf8')
        for keywords in keywordList:
            hasWord=1
            keywords=re.sub('\r\n','',keywords.decode('gbk').encode('utf8')).split(' ')
            for keyword in keywords:
                if title.upper().find(keyword.upper())>=0:
##                    print title.find(keyword),keyword
                    pass
                else:
                    strTemp=''
                    for i in title.decode('utf8'):
                        if u'\u4E00'<i<u'\u9FFF':
                            strTemp+=i
                    strTemp=strTemp.encode('utf8')
                    strTemp=jft.f2j('utf8','utf8',strTemp)
                    if strTemp.find(keyword)>=0:
##                        print strTemp.find(keyword),keyword
                        pass
                    else:
                        hasWord=0
##                    print keyword,hasWord
##            print time.strftime("%Y/%m/%d %X",time.strptime(d.entries[j].published,'%a, %d %b %Y %X +%f'))
            if hasWord:
                times.append(time.strftime("%Y/%m/%d %H:%M",time.strptime(d.entries[j].published,'%a, %d %b %Y %X +%f')))
                titles.append(title.decode('utf8'))
                btAdds.append(d.entries[j].enclosures[0].href)
    download.downNew(dbwrite.dbwrite(times,titles,btAdds))
if __name__ == '__main__':
    rssUpdata()
    os.system('pause')
