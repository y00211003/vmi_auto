from csrclient import CSRClient
from vncclient import VNCClient
from rfb import KEY_Escape
import time
import threading
import random
from constant import *
#import logging
from printlog import *

defaultScript = [
    #{'action':'start', 'name':'start'},
    # {'action':'tap', 'name':'launcher', 'para':{'x':0x17c, 'y':0x2e9}},
    #{'action':'swipe', 'name':'swipe up 1', 'para':{'x0':0x154, 'y0':0x396, 'x1':0x154, 'y1':0x26f, 'step':2}},
    # {'action':'back', 'name':'back to google'},

]

class Script(threading.Thread):

    def __init__(self, client, mode):
        super(Script, self).__init__()
        self.client = client
        self.use_mode = mode

    def run(self):
        result = []
        printTime()
        print 'In Script'
        while(False):

            x = random.randint(10, 400)
            y = random.randint(20, 800)
            if MUTEX.acquire():
                self.client.pointerEvent(x, y, 1)
                self.client.pointerEvent(x, y, 0)
                MUTEX.release()
            printTime()
            print 'click at ['+str(x)+' : ' +str(y)+']'
            time.sleep(15)

        '''
        for item in self.script:
            action = item['action']
            name = item['name']
            print action + ' ' + name
            if action == 'start':
                self.client.sendRequestData()
                #result.append((item['name'], self.client.waitResponse(time.time(), 3)))
            elif action == 'tap':
                startSendTime = time.time()
                self.client.pointerEvent(item['para']['x'], item['para']['y'], 1)
                self.client.pointerEvent(item['para']['x'], item['para']['y'], 0)
                result.append((name, self.client.waitResponse(startSendTime, 3)))
            elif action == 'swipe':
                x0 = item['para']['x0']
                y0 = item['para']['y0']
                x1 = item['para']['x1']
                y1 = item['para']['y1']
                step = item['para']['step']

                startSendTime = time.time()
                self.client.pointerEvent(x0, y0, 1)

                if x0 == x1: # vertical swap
                    if y0 < y1:
                        ysteps = xrange(y0, y1, step)
                    else:
                        ysteps = xrange(y0, y1, -step)
                    for ypos in ysteps:
                        self. client.pointerEvent(x0, ypos, 1)
                elif y0 == y1: # horizon swap
                    if x0 < x1:
                        xsteps = xrange(x0, x1, step)
                    else:
                        xsteps = xrange(x0, x1, -step)
                    for xpos in xsteps:
                        self.client.pointerEvent(xpos, y0, 1)

                self.client.pointerEvent(x1, y1, 0)
                result.append((name, self.client.waitResponse(startSendTime, 3)))
            elif action == 'back':
                startSendTime = time.time()
                self.client.keyEvent(KEY_Escape, 1)
                self.client.keyEvent(KEY_Escape, 0)
                result.append((name, self.client.waitResponse(startSendTime, 2)))
        '''
        # print '\n---------------------------------------------------------------------------'
        # for item in result:
        #     print '%25s : %f, %f' % (item[0], item[1][0], item[1][1])
        # print '---------------------------------------------------------------------------'

        #return result
