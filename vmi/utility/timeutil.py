'''
Created on 2012-11-23

@author: Xiang Wang
'''

import time
def current_time_millis():
    t = time.time()
    return int(t * 1000)

def getCurrentMilliseconds():
    now = time.time()
    secs = int(now)
    milli = secs * 1000 + int(( now - secs) * 1000)
    return int(milli)

if __name__ == '__main__':
    print current_time_millis()
