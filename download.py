# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
import sys
import re
import os
import time
from string import atoi
from animeDir import dirName
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]),'lx'))
import lixian_commands as lxcmd
import lixian_cli
import ConfigParser

def download(times,title,btAdd):
    Title=title
    title=re.sub(r'\\',r'﹨'.decode('utf8').encode('gbk'),re.sub(r'\"',r'',re.sub(r'/',r'∕'.decode('utf8').encode('gbk'),title.decode('utf8').encode('gbk'))))
    dirNow=os.getcwd()
    cf = ConfigParser.ConfigParser()
    cf.read(os.path.join(dirNow,"config.ini"))
    downloadpath=cf.get('info','downloadpath')
    strfile=os.path.join(dirNow,'list.txt')
    # torrent=dirNow+'\\Torrent\\'+title+'.torrent'
    add=btAdd.encode('utf8')
    print times,title
    # try:
    #     response = urllib2.urlopen(add)
    #     import shutil
    #     with open(torrent, 'wb') as output:
    #         shutil.copyfileobj(response, output)
    #     r = requests.get(add)
    #     with open(torrent, "wb") as code:
    #         code.write(r.content)
    #     f = urllib2.urlopen(add)
    #     data = f.read()
    #     with open(torrent, "wb") as code:
    #         code.write(data)
    # except:
    #     os.makedirs(dirNow+'\\Torrent')
    #     f = urllib2.urlopen(add)
    #     data = f.read()
    #     with open(torrent, "wb") as code:
    #         code.write(data)
    for i in range(0,9):
        try:
            t=lxcmd.add.add_task(['--bt',add])[0]
            if (not t['status']==2):
                time.sleep(600)
            while (not t['status']==2):
                time.sleep(600)
                t=lxcmd.add.add_task(['--bt',add])[0]
                break
            break
        except Exception,e:
            print e
            time.sleep(10)
    try:
        Nums=re.findall("(?<=\[)(\d+-\d+)?(?=\])",t['name'])
        Num=Nums[0].split('-')
        if abs(atoi(Num[0])-atoi(Num[1]))>=5:
            print "已完结".decode('utf').encode('gbk')
            return 1
    except:
        pass
    if t['name'].find('ALL')>=0:
        print "已完结".decode('utf').encode('gbk')
        return 1
    Nums=re.findall("(?<=\[)(\d+)(?:v\d+|_\w+)?(?=\])",t['name'])
    dellist=['720','576']
    for i in Nums:
        if len(i)>3:
            dellist.append(i)
    for i in dellist:
        try:
            Nums.remove(i)
        except:
            pass
    try:
        downloadpath+='\\'+dirName(Title,max(Nums))
    except Exception,e:
        print e
        Nums=[]
        tmp_t=lxcmd.list.list_task([t['id']+'/','--name'])
        print tmp_t
        for i in tmp_t:
            filename=i['name']
            Nums+=re.findall("(?<=\[)(\d+)(?:v\d+|_\d+)?(?=\])",filename)
        dellist=['720','576']
        for i in Nums:
            if len(i)>3:
                dellist.append(i)
        for i in dellist:
            try:
                Nums.remove(i)
            except:
                pass
        try:
            if atoi(max(Nums))-atoi(min(Nums))>=5:
                print "已完结".decode('utf').encode('gbk')
                return 1
            downloadpath+='\\'+dirName(Title,max(Nums))
        except Exception,e:
            print e
            downloadpath+='\\'+dirName(Title,['-1'])
    if t['name'].find('EMD')>=0:
        for i in range(0,9):
            try:
                lxcmd.download.download_task([t['id']+"/.mp4","--output-dir",downloadpath,"-c"])
                break
            except Exception,ex:
                print Exception,":",ex
                time.sleep(10)
    else:
        for i in range(0,9):
            try:
                lxcmd.download.download_task([t['id'],"--output-dir",downloadpath,"-c"])
                break
            except Exception,ex:
                print Exception,":",ex
                time.sleep(10)
    lxcmd.delete.delete_task([t['id']])

def downNew(hasNew):
    dirNow=os.getcwd()
    cf = ConfigParser.ConfigParser()
    cf.read(os.path.join(dirNow,"config.ini"))
    if hasNew>0:
        while 1:
            try:
                lixian_cli.login([cf.get('thunder','account'),cf.get('thunder','password')])
                break
            except Exception,ex:
                print Exception,":",ex
        import sqlite3
        cx = sqlite3.connect("ktxp.db")
        cx.isolation_level = None
        cx.text_factory = str
        cu = cx.cursor()
        cu.execute("select * from t1 Order by subTime desc LIMIT %s"%hasNew)
        res = cu.fetchall()
        for i in res[::-1]:
            print hasNew
            if i[1]<'2012/11/02 19:11':
                continue
            while 1:
                try:
                    download(i[1],i[2],i[3])
                    break
                except Exception,ex:
                    print Exception,":",ex
            hasNew=hasNew-1
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
    
    downNew(int(raw_input()))
    os.system('pause')
