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
1.namedtuple
用来创建一个自定义的tuple类(tuple的一种子类),并且规定了tuple元素的个数,同时可以用属性而不是索引来引用tuple的某个元素
    具备tuple的不变性又可以根据属性来引用
2.deque
使用list存储数据时按索引访问元素很快,但是插入和删除元素就很慢<--list是线性存储
为了高效实现插入和删除操作的双向列表-->deque(适合用于队列和栈)
    除了实现list的append()和pop()外,还支持appendleft()和popleft().这样就可以非常高效地往头部添加或删除元素
3.defaultdict
使用dict时,若引用的Key不存在就会抛出KeyError
    -->key不存在时返回一个默认值(调用函数返回的)    defaultdict
4.OrderedDict
使用dict时,Key是无序的-->迭代时是无法确定顺序
    -->OrderedDict 可保持Key的顺序(按照插入的顺序排列,不是Key本身排序)
5.ChainMap
把一组dict串起来并组成一个逻辑上的dict
    本身也是一个dict,查找时会按照顺序在内部的dict依次查找(一组dict按序列顺序进行查找)
6.Counter
一个简单的计数器
    实际上也是dict的一个子类
'''
from collections import namedtuple,deque,defaultdict,OrderedDict,ChainMap,Counter
import os, argparse

def demo002():
    Point = namedtuple('point', ['x','y'])
    p1 = Point(1,2) 
    p2 = Point(3,4)
    print(type(p1))
    print(isinstance(p1, tuple))    #<class '__main__.point'>
    print(isinstance(p1, Point))
    print(p1.x)
    print(p1[0])
    #
    d1 = deque(['a','b','c'])
    d1.append('d')
    d1.appendleft('0')
    print(d1)
    #
    dd = defaultdict(lambda : "N/A")
    dd[1]=1
    print(dd[1])
    print(dd[2])    #返回默认值
    #
    od = OrderedDict()
    od[1]=10
    od[2]=20
    od[3]=30
    print(od)
    print(list(od.keys()))
    #
#实现一个FIFO（先进先出）的dict
class moniFIFO(OrderedDict):
    def __init__(self, capacity):
        super(moniFIFO, self).__init__()
        self._capacity = capacity
    def __setitem__(self, key, value):  #赋值重载
        contain = 1 if key in self else 0   #add or set
        if len(self) - contain >= self._capacity:   #已满
            print('remove: ', self.popitem(last=False))
        if contain:
            del self[key]
            print("set: ", (key, value))
        else:
            print("add: ", (key, value))
        OrderedDict.__setitem__(self, key, value) 
def demo003():
    obj = moniFIFO(5)
    obj[1] = 1
    obj[2] = 2
    obj[3] = 3
    obj[4] = 4
    obj[5] = 5
    print(obj)
    obj[6] = 6
    print(obj)
# 构造缺省参数:
defaults = {
    'color': 'red',
    'user': 'guest'
}
def demo004():
    # 构造命令行参数:
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-c', '--color')
    namespace = parser.parse_args()
    command_line_args = { k: v for k, v in vars(namespace).items() if v }
    # 组合成ChainMap:命令行参数 > 环境变量 > 默认参数
    combined = ChainMap(command_line_args, os.environ, defaults)    
    # 打印参数:
    print('color=%s' % combined['color'])   
    print('user=%s' % combined['user'])
#统计字符出现的个数
def demo005():
    c = Counter()
    c.update('hello')
    print(c)

##base64
'''
'''

##struct
'''
'''

#contextlib(py也有context？)
'''
1.任何对象,只要正确实现了上下文管理就可以用于with语句
    上下文管理是通过__enter__和__exit__这两个方法实现的
2.编写__enter__和__exit__仍然很繁琐--->标准库 contextlib 提供了更简单的写法
    在某段代码执行前后自动执行特定代码,也可以用@contextmanager实现
        代码顺序:
        (1).with语句先执行yield之前的语句
        (2).yield调用会执行with语句内部的所有语句
        (3).执行yield之后的语句
        -->@contextmanager通过编写generator来简化上下文管理(某段代码执行前后的逻辑控制)
3.若一个对象没有实现上下文,就不能把它用于with语句.此时可以用closing()来把该对象变为上下文对象
eg: 用with语句使用urlopen()
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)
---->closing(其作用把任意对象变为上下文对象)也是一个经过@contextmanager装饰的generator:
@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()
'''
class Query(object):
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        print('begin~~')
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')
    def query(self):
        print('Query info about %s...' % self.name)
def demo008():
    with Query("city") as q:
        #with前后会执行 __enter__ 和 __exit__ 方法
        q.query()
from contextlib import contextmanager
class QueryEx(object):
    def __init__(self, name):
        self.name = name
    def query(self):
        print('Query info about %s...' % self.name)
@contextmanager     #接受一个generator,用yield语句把with ... as var把变量输出出去
def demo009(name):
    print('Begin')
    q = QueryEx(name)
    yield q
    print('End')
def demo010():
    with demo009('Bob') as q:
        q.query()
#
@contextmanager
def tag(name):
    print("<%s>" % name)    #begin
    yield
    print("</%s>" % name)   #end
def demo011():
    with tag('h1'):
        print('hello')
        print('world')


#urllib
'''
urllib提供了一系列用于操作URL的功能:
1.urllib的request模块可以非常方便地抓取URL内容,也就是发送一个GET请求到指定的页面,然后返回HTTP的响应
2.要以POST发送一个请求,只需要把参数data以bytes形式传入
'''
from urllib import request
def demo006():
    with request.urlopen("https://www.sina.com.cn") as f:
        data = f.read()
        print("status: ", f.status, f.reason)
        for k,v in f.getheaders():
            print("%s: %s" % (k, v))
        print("Data: ", data.decode('utf-8'))
#模拟浏览器发送GET请求:需要使用Request对象(通过往Request对象添加HTTP头,就可以把请求伪装成浏览器)
def demo007():
    req = request.Request("https://www.sina.com.cn")
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    with request.urlopen(req) as f:
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        print('Data:', f.read().decode('utf-8'))    #返回移动端内容

if __name__=='__main__':
    demo011()