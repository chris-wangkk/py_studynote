# -*- coding: utf-8 -*-

#面向对象高级编程
##使用__slots__
'''
1.动态绑定允许在程序运行的过程中动态给class加上功能（见ch6）
2.想要限制实例的属性怎么办？
    在定义class的时候定义一个特殊的__slots__变量，来限制该class实例能添加的属性
    eg：
        class Student(object):
        __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
    试图绑定非允许的属性将得到AttributeError的错误
-->__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的(除非在子类中也定义__slots__)
'''

##使用@property
'''
1.有没有既能检查参数，又可以用类似属性这样简单的方式来访问类的变量呢？
Py内置的@property装饰器负责把一个方法变成属性调用的
    (1)把一个getter方法变成属性,只需要加上@property就可以了(若不定义setter方法就是一个只读属性)
    (2)把一个setter方法变成属性赋值,加上了另一个装饰器@属性名.setter
'''
class Screen(object):
    def __init__(self, resolution):
        self._resolution = resolution
    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        if 0 >= value:
            raise ValueError("width must over 0")
        self._width = value
    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        if 0 >= value:
            raise ValueError("wheightidth must over 0")
        self._height = value
    @property
    def resolution(self):
        return self._resolution
def demo001():
    obj1 = Screen(10)
    obj2 = Screen(20)
    obj1.height = 11
    obj1.width = 12
    obj2.height = 21
    obj2.width = 22
    print(obj1.width, obj1.height, obj1.resolution)
    print(obj2.width, obj2.height, obj2.resolution)
    #obj2.width = 0

##多重继承
'''
通过多重继承，一个子类就可以同时获得多个父类的所有功能(这种设计通常称之为MixIn)
MixIn的目的
    给一个类增加多个功能，这样在设计类时优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系
    eg：
        Py自带了TCPServer和UDPServer这两类网络服务
        同时服务多个用户就必须使用多进程或多线程模型，这两种模型由ForkingMixIn和ThreadingMixIn提供(协程 CoroutineMixIn)
        -->编写一个多进程模式的TCP服务
            class myTCPServer(TCPServer, ForkingMixIn):
                ...
只允许单一继承的语言（如Java）不能使用MixIn的设计
'''

##定制类
'''

'''
class Student(object):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Student object (name: %s)' % self.name
    __repr__ = __str__
    def __getattr__(self, attr):
        if attr == "x":
            return 100      #动态返回一个属性
        if attr == "y":
            return lambda: 200  #动态返回一个方法
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值
    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):
            #简单处理
            start = n.start
            end = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for i in range(end):
                if i >= start:
                    L.append(a)
                a, b = b, a + b
            return L 
class Chain(object):    #自动生成URL
    def __init__(self, path=''):
        self._path = path
    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))
    def __str__(self):
        return self._path
    __repr__ = __str__
    def __call__(self, param):
        return Chain('%s/:%s' % (self._path, param))
def demo002():
    print(Student('Test'))
    print(Student('Test').x)
    print(Student('Test').y())
    '''
    for n in Fib():
        print(n)
    '''
    f = Fib()
    print(f[0])
    print(f[10])
    print(f[20])
    print(f[0])
    print(f[2:5])
    #
    print(Chain().status.user.timeline.list)
    print(Chain().users('test').repos)

##使用枚举类
'''
可以把一组相关常量定义在一个class中且class不可变，而且成员可以直接比较。
'''
from enum import Enum,unique
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
@unique #检查保证没有重复值
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
@unique
class Gender(Enum):
    Male = 0
    Female = 1
class Student001(object):
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
def demo003():
    for name, member in Month.__members__.items():
        print(name, '=>', member, ',', member.value)    #value属性则是自动赋给成员的int常量，默认从1开始计数
    bart = Student001('Bart', Gender.Male)
    if bart.gender == Gender.Male:
        print('测试通过!')
    else:
        print('测试失败!')

##使用元类
'''
1.动态语言中的函数和类的定义，不是编译时定义的，而是运行时动态创建的
对于如下代码：
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)
Py解释器载入hello模块时，就会依次执行该模块的所有语句，执行结果就是动态创建出一个Hello的class对象(类对象)
类class对象的类型就是type
-->class的定义是运行时动态创建的，而创建class的方法就是使用type()函数:
type()函数既可以返回一个对象的类型(见上),又可以创建出新的类型
2.要创建一个class对象,type()函数依次传入3个参数
(1)class的名称
(2)继承的父类集合(tuple形式)，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法
(3)class的方法名称与函数绑定(dict形式)
通过type()函数创建的类和直接写class是完全一样的
因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class
--->type()函数也允许在运行时动态创建出类
3.metaclass(元类)
除了使用type()动态创建类以外，要控制类的创建行为，还可以使用metaclass
    定义类-->创建类实例
    定义metaclass-->创建类-->创建实例
metaclass允许你创建类或者修改类,类看成是metaclass创建出来的"实例"
'''
#常规or静态
class Hello001(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)
#动态
def fn(self, name='world'):
    print('Hello, %s.' % name)
HelloCls = type("Hello002", (object,), dict(hello=fn))
def demo004():
    print(type(Hello001))   #<class 'type'>
    print(type(HelloCls))   #<class 'type'>
    h1 = Hello001()
    h1.hello()
    h2 = HelloCls()
    h2.hello()


if __name__=='__main__':
    demo004()