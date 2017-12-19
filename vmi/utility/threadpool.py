'''
Created on 2012-12-18

@author:  xiang wang
'''
from Queue import Queue
from threading import Thread
from logger import Logger

_logger = Logger(__name__)

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception, e:
                _logger.exception(e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kwargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

if __name__ == '__main__':
    from random import randrange
    from time import sleep

    delays = [randrange(1, 10) for i in range(100)]

    def wait_delay(d):
        print 'sleeping for (%d)sec' % d
        sleep(d)

    pool = ThreadPool(20)

    for i, d in enumerate(delays):
        pool.add_task(wait_delay, d)

    pool.wait_completion()
