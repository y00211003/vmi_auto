#coding=utf-8
#author: xiang_wang@trendmicro.com.cn


import socket,time,ssl
import threading
from vmi.singleton import *
from vmi.configure import *

config = Configure.Instance()

@Singleton
class SafeCounter():
    def __init__(self):
        self.lock = threading.Lock()
        self.counter = 5901
    def inc(self):
        with self.lock:
            self.counter += 1
            return self.counter
    def dec(self):
        with self.lock:
            self.counter -= 1
            return self.counter

class InBound(threading.Thread):
    def __init__(self, i_sock, o_sock, g_ip, g_port, v_ip, v_port):
        super(InBound,self).__init__()
        self._i_sock = i_sock
        self._o_sock = o_sock
        self._g_ip = g_ip
        self._g_port = g_port
        self._v_ip = v_ip
        self._v_port = v_port

    def run(self):
        try:
            self._i_sock.connect((self._g_ip, int(self._g_port)))
            payload = 'CONNECT ' + self._v_ip + ':' + str(self._v_port) + \
                      ' HTTP/1.0\r\nUser-agent: TMSMW-client/2.0\r\n\r\n'
            self._i_sock.send(payload)
            buf = self._i_sock.recv(2048)
            if 'established' in buf:
                while True:

                    buf = self._i_sock.recv(2048)
                    self._o_sock.send(buf)
            else:
                print buf
        finally:
            self._i_sock.close()

class OutBound(threading.Thread):

    def __init__(self, i_sock, o_sock, g_ip,g_port, v_ip, v_port , o_port):

        super(OutBound,self).__init__()
        self._i_sock = i_sock
        self._o_sock = o_sock
        self._g_ip = g_ip
        self._g_port = int(g_port)
        self._v_ip = v_ip
        self._v_port = int(v_port)

        self._o_port = int(o_port)
        self.o_port = o_port
        self._i_bound = None
    def run(self):
        #self._o_sock.bind(('0.0.0.0', self._o_port))
        self._o_sock.bind(('',0))
        self._o_port = self._o_sock.getsockname()[1]

        self.o_port = int(self._o_port)

        self._o_sock.listen(5)
        try:
            connection , address = self._o_sock.accept()
            self._i_bound = InBound(self._i_sock,connection , self._g_ip, self._g_port, self._v_ip, self._v_port)
            self._i_bound.start()

            while True:
                buf = connection.recv(2048)
                self._i_sock.send(buf)
        finally:
            self._o_sock.close()


class Tunnel(object):

    def __init__(self, g_ip, g_port, v_ip, v_port):
        self.counter = SafeCounter.Instance()
        self.o_port = 0#self.counter.inc()
        super(Tunnel,self).__init__()
	i_sock = None
	if config.get('Gateway','protocol') == 'https':
	    i_sock = ssl.wrap_socket(socket.socket())
	else:	
            i_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        o_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        outbound = OutBound(i_sock,o_sock, g_ip,g_port, v_ip, v_port, self.o_port)
        outbound.start()
        time.sleep(1)
        self.o_port = outbound.o_port

if __name__ == '__main__':

    tunnel = Tunnel('10.64.90.124',80,'192.168.10.16')
