# -*- coding: utf-8 -*-



#模块定义
'''
函数/变量-->模板-->目录（包）
eg：
一个abc.py的文件就是一个名字叫abc的模块
避免abc与其他模块冲突，可以通过包来组织模块-->方法是选择一个顶层包名mycompany:
mycompany
├─ __init__.py
└─  abc.py
这样只要顶层的包名不与别人冲突即可（abc.py模块的名字就变成了mycompany.abc）
每一个包目录下面都会有一个__init__.py的文件，该文件是必须存在的，否则Py就把这个目录当成普通目录而不是一个包
__init__.py可以是空文件，也可以有Python代码
__init__.py本身就是一个模块，而它的模块名就是mycompany
注意不能和Python自带的模块名称冲突
    检查方法是在Python交互环境执行import 模块名，若成功则说明系统存在此模块
'''

#使用模块
'''
1.Python模块的标准文件模板:
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

(可选)任何模块代码的第一个字符串都被视为模块的文档注释
(可选)使用__author__变量把作者写进去

2.import sys
导入sys模块后就有了变量sys指向该模块，利用sys这个变量就可以访问sys模块的所有功能
    sys模块有一个argv变量，用list存储了命令行的所有参数
3.关于if __name__=='__main__':
命令行运行***模块文件时，Py解释器把一个***中的特殊变量__name__置为__main__；如在其他地方导入***模块时，if判断将失败
-->这种if测试可以让一个模块通过命令行运行时执行一些额外的代码(运行测试)

4.作用域
(1)正常的函数和变量名是公开的（public），可以被直接引用
(2)类似__xxx__这样的变量是特殊变量(__author__，__name__)，可以被直接引用，但是有特殊用途
(3)类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用
    Py并没有一种方法可以完全限制访问private函数或变量
'''

#安装第三方模块
'''
通过包管理工具pip完成
    Windows:确保安装时勾选了pip和Add python.exe to Path
    并存Python 3.x和Python 2.x时，对应的pip命令是pip3
第三方库都会在Python官方的pypi.python.org网站注册，要安装一个第三方库，必须先知道该库的名称，可以在官网或者pypi上搜索
pip安装命令：
    pip install 第三方库名
    -->Anaconda(一个基于Python的数据处理和科学计算平台，内置了许多非常有用的第三方库):装上Anaconda就相当于把数十个第三方模块自动安装好了

模块搜索路径
加载模块时Py会在指定的路径下搜索对应的.py文件，如果找不到，就会报错（ImportError: No module named ***）
默认情况下Py解释器会搜索当前目录、所有已安装的内置模块和第三方模块：搜索路径存放在sys模块的path变量中（sys.path）
-->添加自己的搜索目录
(1)直接修改sys.path(在运行时修改，运行结束后失效)
    import sys
    sys.path.append('****')
(2)设置环境变量PYTHONPATH
    该环境变量的内容会被自动添加到模块搜索路径中
'''

if __name__=='__main__':
    pass