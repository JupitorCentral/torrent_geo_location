from ast import While, arg
from audioop import mul
from glob import glob
from multiprocessing import Process, Pool, cpu_count, Lock
import multiprocessing
import os, queue
from time import sleep


def f(q:multiprocessing.Queue, rst:multiprocessing.Queue):


    while True:
        try:
            x = q.get_nowait()
        except queue.Empty:
            break
        else:
            print(x)
            # rst.append(x*x)
            rst.put(x*x)
            sleep(.3)
    
    return True


if __name__ == '__main__':


    q = multiprocessing.Queue()
    rst = multiprocessing.Queue()

    for i in range(10):
        q.put(i)

    procs = []
    while not q.empty():
        proc = multiprocessing.Process(target=f, args=(q, rst))
        print('start process')
        sleep(0.1)
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    rst.put('STOP')
    for i in iter(rst.get, 'STOP'):
        print(i, end=' ')

    print('end')