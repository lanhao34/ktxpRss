# -*- coding: utf-8 -*-
import ktxpupdate
import download
import os
import webbrowser
if __name__ == '__main__':
    f=raw_input("是否要更新动漫(Y/N)：".decode('utf-8').encode('gbk'))
    if f.upper()=='Y':
        ktxpupdate.update()
    f=raw_input("是否要打开浏览器查看(Y/N)：".decode('utf-8').encode('gbk'))
    if f.upper()=='Y':
        webbrowser.open_new_tab(os.getcwd()+'\index.html')
    download.downNew(int(raw_input("请输入下载动漫数：".decode('utf-8').encode('gbk'))))
    os.system('pause')