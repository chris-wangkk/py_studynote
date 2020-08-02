# -*- coding: utf-8 -*-

#类和实例
'''
1.类的定义
class 类名(父类，如没有合适的继承类就使用object类):
    ...    
2.定义类对象
obj = 类名()    //变量obj指向的就是一个类实例
3.类方法定义
    除了第一个参数是self（指向创建的实例本身）外，其他（定义和调用）和普通函数一样
    def funcname(self, ...):
        ...
    --->一些特殊方法:
    (1)创建类实例
        def __init__(self, ...):
    (2)返回长度
        __len__()
        调用len()函数试图获取一个对象的长度,内部实际自动去调用该对象的__len__()方法，如下是等价的
            len('ABC')
            'ABC'.__len__()
    (3)用于'print(类实例)'时调用（返回用户看到的）
        __str__()
    (4)交互模式时直接显示变量（返回程序开发者看到）
        __repr__()
    (5)想被用于for ... in循环
        __iter__()
        __iter__()返回一个迭代对象,然后Py的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值,直到StopIteration错误时退出循环
    (6)像list那样按照下标取出元素
        __getitem__(self, idx/slice)
        内部需要判断传入的类型是int还是切片
        如把对象看成dict,__getitem__()的参数也可能是一个可以作key的object
        --->
        __setitem__()   #把对象视作list或dict来对集合赋值
        __delitem__()   #用于删除某个元素
        注意：通过上面的方法，自定义的类表现得和Py自带的list,tuple,dict没什么区别
    (7)动态返回一个attr属性(或方法)
        __getattr__(self, attr)
        当调用不存在的属性时如score,Py解释器会试图调用 __getattr__(self, 'score')来尝试获得属性
        注意：
            只有在没有找到属性的情况下，才调用 __getattr__
            __getattr__ 默认返回是None,要让class只响应特定的几个属性需自行抛出AttributeError的错误
        -->
        可以把一个类的所有属性和方法调用全部动态化处理了，不需要任何特殊手段
    (8)直接在实例本身上调用(把对象看成函数)
        __call__
        当遇到 实例() 时即调用,self参数不要传入
        怎么判断一个变量是对象还是函数呢？
        能被调用的对象就是一个Callable对象(带有__call__()的类实例)
            通过callable()函数可以判断一个对象是否是可调用对象
4.类方法调用
    类对象.方法名(...)
5.Py允许动态对实例变量绑定任何新的数据，即对于两个实例变量，虽然它们都是同一个类的不同实例，但可能拥有不同的变量名
    obj1 = Cls001()
    obj2 = Cls001()
    obj1.sub001 = 1     #动态绑定
    print(obj1.sub001)  #1
    print(obj2.sub001)  #报错   AttributeError: 'Cls001' object has no attribute 'sub001'
--->给实例绑定一个方法
    见实例
'''

#访问限制
'''
1.Py中实例的变量名如果以'__'开头，就变成了一个私有变量(只有内部可以访问，外部不能访问)
    强制访问会报错 AttributeError；强制做设置则只会动态新增一个这样的变量
    内部实现：Py解释器对外把'__name'变量名改成了'_类名__name'，按'_类名__name'能访问到（但不要这么搞）
-->
    一个下划线开头'_'的变量:约定为"虽然可以被访问,但请把视为私有变量,不要随意访问";
    类似__xxx__的变量:特殊变量(可访问，但有特殊用途)
'''
from types import MethodType

def funcobj2(obj):
    print(obj.a)
    print("func for obj2")
class Cls001(object):
    def __init__(self, a, b):
        self.a = a
        self.__b = b
    def get(self):
        print(self.a, self.__b)
def demo001():
    obj1 = Cls001(1,1)
    obj2 = Cls001(2,2)
    obj1.get()
    obj2.a = 20
    obj2.__b = 20
    obj2.get()
    #
    obj2.selfFunc = MethodType(funcobj2, obj2)  #这里不一定要传obj2，可以是一切非None的实例
    obj2.selfFunc()
#继承和多态
'''
class 子类名(父类名):
    ...
1.在继承关系中，如果一个实例的数据类型是某个子类，那它的数据类型也可以被看做是父类
2.传入的类型定义为父类，则具体调用时只要是父类及其子类，就会自动调用实际类型的方法（若无则用父类方法）
3.新增一种子类时，只要确保要调用的方法编写正确，不用管原来的代码是如何调用的，这就是著名的“开闭”原则:
    对扩展开放：允许新增子类；
    对修改封闭：不需要修改依赖父类类型的函数逻辑
4.vs静态语言
静态：传入的实例类型必须是父类及其子类，否则无法调用对应的方法（强关联，要求严格的继承体系）
动态：只需要保证传入的实例中有对应的方法就可以（组合形式，golang的interface也是如此，解耦了类之间的关系）
    动态语言的"鸭子类型"    file-like object
'''
class father(object):
    def f1(self, val):
        print("father is %s" % val) 
class son1(father):
    def f1(self, val):
        print("son1 is %s" % val) 
class son2(father):
    def f1(self, val):
        print("son2 is %s" % val) 
class likeson(object):
    def f1(self, val):
        print("likeson is %s" % val)
def callf1(obj):
    obj.f1(100)
def demo002():
    callf1(father())
    callf1(son1())
    callf1(son2())
    callf1(likeson())

#获取对象信息
'''
如何知道对象是什么类型、有哪些方法呢？
1.使用type()得到对象类型
    比较两个变量的type类型是否相同:
    if type(obj1) == type(obj2):
--->判断基本数据类型可以直接写int，str等，但如果要判断一个对象是否是函数？可以使用types模块中定义的常量
    types.FunctionType
    types.LambdaType
    ...
2.要判断class的类型，可以使用 isinstance()函数
    isinstance()判断的是一个对象是否是该类型本身或者位于该类型的父继承链上
    isinstance(obj, 类名)   #返回 True or False
--->判断一个变量是否是某些类型中的一种
    isinstance(obj, (类名1,类名2...))
3.获得一个对象的所有属性和方法，可以使用dir()函数
    返回一个包含字符串的list
4.操作一个对象的状态
    hasattr()
        hasattr(obj, 'x')   #有属性'x'吗？

    getattr()
        getattr(obj, 'y')       # 获取属性'y'，如果不存在则报错
        getattr(obj, 'y', 404)  # 获取属性'z'，如果不存在，返回默认值404
    setattr()
        setattr(obj, 'z', 19) # 设置一个属性'z'
--->获得对象的方法
    getattr(obj, 'power') # 获取属性'power'
    fn = getattr(obj, 'power') # 获取属性'power'并赋值到变量fn(fn指向obj.power)
    fn() # 调用fn()与调用obj.power()是一样的
'''
import types
def demo003():
    print(type(abs)==types.BuiltinFunctionType)
    print(type(lambda x: x)==types.LambdaType)
    print(type((x for x in range(10)))==types.GeneratorType)
    #
    obj = father()
    print(hasattr(obj, 'x'))
    setattr(obj, 'x', 10)
    print(hasattr(obj, 'x'))
    print(getattr(obj, 'x'))
    print(getattr(obj, 'y', 404))

#实例属性和类属性
'''
1.Py是动态语言，根据类创建的实例可以任意绑定属性
2.如类本身需要绑定一个属性呢？可以直接在class中定义属性，这种属性是类属性，归类所有
3.类属性虽然归类所有，但类的所有实例都可以访问到（所有实例共享一个属性）
4.属性名冲突情况下实例属性优先级比类属性高，因此会屏蔽掉类属性
'''

if __name__=='__main__':
    demo001()