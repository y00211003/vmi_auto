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
from printlog import *

CSR_REQUEST_DATA_ENCODING = 147
CSR_REQUEST_CACHE_ENCODING = 148

class CSRClient(rfb.RFBClient, object):

    def __init__(self):
        super(CSRClient, self).__init__()
        self.encodingExt = {
            CSR_REQUEST_DATA_ENCODING: (self.handleRequestData, 7),
            CSR_REQUEST_CACHE_ENCODING: (self.handleRequestCache, 23)
        }
        
        self._header = CSR_HEADER
        #self._lastReceiveTime = 0
        #self._lastRecvTimeLock = threading.Lock()
        #self._csv = open('ts.csv', 'w')

    def vncConnectionMade(self):
        self.setPixelFormat()
        encodings = [rfb.RAW_ENCODING, CSR_REQUEST_DATA_ENCODING, CSR_REQUEST_CACHE_ENCODING]
        self.setEncodings(encodings)
        self.factory.clientConnectionMade(self)

    def vncRequestPassword(self):
        if self.factory.password is None:
            self.factory.password = ''
        self.sendPassword(self.factory.password)

    def sendRequestData(self, cleanCache = 0):
	printTime()
	print 'CSR request sent'
        self.transport.write(pack('!BB', CSR_REQUEST_DATA_ENCODING, cleanCache))
        #stats.start()       

    def sendRequestCache(self, cacheIndex):
	printTime()
	print 'CSR cache request sent'
        self.transport.write(pack('!B16s', CSR_REQUEST_CACHE_ENCODING, cacheIndex))

    def handleRequestData(self, block):
        (size,) = unpack('!3xI', block)
        #self.lastReceiveTime = time.time()
        #stats.addBytes(size)
	printTime()
        print 'In handleRequestData, more size:'+str(size)
        self.expect(self._handleData, size)
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
	
    def _handleData(self, block):
        '''
	packetStartPos = 0
        frameNum = 0
        maxInSendQTs = 0
        minInSendQTs = -1
        maxInBinderQTs = 0
        minInBinderQTs = -1
        originBlock = decompress(block)
        #recvTime = time.time()
        while packetStartPos < len(originBlock):
            remainBlock = originBlock[packetStartPos:]
            # packetType = unpack('B', remainBlock[:1])
            (ts, packetType) = unpack('IB', remainBlock[:5])

            if ts > maxInSendQTs:
                maxInSendQTs = ts
            if ts < minInSendQTs or minInSendQTs == -1:
                minInSendQTs = ts

            # packetStartPos += 1
            packetStartPos += 5
            if packetType == 1:  # create surface
                packetStartPos += 17
            elif packetType == 2: # draw surface
                (bufferLen, inTs) = unpack('II', originBlock[packetStartPos+5:packetStartPos+13])
                packetStartPos += bufferLen + 9

                # inTs = ts - inTs
                if inTs > maxInBinderQTs:
                    maxInBinderQTs = inTs
                if inTs < minInBinderQTs or minInBinderQTs == -1:
                    minInBinderQTs = inTs

            elif packetType == 3:  # unbind surface
                frameNum += 1
                packetStartPos += 4
            elif packetType == 4: # delete surface
                packetStartPos += 4
            elif packetType == 5: # set surface state
                (packetSize,) = unpack('I', originBlock[packetStartPos:packetStartPos+4])
                packetStartPos += 4
                for i in range(packetSize):
                    (what,) = unpack('B', originBlock[packetStartPos+4:packetStartPos+5])
                    packetStartPos += 5
                    if what & 0x01:
                        packetStartPos += 8
                    if what & 0x02:
                        packetStartPos += 4
                    if what & 0x04:
                        packetStartPos += 8
                    if what & 0x08:
                        packetStartPos += 4
                    if what & 0x10:
                        packetStartPos += 16
                    if what & 0x20:
                        (transRegionLen,) = unpack('I', originBlock[packetStartPos:packetStartPos+4])
                        packetStartPos += 4 + transRegionLen
                    if what & 0x40:
                        packetStartPos += 8
            else:
                print 'unknow packet (%d) type:%d' % (len(block),packetType)
                break

        if frameNum:
            printTime()
	    print ' add frame %d' % frameNum
            #stats.addFrame(frameNum)
	'''
        #self._csv.write('%f,%d,%d,%d,%d,%d\n' %(recvTime, minInSendQTs, maxInSendQTs, minInBinderQTs, maxInBinderQTs,recvTs))
        printTime()
	print 'In handleData, data handled:'+str(len(block))
	#print '%f,%d' % (recvTime, recvTs)
        self.expect(self._handleConnection, 1)

    def _handleCacheData(self, block):
	printTime()
	print 'handleCacheData'
        self.expect(self._handleConnection, 1)

    def handleRequestCache(self, block):
        (cacheIndex, size) = unpack('!3x16sI', block)
	printTime()
        print 'receive cache Id: %s, size: %d' % (cacheIndex.encode('hex'), size)
        self.expect(self._handleCacheData, size)


class CSRFactory(rfb.RFBFactory):
    password = None

    protocol = CSRClient
    shared = True

    def __init__(self):
        self.deferred = Deferred()

    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(reason)
        self.deferred = None

    def clientConnectionMade(self, protocol):
        self.deferred.callback(protocol)
        self.deferred = None
