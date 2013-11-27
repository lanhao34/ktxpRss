# -*- coding: utf-8 -*-
import os
import sys
import jft
import re
import time
import download,dbwrite,ktxpupdate

def rssUpdata():
    print time.strftime("%Y/%m/%d %X",time.localtime(time.time()))
    times=[]
    titles=[]
    btAdds=[]
    dirNow=os.path.dirname(sys.argv[0])
    dirNow='F:\Anime\ktxpRss'
    strfile=dirNow+'\list.txt'
    try:
        f2 = file(strfile, 'rb')
    except:
        print "请在目录下创建list.txt，并以行为分隔写入关键词".decode('utf').encode('gbk')
        os.system('pause')
        sys.exit(0)
    keywordList=f2.readlines()
    title=re.sub(r'amp;','',"[澄空学园&华盟字幕社] Robotics;Notes 第05话 简体 MP4 720p")
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
##            times.append(time.strftime("%Y/%m/%d %H:%M",time.strptime(d.entries[j].published,'%a, %d %b %Y %X +%f')))
            print 1
##            btAdds.append(d.entries[j].enclosures[0].href)
if __name__ == '__main__':
    rssUpdata()
