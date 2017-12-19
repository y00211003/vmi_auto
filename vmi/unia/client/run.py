#!/usr/bin/env python

from twisted.python.log import PythonLoggingObserver
from twisted.internet import reactor, protocol
#from csrclient import CSRClient, CSRFactory
from vncclient import VNCClient, VNCFactory
from csrclient import CSRClient, CSRFactory
from xclient import XClient, XFactory
from statistics import stats, statsWriter
from script import Script
from heartbeatScript import HeartbeatScript
from framebufferScript import FramebufferScript
import time
import thread
import threading
import sys
import constant
#import logging
from printlog import *

logger = None

def error(reason):
    printTime()
    print reason.getErrorMessage()
    reactor.exit_status = 10
    reactor.stop()

def stop(pcol):
    printTime()
    print 'client stoped'
    reactor.exit_status = 0
    pcol.transport.loseConnection()
    # XXX delay
    reactor.callLater(0.1, reactor.stop)

def started(pcol):
    printTime()
    print 'start called'
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        pcol.sendRequestData()
    else:
        print 'script start'
        print 'mode:'+str(constant.MODE_USED)
        script = Script(pcol, constant.MODE_USED)
        heartbeatScript = HeartbeatScript(pcol, constant.MODE_USED)
        framebufferScript = FramebufferScript(pcol, constant.MODE_USED)

        script.start()
        heartbeatScript.start()
        framebufferScript.start()

'''
def connect(host, port, password):
    client = VNCClient
    factory = VNCFactory()
    factory.deferred.addCallback(started)
    factory.deferred.addErrback(error)
    reactor.connectTCP(host, int(port), factory)
    reactor.exit_status = 1
    factory.password = password
    return factory
'''

def connectWithProtocal(host, port, password, protocol = constant.VNC_MODE):
    try:
        constant.MODE_USED = protocol
        if protocol == constant.VNC_MODE:
            client  = VNCClient
            factory = VNCFactory()
            factory.deferred.addCallback(started)
            factory.deferred.addErrback(error)
            reactor.connectTCP(host, int(port), factory)
            reactor.exit_status = 1
            factory.password = password
        elif protocol == constant.CSR_MODE:
            client  = CSRClient
            factory = CSRFactory()
            factory.deferred.addCallback(started)
            factory.deferred.addErrback(error)
            reactor.connectTCP(host, int(port), factory)
            reactor.exit_status = 1
            factory.password = password
        elif protocol == constant.X_MODE:
            client  = XClient
            factory = XFactory()
            factory.deferred.addCallback(started)
            factory.deferred.addErrback(error)
            reactor.connectTCP(host, int(port), factory)
            reactor.exit_status = 1
            factory.password = password
    except e:
        print e
    return factory

def connectThroughGateway( gw_host, gw_port, host, port, password, protocol =
                           constant.VNC_MODE):
    try:
        constant.MODE_USED = protocol
        factory = None
        client = None
        if protocol == constant.VNC_MODE:
            print 'vnc mode'
            factory = VNCFactory()
            client = VNCClient
        elif protocol == connect.CSR_MODE:
            factory = CSRFactory()
            client = CSRClient
        elif protocol == constant.X_MODE:
            factory = XFactory()
            client = XClient
        factory.deferred.addCallback(started)
        factory.deferred.addErrback(error)
        factory.vnc_host = host
        factory.vnc_port = int(port)
        reactor.connectTCP(gw_host,int(gw_port),factory)
        factory.exit_status = 1
        factory.password = password
    except e:
        print e
    return factory

def getLogger():
    #global loggername
    return logging.getLogger(loggername)

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    token = sys.argv[3]

    try:
        #print 'starting...'
        connectWithProtocal(ip, port, token, constant.CSR_MODE)
        print 'Connecting to %s:%d %s' % (ip, port, token)
        #stats.setDaemon(True)
        reactor.run()
    except KeyboardInterrupt:
        pass
        #statsWriter.writeEnd()
