# -*- coding: utf-8 -*-
import xlrd
import os
import sys
import jft

def dirName(title,animeNum):
    downloadpath=r"D:\\Anime"
    dirNow=os.path.dirname(sys.argv[0])
    data = xlrd.open_workbook('dirList.xls')
    table = data.sheets()[0]
    keywords=table.col_values(3)
    for rownum in range(table.nrows):
        hasWord=1
        for keyword in keywords[rownum].split(' '):
            keyword=keyword.encode('utf8')
            if title.upper().find(keyword.upper())<0:
                strTemp=''
                for i in title.decode('utf8'):
                    if u'\u4E00'<i<u'\u9FFF':
                        strTemp+=i
                strTemp=strTemp.encode('utf8')
                strTemp=jft.f2j('utf8','utf8',strTemp)
                if strTemp.upper().find(keyword.upper())<0:
                    hasWord=0
        if hasWord==1:
            dirWords=table.row_values(rownum)
            break
    dirname='%s-%s-%s'%(dirWords[0],animeNum,dirWords[1])
    for i in dirWords[2].split(' '):
        dirname+='[%s]'%i
    dirname=dirname.encode('gbk')
    name=dirWords[1].encode('gbk')
    L = os.listdir(downloadpath)
    for folder in L:
        if folder.find(name)>0:
            oldFolder=folder
    if animeNum<'00':
        dirname=oldFolder
    try:
        os.rename(r'%s\\%s'%(downloadpath,oldFolder),r'%s\\%s'%(downloadpath,dirname))
    except:
        try:
            os.makedirs(r'%s\%s'%(downloadpath,dirname))
        except:
            None
    return dirname
if __name__ == '__main__':
    import sqlite3
    cx = sqlite3.connect("ktxp.db")
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
    cu.execute("select * from t1 Order by subTime")
    res = cu.fetchall()
##    for i in res:
##        if i[1]<'2012/08/09 16:42':
##            continue
    dirName('★千夏字幕組★【學活！】[Gakkatsu!][第21v2話][640x360][x264_AAC][繁體外掛](後期強力招募中！)','05')
