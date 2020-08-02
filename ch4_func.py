# -*- coding: utf-8 -*-

#函数式编程
##高阶函数
'''
1.变量可以指向函数
    <built-in function func_name>
2.函数名也是变量(这里和C不同，C是改不了了的)
3.一个函数就可以接收另一个函数作为参数，即高阶函数
    def add(x, y, f):
        return f(x) + f(y)
'''
def nothing():
    return 100

def demo001():
    global nothing
    obj1 = nothing()
    obj2 = nothing  #变量可以指向函数
    print(type(obj1))
    print(type(obj2))
    print(type(nothing))
    nothing = 123   #函数名也是变量，更改后就不能再做函数调用了
    print(type(nothing))

###map/reduce
'''
1.map()函数接收两个参数，一个是函数，一个是Iterable
    将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator(这里是迭代器，故要一次性计算需转换下)返回
2.reduce()把一个函数作用在一个序列上（该函数接收两个参数），把结果继续和序列的下一个元素做累积计算
    reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
'''
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2int(s):
    def char2num(strObj):
        return DIGITS[strObj]
    def fn(x, y):
        return x * 10 + y
    return reduce(fn, map(char2num, s))

def demo002():
    print(str2int("123456"))

def normalize(name):
    name = name.lower()
    name = name.replace(name[0], name[0].upper())
    name = name.replace(name[1:], name[1:].lower())
    return name

def prod(L):
    def f1(x, y):
        return x * y
    return reduce(f1, L)

def str2float(s):
    flag = False
    cnt = 0
    def f1(strObj):
        return DIGITS[strObj]     
    def f2(x, y):
        return x * 10 + y

    if '.' in s:
        ss = s.split('.')
        n = 10
        for _ in range(1,len(ss[1])):
            n *= 10
        s1 = ss[0] + ss[1]
        return reduce(f2, map(f1, s1))/n
    else:
        return reduce(f2, map(f1, s))

def demo003():
    L1 = ['adam', 'LISA', 'barT']
    L2 = list(map(normalize, L1))
    print(L2)
    ###
    print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
    if prod([3, 5, 7, 9]) == 945:
        print('测试成功!')
    else:
        print('测试失败!')
    ###
    print('str2float(\'123.456\') =', str2float('123.456'))
    if abs(str2float('123.456') - 123.456) < 0.00001:
        print('测试成功!')
    else:
        print('测试失败!')

###filter
'''
用于过滤序列(筛选),接收一个函数和一个序列
filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
返回的是一个Iterator，也就是一个惰性序列，要强迫filter()完成计算结果，需要用list()函数获得所有结果并返回list
'''
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
#过滤出非整数
def _not_divisible(n):
    return lambda x: x % n > 0
#求素数（生成器）
def primes():
    yield 2
    it = _odd_iter()    #初始序列（奇数集3,5,7...）
    while True:
        n = next(it)    #返回序列的第一个数(首次为3)
        it = filter(_not_divisible(n), it) #基于过滤系统构造新的序列，想下写为_not_divisible时会发生什么
        yield n
#回数
def is_palindrome(n):
    obj = n
    res = 0
    while obj >= 1:
        res = res * 10 + obj % 10
        obj //= 10
    if res == n:
        return True
    else:
        return False

def demo004():
    for n in primes():
        if n < 50:
            print(n)
        else:
            break
    #
    output = filter(is_palindrome, range(1, 200))
    print('1~200:', list(output))

###sorted
'''
sorted()函数是一个高阶函数，可以接收一个key函数来实现自定义的排序,同时安排第三个参数reverse=True控制是否反向排序
key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序(sorted()函数按照keys进行排序,并按照对应关系返回list相应的元素)
'''
def by_name(t):
    return t[0]
def by_score(t):
    return t[1]
def demo005():
    L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    L2 = sorted(L, key=by_name)
    print(L2)
    L3 = sorted(L, key=by_score, reverse=True)
    print(L3)

##返回函数
'''
1.函数的返回对象是函数，即使函数里提供了参数，返回的还是函数对象
2.-->闭包
返回的函数在其定义内部引用了局部变量，所以当一个函数返回了一个函数后，其内部的局部变量还被新函数引用(和C不同，此时局部变量不是栈对象而是逃逸了，用计数控制GC)
返回的函数并没有立刻执行，而是直到调用了f()才执行-->返回函数不要引用任何循环变量，或者后续会发生变化的变量
'''
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

def subdemo001(l):
    def f1():
        print(l)
    return f1
#计数器
def createCounter():
    i = [0]
    #i = 0     
    def counter():
        i[0] += 1   #闭包情况：不可变对象可读不可写（另一块数据），可变对象可读写？？
        #i += 1  #报错,没有让解释器清楚变量是全局变量还是局部变量
        return i[0]
        #return i
    return counter

def demo006():
    f = lazy_sum(1, 3, 5, 7, 9) #每次调用都会返回一个新的函数，即使传入相同的参数
    f1 = lazy_sum(1, 3, 5, 7, 9)
    f2 = lazy_sum(1, 3, 5, 7, 9)
    print(f)    #打印的函数类型，而不是计算值
    print(f())  #这样才会返回值
    print(f1 == f2)
    print(f1() == f2())
    #
    f1, f2, f3 = count()
    print(f1()) #9
    print(f1()) #9
    print(f1()) #9
    l = [1,2,3]
    f1 = subdemo001(l)
    f2 = subdemo001(l)
    f1()    #1,2,3
    l.append(4)
    f2()    #1,2,3,4
    #
    counterA = createCounter()
    print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
    counterB = createCounter()
    if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
        print('测试通过!')
    else:
        print('测试失败!')

##匿名函数
'''
关键字lambda表示匿名函数，冒号前面的x表示函数参数
匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果
匿名函数也是一个函数对象，也可以把匿名函数赋值给一个变量，再利用变量来调用该函数
    lambda 参数列表: 表达式
'''
def is_odd(n):
    return n % 2 == 1
def demo007():
    L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
    print(L)


##装饰器
'''
在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）
decorator就是一个返回函数的高阶函数:接受一个函数作为参数，并返回一个函数
    wrapper()函数的参数定义是(*args, **kw),可以接受任意参数的调用
    如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数
'''
import time, functools
def log(func):
    @functools.wraps(func)  #解决函数名变化问题
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper
@log                #now = log(now)
def now():
    print('2015-3-25')
#装饰器本身需要传入参数
def log(text):
    def decorator(func):    #返回装饰器函数（里面使用了给装饰器使用的参数）
        @functools.wraps(func)  #解决函数名变化问题
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))   #注意这里的名字变成了 wrapper
            return func(*args, **kw)
        return wrapper
    return decorator
@log('execute')     #now = log('execute')(now)
def now():
    print('2015-3-25')
#被装饰器后面添加处理（练习中实现）
#练习
def metric(fn):
    @functools.wraps(fn)  #解决函数名变化问题
    def wrapper(*args, **kw):
        print('%s executed in %s ms' % (fn.__name__, 10.24))
        ret = fn(*args, **kw)   #还要在后面加处理
        print("call %s finish" % fn.__name__)
        return ret
    return wrapper
@metric
def f1():
    print("aaa")
@metric
def f2():
    print("bbb")
def demo008():
    f1()
    f2()

##偏函数
'''
functools.partial就是帮助创建一个偏函数的
    functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数
'''
import functools
int2 = functools.partial(int, base=2)
def demo009():
    print(int2('1000000'))
    print(int2('1000000', base=10)) #int2函数，仅仅是把base参数重新设定默认值为2，但也可以在函数调用时传入其他值


if __name__ == '__main__':
    demo009()
