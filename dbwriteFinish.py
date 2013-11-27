import sqlite3

def dbwrite(times,titles,adds):
    hasNew=0
    cx = sqlite3.connect("finish.db")
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
    cu.execute('create table if not exists t1(id integer primary key,subTime string,title string UNIQUE,btAdd string)')
    for i in range(0,len(times)):
        if times[i]<'2012/06/15 00:00':
            continue
        try:
            cu.execute("insert into t1(subTime,title,btAdd) values('%s','%s','%s')"%(times[i],titles[i],adds[i]))
            print times[i],titles[i]
            hasNew+=1
        except:
            pass
    cx.commit()
    cu.close()
    cx.close()
    return hasNew
if __name__ == '__main__':
    print dbwrite('testtime','testtitle','testadd')
