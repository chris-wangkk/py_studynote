#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#有关函数
'''
1.空函数
def nop():
    pass
2.参数检查
    调用函数时，如果参数个数不对，Python解释器会自动检查出来，并抛出TypeError
    如果参数类型不对，Python解释器就无法帮我们检查，直到运行出错
3.返回多个值
    实际上是一个tuple：返回一个tuple可以省略括号，而多个变量可以同时接收一个tuple，按位置赋给对应的值
'''

#函数参数
'''
1.默认参数
    def power(x, n=2):
    一是必选参数在前，默认参数在后
    注意：默认参数必须指向不变对象！
        Python函数在定义时，默认参数的值就被计算出来了
        def add_end(L=[]):
            L.append('END')
            return L
        默认参数L是一个变量，它指向对象[].
        每次调用该函数，改变了变量L(指向)的内容；则下次调用时，默认参数指向的内容就变了，不再是函数定义时的[]
2.可变参数
    def calc(*numbers):
    在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去（在函数调用时自动组装为一个tuple）
3.关键字参数
    def person(name, age, **kw):
    允许传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
4.命名关键字参数
--->参数组合
'''