# -*- coding: utf-8 -*-
import ktxpupdate
import download
if __name__ == '__main__':
    print "是否要更新动漫(Y/N)：".decode('utf')
    f=raw_input()
    if f.upper()=='Y':
        ktxpupdate.update()
    print "请输入下载动漫数：".decode('utf')
    download.downNew(int(raw_input())
    os.system('pause')