'''
Created on 2013-12-18

@author: xinxin_fang
'''
import rfb
import time
import datetime
import threading
from struct import pack, unpack
from zlib import decompress
from twisted.internet.defer import Deferred
from twisted.internet import reactor
from statistics import stats, statsWriter
from constant import *

X_REQUEST_DATA_ENCODING = 73


class XClient(rfb.RFBClient, object):

    def __init__(self):
        super(XClient, self).__init__()      
        self._header = X_HEADER
        #self._lastReceiveTime = 0
        #self._lastRecvTimeLock = threading.Lock()

    def vncConnectionMade(self):
        self.setPixelFormat()
        encodings = [X_REQUEST_DATA_ENCODING]
        self.setEncodings(encodings)
        self.factory.clientConnectionMade(self)

    def vncRequestPassword(self):
        if self.factory.password is None:
            self.factory.password = ''
        self.sendPassword(self.factory.password)

    '''
    def _getLastReceiveTime(self):
        self._lastRecvTimeLock.acquire()
        time = self._lastReceiveTime
        self._lastRecvTimeLock.release()
        return time

    def _setLastReceiveTime(self, time):
        self._lastRecvTimeLock.acquire()
        self._lastReceiveTime = time
        self._lastRecvTimeLock.release()

    lastReceiveTime = property(_getLastReceiveTime, _setLastReceiveTime)
        
    def waitResponse(self, startTime, minIdleTime):
        while True:
            lastRecvTime = self.lastReceiveTime
            if lastRecvTime > startTime and time.time() - lastRecvTime > minIdleTime:
                return startTime, lastRecvTime - startTime
            time.sleep(0.5)
    '''
        
    def waitResponse(self, startTime, minIdleTime):
        time.sleep(minIdleTime)
        return startTime, minIdleTime

class XFactory(rfb.RFBFactory):
    password = None

    protocol = XClient
    shared = True

    def __init__(self):
        self.deferred = Deferred()

    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(reason)
        self.deferred = None

    def clientConnectionMade(self, protocol):
        self.deferred.callback(protocol)
        self.deferred = None
