import threading
import time
import sys

class OutputUtil():
    def writeHeader(self, headers):
        self.headerLengths = []
        totalLen = 0
        headerStr = ''
        for i in headers:
            self.headerLengths.append(len(i)+2)
            totalLen += len(i) + 3
            headerStr += ' %s |' % (i,)
        self.lineLength = totalLen + 1

        print '+%s+' % ('-' * (totalLen-1),)
        print '|%s' % (headerStr,)
        print '|%s|' % ('-' * (totalLen-1),)

    def writeValues(self, values):
        sys.stdout.write('\r')
        self._writeValue(values)

    def writeValueWithLF(self, values):
        self._writeValue(values)
        sys.stdout.write('\n')

    def _writeValue(self, values):
        if len(values) != len(self.headerLengths):
            return
        for index, item in enumerate(values):
            sys.stdout.write('|%s' % (self._getStr(item, self.headerLengths[index]),))
        sys.stdout.write('|')
        sys.stdout.flush()

    def writeEnd(self):
        print '\n+%s+' % ('-' * (self.lineLength - 2),)

    def _getStr(self, value, maxLength):
        if isinstance(value, int):
            s = '%d' % (value,)
        else:
            s = '%.2f' % (value,)
        sLen = len(s)
        if sLen > maxLength:
            s = s[:maxLength]
        else:
            leftLen = (maxLength - sLen) / 2
            rightLen = maxLength - sLen - leftLen
            s = '%s%s%s' % (' ' * leftLen, s, ' ' * rightLen)
        return s

statsWriter = OutputUtil()

class Statistics(threading.Thread):

    TIMER_SECOND_INTERVAL = 0.5

    def __init__(self):
        super(Statistics, self).__init__()
        self.totalBytes = 0
        self.totalFrames = 0
        self.currMbps = 0.0
        self.maxMbps = 0.0
        self.minMbps = -1.0
        self.currFps = 0.0
        self.maxFps = 0.0
        self.minFps = -1.0
        self.lastBytes = 0
        self.lastFrames = 0
        self.timer = None
        self.startTime = 0

    def _getTotalmSec(self):
        if self.startTime == 0:
            return 0
        return time.time() - self.startTime

    totalmSec = property(_getTotalmSec)

    def _getAvgMbps(self):
        return self.totalBytes / self.totalmSec * 1000 / 1024 / 128

    avgMbps = property(_getAvgMbps)

    def _getAvgFps(self):
        return self.totalFrames / self.totalmSec * 1000

    avgFps = property(_getAvgFps)

    def _statsWorker(self):
        self._stopTimer()

        self.currMbps = (self.totalBytes - self.lastBytes) / self.TIMER_SECOND_INTERVAL / 1024 / 128
        if self.maxMbps < self.currMbps:
            self.maxMbps = self.currMbps
        if self.minMbps > self.currMbps or self.minMbps < 0.0:
            self.minMbps = self.currMbps

        self.currFps = (self.totalFrames - self.lastFrames) / self.TIMER_SECOND_INTERVAL
        if self.maxFps < self.currFps:
            self.maxFps = self.currFps
        if self.minFps > self.currFps or self.minFps < 0.0:
            self.minFps = self.currFps

        self.lastBytes = self.totalBytes
        self.lastFrames = self.totalFrames

        # statsWriter.writeValues([self.currMbps, self.maxMbps, self.minMbps, self.totalBytes/1024.0/1024.0,
        #                          self.currFps, self.maxFps, self.minFps, self.totalFrames,
        #                          time.time()-self.startTime])

        self._startTimer()

    def _startTimer(self):
        self.timer = threading.Timer(self.TIMER_SECOND_INTERVAL, self._statsWorker)
        self.timer.start()

    def _stopTimer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def run(self):
        header = ' Mbps , Max , Min ,Total, Fps , Max , Min ,Total, Time '.split(',')
        #header = ' max send , min send , max total , min total '.split(',')
        statsWriter.writeHeader(header)
        self.startTime = time.time()
        self._startTimer()
        while True:
            time.sleep(1)

    def addBytes(self, bytesNum):
        self.totalBytes += bytesNum

    def addFrame(self, frameNum):
        self.totalFrames += frameNum

stats = Statistics()
