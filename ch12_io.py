# -*- coding: utf-8 -*-

#IO编程
'''
input:  从外部接收数据
output: 往外部发送数据
-->
同步IO(等待IO执行的结果)
异步IO(不等待IO执行的结果)
    轮询模式
    回调模式
'''

#文件读写
'''
读写文件就是请求操作系统打开一个文件对象(文件描述符),通过操作系统提供的接口从这个文件对象中读取数据.
1.读文件(内置)
    f = open('文件路径', '标识符')  #标识符 r/rb
    如果文件不存在,open()函数就会报错IOError
    如果文件打开成功,read()可以一次读取文件的全部内容,并把内容读到内存(用一个str对象表示)
    要读取二进制文件(如图片,视频等),用'rb'模式打开文件
    --->
        (1)调用read(size)读取size个字节的数据
        (2)调用readlines()读取行数据
file-like Object
    有个read()方法的对象
    不要求从特定类继承,只要写个read()方法就行(鸭子理论)
读取时默认的字符编码是UTF-8-->对于非UTF-8编码的文件,需要给open()函数传入encoding参数
eg:读取GBK编码的文件
    f = open('文件路径', 'r', encoding='gbk')
    ...
有些编码不规范的文件,读取时会导致 UnicodeDecodeError-->open()函数还接收一个errors参数,表示如果遇到编码错误后如何处理(一般就是忽略)
eg:
    f = open('文件路径', 'r', encoding='gbk', errors='ignore')
    ...
2.写文件(内置)
    和读文件是一样的,唯一区别是调用open()函数时,传入标识符  w/wb/a/ab
    可反复调用write()来写入文件,但是务必要调用f.close()来关闭文件
    写文件时,OS往往不会立刻把数据写入磁盘,而是放到内存缓存起来等空闲时再慢慢写入(写延迟).
        (1)调用close()方法时,OS才保证把没有写入的数据全部写入磁盘
        (2)遇到换行符'\n'或缓存区的数据积累到一定的量时
        -->即时写入文件
            print()函数有个参数叫"flush",设为True
    要写入特定编码的文本文件:在open()函数传入encoding参数(将字符串自动转换成指定编码)
3.调用close()方法关闭文件
    文件使用完毕后必须关闭(因为文件对象会占用操作系统的资源,并且操作系统同一时间能打开的文件数量也是有限的,不然提示资源耗尽)
    由于文件读写时都有可能产生IOError,一旦出错后面的f.close()就不会调用,故为了保证无论是否出错都能正确地关闭文件:
    with open('文件路径', '标识符') as f:
        ...
'''

#StringIO和BytesIO
'''
StringIO
在内存中读写str(操作的只能是str)
    1.创建一个StringIO,像文件一样调用write方法写入(和读写文件具有一致的接口)
    2.getvalue()方法用于获得写入后的str
    3.可以用一个str初始化StringIO,像读文件一样读取
BytesIO
在内存中读写bytes(操作二进制数据)
    1.创建一个BytesIO,像文件一样调用write方法(和读写文件具有一致的接口)
'''
from io import StringIO,BytesIO
def demo003():
    f1 = StringIO()
    f1.write("abc")
    f1.write(" ")
    f1.write("xyz")
    print(f1.getvalue())
    #
    f2 = StringIO('Hello!\nHi!\nGoodbye!')
    while True:
        s = f2.readline()   #按行读取
        if "" == s:
            break
        print(s.strip())
def demo004():
    f3 = BytesIO()
    f3.write("深度学习".encode('utf-8'))
    print(f3.getvalue())    #bytes
    #
    f4 = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
    print(f4.read())

#操作文件和目录
'''
操作系统提供的命令只是简单地调用了操作系统提供的接口函数
    Py内置的os模块也可以直接调用操作系统提供的接口函数
1.os.name       # 操作系统类型
    posix:  Linux,Unix,Mac OS X
    nt:     Windows
2.os.uname()    # 详细的系统信息(在Windows上不提供,os模块的某些函数是跟操作系统相关的)
3.环境变量
在操作系统中定义的环境变量,全部保存在 os.environ 这个变量中
    要获取某个环境变量的值,可以调用 os.environ.get('key')
4.操作文件和目录
对应接口一部分放在 os 模块中,一部分放在 os.path 模块中
    os.path.join()      #把两个路径合成一个(不要直接拼字符串)
        可以正确处理不同操作系统的路径分隔符
    os.mkdir(...)                   #创建一个目录
    os.rmdir(...)                   #删掉一个目录
    os.path.split(...)              #拆分路径(最后级别的目录或文件名)
    os.path.splitext()              #得到文件扩展名
        这些合并/拆分路径的函数并不要求目录和文件要真实存在,它们只对字符串进行操作
    os.rename(old_name, new_name)   #对文件重命名
    os.remove(...)                  #删掉文件
    复制文件并非由操作系统提供的系统调用
        shutil模块提供了copyfile()的函数
'''
import os
def demo005():
    print(os.name)
    print(os.uname())
    print(os.environ)
    print(os.path.abspath('.')) #查看当前目录的绝对路径
#列出当前目录下的所有目录
def demo006():
    print([x for x in os.listdir('.') if os.path.isdir(x)])
    print('-----------------------------------')
    print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'])

#序列化
'''
1.术语
    把变量从内存中变成可存储或传输的过程称之为序列化(Python中叫pickling).序列化后,就可以把序列化后的内容写入磁盘或通过网络传输到别的机器上
    把变量内容从序列化的对象重新读到内存里称之为反序列化(unpickling)
2.Python提供了pickle模块来实现序列化
    pickle.dumps()      #把任意对象序列化成一个bytes
    pickle.dump()       #直接把对象序列化后写入一个file-like Object
    pickle.loads()      #反序列化一个bytes出对象
    pickle.load()       #从一个file-like Object中直接反序列化出对象
    what a pity! -->pickle 只能用于Python
3.JSON
Python内置的json模块提供了非常完善的Python对象到JSON格式的转换
    json.dumps()    #序列化返回一个str
    json.dump()     #直接把JSON写入一个file-like Object
    json.loads()    #把JSON的字符串反序列化
    json.load()     #从file-like Object中读取字符串并反序列化
JSON标准规定JSON编码是UTF-8,故总是能正确地在Python的str与JSON的字符串之间转换
--->
Python的dict对象可以直接序列化为JSON的{},若尝试序列化一个class对象则会报错TypeError(对象不是一个可序列化为JSON的对象)
让dumps()知道如何将类实例变为一个JSON的{}对象
    +可选参数default:为对应的类专门写一个转换函数(实例转换为dict),再把函数传进去即可
    eg:
        json.dumps(s, default=***)
        -->把任意class的实例变为dict
            json.dumps(s, default=lambda obj: obj.__dict__)
    --->反序列化场景
        json.loads(json_str, object_hook=***)   #object_hook负责把dict转换为对应类实例
'''
import pickle
import json
def demo001():
    #
    d1 = dict(name='Bob', age=20, score=88)
    print(pickle.dumps(d1))
    d2 = pickle.loads(pickle.dumps(d1))
    print(d2)
def demo002():
    d = dict(name='Bob', age=20, score=88)
    print(json.dumps(d))
    print(json.loads(json.dumps(d)))

if __name__=='__main__':
    demo006()