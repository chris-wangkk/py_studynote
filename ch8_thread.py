# -*- coding: utf-8 -*-

#进程和线程
'''
1.多任务的实现有3种方式:
    多进程模式
    多线程模式
    多进程+多线程模式
Python既支持多进程，又支持多线程(还有同步、数据共享)
'''

#多进程 multiprocessing
'''
1.原生
fork()系统调用:把当前进程(父进程)复制了一份(子进程),然后分别在父进程和子进程内返回
    子进程永远返回0,父进程返回子进程的ID->父进程可记下每个子进程的ID,子进程只需要调用getppid()就可以拿到父进程ID
Py的os模块封装了常见的系统调用
2.multiprocessing 模块就是跨平台版本的多进程模块
    提供了一个Process类来代表一个进程对象
        start()     #启动子进程
        join()      #等待子进程结束后再继续往下运行(通常用于进程间的同步)
3.用进程池的方式批量创建子进程  Pool    from multiprocessing import Pool
    join()          #等待所有子进程执行完毕,调用join()之前必须先调用close(),调用 close()之后就不能继续添加新的 Process
4.子进程 subprocess     import subprocess
    启动一个子进程,控制其输入和输出
        子进程还需要输入,则可以通过communicate()方法输入
5.进程间通信
    py的multiprocessing模块包装了底层的机制,提供了Queue/Pipes等多种方式来交换数据
'''
import os, time, random
from multiprocessing import Process,Queue
from multiprocessing import Pool
import subprocess

def subdemo001():
    print('Process (%s) start...' % os.getpid())
    pid = os.fork()
    if 0 == pid:
        print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
def subdemo002():
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=("test",))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
def long_time_task(name):
    print("run task %s (%s)..." % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
def subdemo003():
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
def subdemo004():
    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)
def subdemo005():
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code:', p.returncode)
#在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)    #向队列写数据
        time.sleep(random.random())
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)
def subdemo006():
    q = Queue()     # 父进程创建Queue，并传给各个子进程
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()  #启动子进程pw，写入
    pr.start()  #启动子进程pr，读取
    pw.join()   #等待pw结束
    pr.terminate()  #pr进程里是死循环，无法等待其结束，只能强行终止
def demo001():
    #subdemo001()
    #subdemo002()
    #subdemo003()
    #subdemo004()
    subdemo006()

#多线程
'''
多任务可以由多进程完成，也可以由一个进程内的多线程完成
由于线程是操作系统直接支持的执行单元,Py的线程是真正的Posix Thread 而不是模拟出来的线程
1.Py的标准库提供了两个模块:_thread & threading
    _thread是低级模块
    threading是高级模块(对 _thread 进行了封装)
        current_thread()    #永远返回当前线程的实例
            如果不起名字Python就自动给线程命名为Thread-1,Thread-2...
2.Lock
    多进程:同一个变量各自有一份拷贝存在于每个进程中,互不影响;
    多线程:所有变量(在堆中)都由所有线程共享,故任何一个变量都可以被任何一个线程修改.
        -->线程之间共享数据需要有保护机制:无论多少线程,同一时刻最多只有一个线程持有该锁(可操作共享数据)
            创建一个锁: lock = threading.Lock()
            获取锁: lock.acquire()
                只有一个线程能成功地获取锁,然后继续执行代码,其他线程就继续等待直到获得锁为止
            释放锁: lock.release()
                获得锁的线程用完后一定要释放锁,否则那些苦苦等待锁的线程将永远等待下去,成为死线程
锁好处
    确保了某段关键代码只能由一个线程从头到尾完整地执行
锁坏处
    阻止了多线程并发执行(包含锁的某段代码实际上只能以单线程模式执行)
    死锁(多个线程全部挂起，既不能执行，也无法结束，只能靠操作系统强制终止)
3.关于多核CPU
现象:启动与CPU核心数量相同的N个线程(如在4核CPU上可以监控到CPU占用率仅有102%,也就是仅使用了一核)
-->Py的线程虽然是真正的线程,但解释器执行代码时有一个GIL锁(Global Interpreter Lock):
任何Py线程执行前必须先获得GIL锁,然后每执行100条字节码,解释器就自动释放GIL锁,让别的线程有机会执行.
因此这个GIL全局锁实际上把所有线程的执行代码都给上了锁,故多线程在Py中只能交替执行,即使100个线程跑在100核CPU上也只能用到1个核
--->在Py中可以使用多线程,但无法有效利用多核(如果一定要通过多线程利用多核,那只能通过C扩展来实现)
--->py可以通过多进程实现多核任务(多个Python进程有各自独立的GIL锁,互不影响)
'''
import time, threading
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)
def subdemo010():
    print('thread %s is running...' % threading.current_thread().name)  #当前线程(主线程)
    t = threading.Thread(target=loop, name="LoopThread")
    t.start()   #启动新的线程
    t.join()
    print('thread %s ended.' % threading.current_thread().name)
balance = 0
def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n   #计算balance + n，存入临时变量中；将临时变量的值赋给balance-->
    balance = balance - n
def run_thread(n):
    for i in range(2000000):
        change_it(n)
def subdemo011():
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
balance = 0
lock = threading.Lock()
def run_thread_ext(n):
    for i in range(10000):
        #获取锁
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()
def subdemo012():
    t1 = threading.Thread(target=run_thread_ext, args=(5,))
    t2 = threading.Thread(target=run_thread_ext, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
def demo002():
    subdemo012()

#ThreadLocal
'''
每个Thread可以对ThreadLocal对象可以读写操作且但互不影响,因为所操作的相关属性都是线程的局部变量(不用管理锁)
    可以理解为全局ThreadLocal变量是一个dict
    最常用的地方就是为每个线程绑定一个数据库连接,HTTP请求,用户身份信息等
'''
import threading
local_school = threading.local()
def process_student():
    std = local_school.std
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))
def process_thread(name):
    local_school.std = name
    process_student()
def demo003():
    t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
    t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
    t1.start()
    t2.start()
    t1.join()
    t2.join()

#进程 vs 线程
'''
1.多进程和多线程是实现多任务最常用的两种方式
要实现多任务,通常会设计Master-Worker模式:Master负责分配任务,Worker负责执行任务(多任务环境下通常是一个Master,多个Worker)
多进程模式:
    优点是稳定性高(一个子进程崩溃了,不会影响主进程和其他子进程,主进程除外),Apache早期模式
    缺点是创建进程的代价大,os能同时运行的进程数也是有限的(在内存和CPU的限制下太多进程会影响调度)
多线程模式:
    优点线程切换比进程切换开销小(但也不是非常明显)
    缺点任何一个线程挂掉都可能直接造成整个进程崩溃(不稳定),IIS服务器默认采用多线程模式
2.无论是多进程还是多线程,只要数量一多,效率肯定上不去,WHY?
    任务太多,OS会浪费大量时间进行线程切换,真正执行任务的时间反倒少
3.计算密集型 vs. IO密集型
    要最高效地利用CPU,计算密集型任务同时进行的数量应当等于CPU的核心数
    对于IO密集型任务,采用同步IO会导致大部分时间都在等待IO操作,性能太差(采用多进程/多先也会因2而导致性能问题)
    -->异步IO(事件驱动模型)
        Py中单线程的异步编程模型称为协程
'''


#分布式进程
'''
Py的multiprocessing模块不但支持多进程,其中managers子模块还支持把多进程分布到多台机器上:
    一个服务进程可以作为调度者,将任务分布到其他多个进程中,依靠网络通信
'''
#通过managers模块把Queue通过网络暴露出去,就可以让其他机器的进程访问Queue
import random, time, queue
from multiprocessing.managers import BaseManager
#发送任务的队列
task_queue = queue.Queue()
#接收结果的队列
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

def demo004():
    QueueManager.register('get_task_queue', callable=lambda: task_queue)
    QueueManager.register('get_result_queue', callable=lambda: result_queue)
    # 绑定端口5000, 设置验证码'abc':
    manager = QueueManager(address=('', 5000), authkey=b'abc')
    # 启动Queue:
    manager.start()
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    # 放几个任务进去:
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)
    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)
    # 关闭:
    manager.shutdown()
    print('master exit.')

if __name__=='__main__':
    demo003()