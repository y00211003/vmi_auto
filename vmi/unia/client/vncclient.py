import rfb
import time
import datetime
import threading
from struct import pack, unpack
from zlib import decompress
from twisted.internet.defer import Deferred
from twisted.internet import reactor

class VNCClient(rfb.RFBClient, object):

    def vncConnectionMade(self):
        self.setPixelFormat()
        encodings = [rfb.RAW_ENCODING]
        self.setEncodings(encodings)
        self.factory.clientConnectionMade(self)

    def vncRequestPassword(self):
        if self.factory.password is None:
            self.factory.password = ''
        self.sendPassword(self.factory.password)

    def waitResponse(self, startTime, minIdleTime):
        time.sleep(minIdleTime)
        return startTime, minIdleTime

class VNCFactory(rfb.RFBFactory):
    password = None
    vnc_host = None
    vnc_port = None
    protocol = VNCClient
    shared = True

    def __init__(self):
        self.deferred = Deferred()

    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(reason)
        self.deferred = None

    def clientConnectionMade(self, protocol):
        self.deferred.callback(protocol)
        self.deferred = None
