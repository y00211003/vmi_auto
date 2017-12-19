# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Default HTTP Request which will be sent by facked device
'''

import urllib, urllib2, sys, cookielib, re, os, json
import time
from logger import Logger
log = Logger(__name__)

urllib2.socket.setdefaulttimeout(60) # set timeout 10 secs

class HttpClient(object):

    opener = None

    uri = ''
    body = ''
    headers = []
    headers_map = {}
    response = None
    httpVersion = 'HTTP/1.1'
    cj = None

    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    def setHeadersMap(self, headersMap):
        self.headers = [(key, headersMap[key]) for key in headersMap.keys()]
        self.headers_map = headersMap

    def setUri(self, uri):
        self.uri = uri


    def getResponse(self):
        #print '[response] headers: %s ' % self.response.headers
        if (self.response.getcode() != 200):
            self.response.close()
            return None
        else:
            data = self.response.read()
            self.response.close()
            #log.debug("Response (%s): %s" % (self.uri, data))
            return data


    def request(self, method, uri = None, body = None):

        self.opener.addheaders = self.headers
        if None != uri:
            self.uri = uri
        if None != body:
            self.body = body
        if '' == uri:
            return None
        req = None
        if 'GET' == method.upper():
            #print 'Get '
            #print 'url: ', self.uri
            req = self.uri
        elif 'POST' == method.upper():
            req = urllib2.Request(self.uri, self.body, self.headers_map)
            #print 'Post:'
            #print 'url: %s, body: %s' % (self.uri, self.body)
        elif 'PUT' == method.upper():
            req = urllib2.Request(self.uri, self.body, self.headers_map)
            req.get_method = lambda: 'PUT'
            #print 'PUT:'
            #print 'url: %s, body: %s' % (self.uri, self.body)
        else:
            return None
        log.debug("Requesting %s..." % self.uri)
        start = time.time()
        self.response = self.opener.open(req)
        end = time.time()
        response_time = end - start
        log.debug("Request end time: %.3f, Response time (%s): %.3f" % (end, self.uri, response_time))
        return self.response

    def requestServer(self, uri = None, body = None, method = ''):
        if None != body:
            if method.upper() == '' or method.upper() == 'POST':
                method = 'POST'
            elif method.upper() == 'PUT':
                method = 'PUT'
            else:
                raise ValueError
        else:
            method = 'GET'
        self.request(method, uri, body)
        return self.getResponse()
