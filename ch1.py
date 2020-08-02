#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#基础
##数据类型和变量
'''
第一点：py是动态语言（与之对应的是静态语言，在定义变量时必须指定变量类型）
第二点：变量在计算机内存中的表示
a = 'ABC'
--> Python解释器干了两件事情：
1.在内存中创建了一个'ABC'的字符串；
2.在内存中创建了一个名为a的变量，并把它指向'ABC'
b = a
--> 实际上是把变量b指向变量a所指向的数据（见demo001）
第三点：关于常量（不能变的变量）
py没有任何机制保证常量不被修改，习惯上用全部大写的变量名表示常量
第四点：
/   除法计算结果是浮点数，即使是两个整数恰好整除，结果也是浮点数
//  地板除，两个整数的除法仍然是整数
'''
def demo001():
    a = 'ABC'   #a是变量，b是字符串对象，变量a指向一个字符串对象
    b = a
    a = 'XYZ'
    print(b)    # ABC

##字符串和编码
'''
第一点：原因+历史
1.计算机只能处理数字，如果要处理文本，就必须先把文本转换为数字才能处理
2.ASCII编码（占用一个字节，包括大小写英文字母、数字和一些符号）
    -->问题：其他语言呢？GB2312（中国），Shift_JIS（日本）...在多语言混合的文本中，显示出来会有乱码
    -->解决：Unicode编码（通常是2个字节，如要用到非常偏僻的字符就需要4个字节）
    -->问题：若全英文文本用Unicode编码比ASCII编码需要多一倍的存储空间（浪费存储，传输更慢）
    -->解决：UTF-8编码（可变长：把一个Unicode字符根据不同数字大小编码成1-6个字节，常用英文字母占1字节（兼容ASCII），汉字占3字节）
3.计算机系统通用的字符编码工作方式
在内存中统一使用Unicode编码，当需要保存到硬盘或者需要传输时（写入），就转换为UTF-8编码；
从文件或网络（读取）的UTF-8字符被转换为Unicode字符到内存里进行处理
第二点：python的字符串
1.py2没统一，有<type 'str'> （由 Unicode 经过编码(encode)后的字节组成的）和 <type 'unicode'>，故经常出现编解码问题
2.Py3版中2字符串是以Unicode编码的，故Py3的字符串支持多语言
    ord()   获取字符的整数表示  ord('中')
    chr()   编码转换为对应的字符    chr(25991)
Python的字符串类型是str（在内存中以Unicode表示），一个字符对应若干个字节
-->如果要在网络上传输或者保存到磁盘上，就需要把str变为以字节为单位的bytes类型（用带b前缀的单引号或双引号表示）
以Unicode表示的str通过encode()方法可以*编码*为指定的bytes：
    'ABC'.encode('ascii')   //按ascii编码
    '中文'.encode('utf-8')  //按utf-8编码
    '中文'.encode('ascii')  //超出编码范围的会报错
-->从网络或磁盘上读取了字节流数据就是bytes
要把bytes变为str，需要用decode()解码
    b'ABC'.decode('ascii')  //按ascii解码
    b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8') //按utf-8解码
如bytes中包含无法解码的字节，decode()方法会报错：
    b'\xe4\xb8\xad\xff'.decode('utf-8', errors='ignore')    //传入errors='ignore'忽略错误的字节
关于长度：
len(obj)    //obj是str计算str的字符数，换成bytes就计算字节数
    len('中文')                     //2
    len('中文'.encode('utf-8'))     //6（1个中文字符经过UTF-8编码后通常会占用3个字节）
4.Python源代码
Python源代码也是一个文本文件，当源代码中包含中文时，在保存源代码时就需要指定保存为UTF-8编码
当Python解释器读取源代码时，为了让它按UTF-8编码读取：
#!/usr/bin/env python3                      告诉Linux/OS X系统，这是一个Python可执行程序
# -*- coding: utf-8 -*-                     按照UTF-8编码读取源代码
5.格式化输出
     'Hi, %s, you have $%d.' % ('Michael', 1000000)
'''
def demo002():
    print(len('中文'))
    print(len('中文'.encode('utf-8')))

##循环
'''
1.for...in循环
    for name in names:
    # range()返回range对象，通过list(**)可转换为一个整数序列
2.while 循环
    while 条件语句:
'''
def demo003():
    print(list(range(10)))
    print(type(range(10)))

##使用list和tuple
'''
list    列表（有序的集合，可以随时添加和删除其中的元素，元素类型可以不同）  list()  or  []
    1.索引是从0开始，当索引超出了范围时会报一个IndexError错误
    2.一个可变的有序表：
        l1.append(obj)          #追加元素到末尾
        l1.insert(idx, obj)     #把元素插入到指定的位置之前
        l1.pop()                #要删除list末尾的元素并返回
        l1.pop(idx)             #删除指定位置的元素
tuple   元组（一旦初始化就不能修改，注意是指向不变）                    ()
    只有1个元素的tuple定义时必须加一个逗号,
dict    字典（键值对）              dict()  or {}
    1.如果key不存在，dict就会报错
    -->避免key不存在的错误
    (1)通过in判断key是否存在
        key in dict     #不存在则返回false
    (2)get()方法：如果key不存在则返回None或指定的value
        dict.get(key)
        dict.get(key, specific-val)
    2.删除一个key
        pop(key)        #对应的value也会从dict中删除
    3.dict内部存放的顺序和key放入的顺序是没有关系的
    4.vs list:
        dict查找和插入的速度极快，不会随着key的增加而变慢（list相反）
        list占用空间小，浪费内存很少（dict相反）
        -->dict是用空间来换取时间
    5.key必须是不可变对象
        dict根据key来计算value的存储位置，如果每次计算相同的key得出的结果不同就存在问题
        eg:
            不可变：字符串、整数等
            可变：list
set     集合（无序和无重复元素的集合）        set()   or  {}
    add(key)        可以添加元素到set中（重复添加但不会有效果）
    remove(key)     删除元素
    两个set可以做数学意义上的交集、并集等操作
        s1 & s2
        s1 | s2
    vs dict:
        唯一区别仅在于没有存储对应的value，同样不可以放入可变对象，否则无法保证set内部“不会有重复元素”
'''

if __name__ == '__main__':
    demo003()