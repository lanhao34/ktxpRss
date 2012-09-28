# -*- coding: utf-8 -*-
import urllib
from pyquery import PyQuery as pq
import sys
import re
import os
import time
from string import atoi
from lx import lixian_cli
from animeDir import dirName

def download(times,title,btAdd):
    Title=title
    title=re.sub(r'\\',r'﹨'.decode('utf8').encode('gbk'),re.sub(r'/',r'∕'.decode('utf8').encode('gbk'),title.decode('utf8').encode('gbk')))
    dirNow=os.path.dirname(sys.argv[0])
    downloadpath=r"D:\\Anime"
    strfile=dirNow+'\list.txt'
    torrent=dirNow+'\\Torrent\\'+title+'.torrent'
    add=btAdd.encode('utf8')
    print times,title
    urllib.urlretrieve(add,torrent)
    for i in range(0,9):
        try:
            (task_id,status,filename)=lixian_cli.add_task(['--bt',torrent])
            while (not status=='completed'):
                time.sleep(60)
                (task_id,status,filename)=lixian_cli.add_task(['--bt',torrent])
            break
        except:
            time.sleep(10)
    print filename
    try:
        Nums=re.findall("(?<=\[)(\d+-\d+)?(?=\])",filename)
        Num=re.findall("(\d+)",Nums[0])
        if abs(atoi(Num[0])-atoi(Num[1]))>=5:
            print "已完结".decode('utf').encode('gbk')
            return 1
    except:
        pass
    if filename.find('ALL')>=0:
        print "已完结".decode('utf').encode('gbk')
        return 1
    Num=re.findall("(?<=\[)(\d+)(?:v\d+|_\d+)?(?=\])",filename)
    dellist=['720']
    for i in Num:
        if len(i)>3:
            dellist.append(i)
    for i in dellist:
        try:
            Num.remove(i)
        except:
            pass
    try:
        downloadpath+='\\'+dirName(Title,max(Num))
    except:
        Num=[]
        names=lixian_cli.list_task([task_id+'/','--name'])
        for filename in names:
            Num+=re.findall("(?<=\[)(\d+)(?:v\d+|_\d+)?(?=\])",filename)
        dellist=['720','576']
        for i in Num:
            if len(i)>3:
                dellist.append(i)
        for i in dellist:
            try:
                Num.remove(i)
            except:
                pass
        if atoi(max(Num))-atoi(min(Num))>=5:
            print "已完结".decode('utf').encode('gbk')
            return 1
        downloadpath+='\\'+dirName(Title,max(Num))
##    try:
##        lixian_cli.download_task([task_id,"--output-dir",downloadpath])
##    except:
    for i in range(0,9):
        try:
            lixian_cli.download_task([task_id,"--output-dir",downloadpath,"-c"])
            break
        except:
            time.sleep(10)

def downNew(hasNew):
    import sqlite3
    cx = sqlite3.connect("ktxp.db")
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
    cu.execute("select * from t1 Order by subTime desc LIMIT %s"%hasNew)
    res = cu.fetchall()
    for i in res[::-1]:
##        if i[1]<'2012/08/11 05:42':
##            continue
        try:
            result=download(i[1],i[2],i[3])
            if result==1:
                f3 = file('Download.log', 'a')
                f3.write("%s %s 已完结\n"%(i[1],i[2]))
                f3.close()
        except:
            os.system('pause')
##        download(i[1],i[2],i[3])

if __name__ == '__main__':
##    import sqlite3
##    cx = sqlite3.connect("ktxp.db")
##    cx.isolation_level = None
##    cx.text_factory = str
##    cu = cx.cursor()
##    cu.execute("select * from t1 Order by subTime")
##    res = cu.fetchall()
##    for i in res:
##        if i[1]<'2012/08/11 05:42':
##            continue
##        download(i[1],i[2],i[3])
    
    downNew(raw_input())
    os.system('pause')
