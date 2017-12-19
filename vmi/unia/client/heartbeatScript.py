from csrclient import CSRClient
from vncclient import VNCClient
import rfb
import time
import threading
from constant import *
#import logging
from printlog import *



class HeartbeatScript(threading.Thread):

    def __init__(self, client, mode):
        super(HeartbeatScript, self).__init__()
        self.client = client
        self.use_mode = mode

    def run(self):
        result = []
        printTime()
        print 'In HeartBeatScript'
        
        while(True):
            time.sleep(10)
            if MUTEX.acquire():
                self.client.sendHeartBeat()               
                MUTEX.release()
            printTime()
            print 'heart beat sent'

            
        
