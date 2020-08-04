# -*- coding: utf-8 -*-

##web
'''
CS架构---问题:Web应用程序的修改和升级非常频繁,CS架构需要每个客户端逐个升级桌面App(太慢)
-->BS架构:客户端只需要浏览器,应用程序的逻辑和数据都存储在服务器端
    浏览器只需要请求服务器,获取Web页面并把Web页面展示给用户即可

Web开发也经历了好几个阶段:
1.静态Web页面:请求的内容是静态的HTML页面
2.CGI:+与用户交互,要处理用户发送的动态数据,出现了Common Gateway Interface
3.ASP/JSP/PHP:脚本语言开发效率高与HTML结合紧密
4.MVC:解决直接用脚本语言嵌入HTML导致的可维护性差的问题,引入了Model-View-Controller模式
'''

##HTTP
'''
服务器把网页传给浏览器(实际上就是把网页的HTML代码发送给浏览器,让浏览器显示出来)
'''

##HTML
'''
1.HTML定义了一套语法规则,来告诉浏览器如何把一个页面显示出来
2.CSS(Cascading Style Sheets(层叠样式表)的简称),用来控制HTML里的所有元素如何展现
3.JavaScript是为了让HTML具有交互性而作为脚本语言添加的(JavaScript既可以内嵌到HTML中,也可以从外部链接到HTML中)
-->HTML定义了页面的内容,CSS来控制页面元素的样式,JavaScript负责页面的交互逻辑
4.用Python或者其他语言开发Web应用时,就是要在服务器端动态创建出HTML或者构造HTML里的数据
--->
WEB应用本质:
1.浏览器发送一个HTTP请求
2.服务器收到请求,生成一个HTML文档
3.服务器把HTML文档作为HTTP响应的Body发送给浏览器
4.浏览器收到HTTP响应,从HTTP Body取出HTML文档并显示
'''

##WSGI接口
'''
1.一般主要工作是在步骤3中(HTML文档或其中的数据),124则会在底层代由专门的服务器软件实现,对上层业务提供一个统一的接口:
--->WSGI: Web Server Gateway Interface
其接口定义只要求Web开发者实现一个函数,就可以响应HTTP请求
def application(environ, start_response):
    ...
其中:
envirion:       一个包含所有HTTP请求信息的dict对象
start_response: 一个发送HTTP响应的函数
    eg:
        ...
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'<h1>Hello, web!</h1>']
(1)Header只能发送一次,也就是只能调用一次start_response()函数
(2)start_response()函数接收两个参数:
    一个是HTTP响应码
    一个是一组list表示的HTTP Header,每个Header用一个包含两个str的tuple表示
(3)函数的返回值(如 b'<h1>Hello, web!</h1>')将作为HTTP响应的Body发送给浏览器
-->开发时只需了解如何从environ这个dict对象拿到HTTP请求信息,然后构造HTML,通过start_response()发送Header,最后返回Body
    业务代码只负责在更高层次上考虑如何响应请求就可以了
2.application()函数怎么调用？
application()函数必须由WSGI服务器来调用
(1)Python内置了一个WSGI服务器,这个模块叫wsgiref(用纯Python编写的WSGI服务器的参考实现)
    既然是参考,仅供开发和测试使用,效率嘛~~~
'''
from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]

def demo001():
    ## 创建一个服务器，IP地址为空，端口是8000，处理函数是application
    httpd = make_server('', 8000, application)
    print('Serving HTTP on port 8000...')
    httpd.serve_forever()

##使用Web框架
'''
WEB应用很复杂的,一般要在WSGI之上再抽象出Web框架,进一步简化Web开发:
1.有了Web框架,在编写Web应用时,注意力就从WSGI处理函数转移到URL+对应的处理函数
2.在编写URL处理函数时,除了配置URL外,从HTTP请求拿到用户数据也是非常重要的(Web框架都提供了自己的API来实现这些功能)
'''

##使用模板
'''

'''


if __name__=='__main__':
    demo001()