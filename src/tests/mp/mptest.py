# -*- coding:utf-8 -*-
"""
@NAME: mptest.py
@Auth: dabin
@Date: 2025/4/28
"""
from multiprocessing import Process, Queue
import os

# def info(name):
#     print('Hello %s!' % name)
#     print('module name: %s' % __name__)
#     print('module path: %s' % __file__)
#     print('process id: %s' % os.getpid())
#     print('parent process id: %s' % os.getppid())
#
# def f(name):
#     info(name)
#     print('hello %s!' % name)
#
# if __name__ == '__main__':
#     p = Process(target=f, args=('John',))
#     p.start()
#     p.join()

import multiprocessing as mp
def foo(q):
    q.put([42, None, 'hello world'])

if __name__ == '__main__':
    mp.set_start_method("spawn", True)
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(p.is_alive())
    print(q.qsize())
    print(q.get())
    p.join()
