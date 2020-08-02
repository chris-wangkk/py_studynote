# -*- coding: utf-8 -*-

#from collections import Iterable
from collections.abc import Iterable,Iterator

#切片
'''
处理对象：list,tuple,字符串
    obj[start:end]  #取start~end-1
'''
def trim(s):
    if 0 == len(s):
        return ''
    while ' ' == s[0]:
        s = s[1:]
        if 0 == len(s):
            return ''
    while ' ' == s[-1]:
        s = s[:-1]
        if 0 == len(s):
            return ''
    return s

def demo001():
    if trim('hello  ') != 'hello':
        print('测试失败!')
    elif trim('  hello') != 'hello':
        print('测试失败!')
    elif trim('  hello  ') != 'hello':
        print('测试失败!')
    elif trim('  hello  world  ') != 'hello  world':
        print('测试失败!')
    elif trim('') != '':
        print('测试失败!')
    elif trim('    ') != '':
        print('测试失败!')
    else:
        print('测试成功!')

#迭代
'''
迭代是通过for ... in来完成的(作用在可迭代对象)
    dict
        for key in d:                   #迭代k
        for value in d.values():        #迭代v
        for k, v in d.items():          #迭代k,v    
-->判断对象是否可迭代
from collections import Iterable
...
isinstance('abc', Iterable)         # str是否可迭代
...
'''
def demo002():
    print(isinstance("abc", Iterable))
    print(isinstance([1,2,3], Iterable))
    print(isinstance(123, Iterable))

#列表生成式
'''
[表达式 for循环（可能n个） {判断过滤语句}]
    表达式可以是 if ... else    --->用于结果表达
    过滤条件 if ... 不能带else  --->用于过滤
'''
def demo003():
    print([x * x for x in range(1, 11)])
    print([x+y+z for x in '123' for y in '456' for z in '789'])

#生成器
'''
1.在循环的过程中不断推算出后续的元素（一边循环一边计算的机制）
2.生成方式：
    (1)把一个列表生成式的[]改成()
    (2)一个函数定义中包含yield关键字
3.获取元素
    (1)通过next()函数获得generator的下一个返回值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误
    (2)for循环(generator也是可迭代对象)
4.vs 普通函数
执行流程不一样：
    函数是顺序执行，遇到return语句或者最后一行函数语句就返回
    在每次调用next()或for循环的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
'''
def fib(max):
    n,a,b = 0,0,1
    while n < max:
        yield b
        a, b = b, a+b
        n = n + 1
    return 'DONE'

def demo004():
    g = (x * x for x in range(10))
    print(type(g))  #<generator object <genexpr> at 0x1022ef630>
    for n in g:
        pass
        #print(n)
    f = fib(10)
    print(type(f))
    for n in f:
        print(n)

#迭代器
'''
1.可迭代对象(Iterable)和迭代器(Iterator)
Iterable直接作用于for循环,此外迭代器可以被next()函数调用并不断返回下一个值的对象
生成器都是迭代器，但list、dict、str虽然是Iterable，却不是Iterator
-->可以使用iter()把list、dict、str等Iterable变成Iterator
2.深度
(1)Py的Iterator对象表示的是一个数据流，可被next()调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误
(2)迭代器对象这个数据流看做是一个有序序列，但却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据
-->迭代器对象的计算是惰性的，只有在需要返回下一个数据时它才会计算
-->迭代器对象可以表示一个无限大的数据流（如全体自然数），而list等却不可能存储（一次性的）
    这里有点像C中的普通类对象指针（类型在编译时确定）和虚类对象指针（类型在运行时确定）
3.py的for循环本质上就是通过不断调用next()函数实现的
'''
def demo005():
    print(isinstance([],Iterable))
    print(isinstance([],Iterator))
    print(isinstance(iter([]),Iterator))
    print(isinstance('abc',Iterable))
    print(isinstance('abc',Iterator))
    print(isinstance(iter('abc'),Iterator))


if __name__ == '__main__':
    #demo001()
    demo005()