# -*- coding: utf-8 -*-

#异步IO
'''
同步IO
    等待IO操作完成，才能继续进行下一步操作
    在IO操作的过程中，当前线程被挂起(阻塞)，而其他需要CPU执行的代码就无法被当前线程执行
-->方式1：多线程或者多进程来并发执行代码
缺点：
系统不能无上限地增加线程
由于系统切换线程的开销也很大,一旦线程数量过多,CPU的时间就花在线程切换上了,真正运行代码的时间就少了,结果导致性能严重下降
-->方式2：异步IO
机制：
当代码需要执行一个耗时的IO操作时,只发出IO指令并不等待IO结果,然后就去执行其他代码了.
一段时间后,当IO返回结果时再通知CPU进行处理
消息模型是如何解决同步IO必须等待IO操作这一问题的呢？
(1)当遇到IO操作时,代码只负责发出IO请求不等待IO结果,然后直接结束本轮消息处理并进入下一轮消息处理过程
(2)当IO操作完成后，将收到一条"IO完成"的消息,处理该消息时就可以直接获取IO操作结果
(3)在"发出IO请求"到"收到IO完成"的这段时间里
    同步IO模型下主线程只能挂起
    异步IO模型下主线程并没有休息,而是在消息循环中继续处理其他消息
        一个线程就可以同时处理多个IO请求且没有切换线程的操作(多路复用？)
        -->对于大多数IO密集型的应用程序,使用异步IO将大大提升系统的多任务处理能力
缺点：
如果按普通顺序写出的代码(同步IO模型的代码)实际上是没法完成异步IO的
    异步IO模型需要一个消息循环:在消息循环中,主线程不断地重复“读取消息-处理消息”这一过程
    loop = get_event_loop()
    while True:
        event = loop.get_event()
        process_event(event)
    在消息模型中，处理一个消息必须非常迅速，否则主线程将无法及时处理消息队列中的其他消息，导致程序看上去停止响应

'''

#协程
'''
又称微线程 Coroutine
1.vs 子程序
子程序(函数)调用是通过栈实现的,一个线程执行一个子程序,子程序调用总是一个入口，一次返回，调用顺序是明确的
协程的调用和子程序不同:执行过程中在子程序内部可中断,然后转而执行别的子程序(非函数调用),在适当的时候再返回来接着执行
2.vs 多线程
执行过程有点像多线程,但~~
(1)子程序切换不是线程切换,而是由程序自身控制,没有线程切换的开销-->协程的性能优势就越明显
(2)不需要多线程的锁机制,只有一个线程不存在同时写变量冲突,在协程中控制共享资源不加锁,只需要判断状态就好
-->利用多核CPU?
    多进程+协程
3.py对协程的支持是通过generator实现的
(1)在generator中,不但可以通过for循环来迭代,还可以不断调用next()函数获取由yield语句返回的下一个值
(2)Py的yield不但可以返回一个值,它还可以接收调用者发出的参数
'''
#生产者-消费者模型
def consumer():
    r = ""
    while True:
        n = yield r #发送消息r给外层，同时等接收n
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = "200 OK"
def producer(c):
    c.send(None)    #启动生成器但没有接收数据（首次其实是无数据）
    n = 0
    while n < 5:
        n += 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)   #切换到c，发送数据n，同时等接收r
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()   #关闭
def demo001():
    c = consumer()  #创建一个消费者generator
    producer(c)     #创建一个生成者generator

#asyncio
'''
Python 3.4版本引入的标准库，直接内置了对异步IO的支持
    编程模型就是一个消息循环:
        从asyncio模块中直接获取一个EventLoop的引用,然后把需要执行的协程扔到EventLoop中执行,就实现了异步IO
        1.用asyncio提供的 @asyncio.coroutine 可以把一个generator标记为coroutine类型
        2.异步操作需要在 coroutinue 中通过 yield from 完成
        3.多个 coroutinue 可以封装成一组 task 然后并发执行
'''
import threading
import asyncio

@asyncio.coroutine  #把一个generator标记为coroutine类型
def hello():
    print('Hello world! (%s)' % threading.currentThread())  #两个coroutine是由同一个线程并发执行的
    # 异步调用asyncio.sleep(1):
    r = yield from asyncio.sleep(1) #调用另一个generator(asyncio.sleep()也是一个coroutine,线程不会等待,而是直接中断并执行下一个消息循环)
    print('Hello again! (%s)' % threading.currentThread())
def demo002():
    # 获取EventLoop:
    loop = asyncio.get_event_loop()
    # 执行coroutine
    loop.run_until_complete(hello())    #coroutine扔到EventLoop中执行
    print("step001")
    # 执行2个
    tasks = [hello(), hello()]
    loop.run_until_complete(asyncio.wait(tasks))    #两个hello之间不会阻塞
    print("step002")
    loop.close()

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect #切换到connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))    #发送请求（写）
    yield from writer.drain()   #等待写完
    while True:
        line = yield from reader.readline() #切换到读操作
        if line == b'\r\n': #读完
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()
def demo003():
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

#async/await
'''
为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await
要使用新的语法，只需要做两步简单的替换
    1.把 @asyncio.coroutine 替换为 async
    2.把 yield from 替换为 await
'''
@asyncio.coroutine
def old_hello():
    print("Hello world!")
    r = yield from asyncio.sleep(1)
    print("Hello again!")
#--->
async def new_hello():
    print("Hello world!")
    r = await asyncio.sleep(1)
    print("Hello again!")

#aiohttp
'''
asyncio可以实现单线程并发IO操作,把其用在服务器端:由于HTTP连接就是IO操作,因此可以用单线程+coroutine实现多用户的高并发支持
asyncio实现了TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架
'''
#一个HTTP服务器
import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')
async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))
async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 1256)
    print('Server started at http://0.0.0.0:1256...')
    return srv
def demo004():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__=='__main__':
    demo004()