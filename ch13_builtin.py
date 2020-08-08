# -*- coding: utf-8 -*-

#datetime   py处理日期和时间的标准库
'''
1.datatime
2.timestamp
计算机中的时间实际上是用数字表示的:
把1970年1月1日 00:00:00 UTC+00:00时区的时刻称为 epoch time(纪元时间),记为0(1970年以前的时间timestamp为负数)
    当前时间就是相对于 epoch time 的秒数-->timestamp
timestamp = 0 = 1970-1-1 00:00:00 UTC+0:00
    timestamp = 0 = 1970-1-1 08:00:00 UTC+8:00  #北京时间
    -->timestamp的值与时区毫无关系
        timestamp一旦确定,其UTC时间就确定了,转换到任意时区的时间也是完全确定的
        (为什么计算机存储的当前时间是以timestamp表示的原因)
3.timestamp是一个浮点数且没有时区的概念,而datetime是有时区的
    eg:
        2015-04-19 12:20:00 #本地(北京 东八区)时间,UTC+8:00时区的时间
        -->2015-04-19 12:20:00 UTC+8:00 (+8小时)
        此时UTC+0:00时区的时间(格林威治标准时间):   2015-04-19 04:20:00 UTC+0:00
--->UTC标准时区的时间
4.str和datetime互转
5.对日期和时间进行加减实际上就是把datetime往后或往前计算(得到新的datetime),需要导入timedelta
6.本地时间转换为UTC时间
    一个datetime类型有一个时区属性tzinfo(默认为None,无法区分这个datetime到底是哪个时区,除非强行给datetime设置一个时区)
    时区转换
        先通过utcnow()拿到当前的UTC时间,再转换为任意时区的时间

几个时间概念:
datatime                #日期/时间
timestamp               #时间戳(与时区无关,但在不同时区表示的日期/时间不同哦)
timestamp for utc       #标准时区对应的日期/时间
'''
from datetime import datetime,timedelta,timezone   #前面模块后面类
def demo001():
    #获取当前日期和时间
    now = datetime.now()
    print(now)
    print(type(now))
    #获取指定日期和时间
    dt = datetime(2020,8,9,1,21)
    print(dt)
    #datetime转换为timestamp
    print(dt.timestamp())   #timestamp是一个浮点数,整数位表示秒-->除以1000得到毫秒级别的值
    #timestamp转换为datetime
    print(datetime.fromtimestamp(datetime(2020,8,9,1,21).timestamp()))
    #timestamp也可以直接被转换到UTC标准时区的时间
    print(datetime.utcfromtimestamp(datetime(2020,8,9,1,21).timestamp()))
    #str转换为datetime
    print(datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S'))  #规定了日期和时间部分的格式,注意转换后的datetime是没有时区信息的
    print(datetime.fromtimestamp(datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S').timestamp()))
    print(datetime.utcfromtimestamp(datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S').timestamp()))
    #datetime转换为str
    now = datetime.now()
    print(now.strftime('%a, %b %d %H:%M'))  #格式化字符串
    #datetime加减
    print(datetime.now())
    print(datetime.now()+timedelta(hours=10))
    print(datetime.now()-timedelta(days=1))
    #本地时间转换为UTC时间
    tz_utc_8 = timezone(timedelta(hours=1)) # 创建时区UTC+8:00
    now = datetime.now()
    print(now)
    dt = now.replace(tzinfo=tz_utc_8)   #强制设置为UTC+8:00
    print(dt)
    #时区转换
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    print(utc_dt)                                            #拿到UTC时间并强制设置时区为UTC+0:00
    print(utc_dt.astimezone(timezone(timedelta(hours=8))))   #将转换时区为北京时间:

#collections    提供了许多有用的集合类
'''
'''

if __name__=='__main__':
    demo001()