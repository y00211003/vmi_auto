from csrclient import CSRClient
from vncclient import VNCClient
import rfb
import time
import threading
from constant import *
#import logging
from printlog import *


class FramebufferScript(threading.Thread):

    def __init__(self, client, mode):
        super(FramebufferScript, self).__init__()
        self.client = client
        self.use_mode = mode
        self.Need_request = False
        

    def run(self):
        result = []
        if self.use_mode == CSR_MODE:
            printTime()
            print 'In framebuffer, CSR client'
            self.client.sendRequestData()
        elif self.use_mode == VNC_MODE:
            printTime()
            print 'In framebuffer, VNC client'
            self.Need_request = True
        elif self.use_mode == X_MODE:
            printTime()        
            print 'In framebuffer, 264 client'
            self.Need_request = True
        time.sleep(15)
        while(self.Need_request):
            try:               
                if MUTEX.acquire():
                    self.client.requestFrameBuffer()
                    MUTEX.release()
                printTime()
                print 'frame buffer request sent'
                time.sleep(8)
            except Exception,e:
                printTime()
                print e

        
