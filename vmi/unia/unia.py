# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Unia Client
'''

import requests, threading
from requests_ntlm import HttpNtlmAuth
from subprocess import call
import os, hashlib,base64, re, time, sys
import simplejson as json
from vmi.configure import Configure
#from vmi.utility.logger import Logger
from vmi.utility.cipher import *
from vmi.dal.dalservice import DalService
from client.run import connectWithProtocal , connectThroughGateway
from twisted.internet import reactor, protocol
from client.tunnel import Tunnel

import subprocess
import logging
import time



class Unia(object):

    def __init__(self, user_name, user_password, enable_gateway_ = False):

        self.user_name = user_name
        self.user_password = user_password
        self.salt = None
        self.vnc_ip = None
        self.vnc_port = None
        self.token = None
        self.config = Configure.Instance()
        self.is_enbale_ldap = False
        self.connection_thread = None
        self.enable_gateway = enable_gateway_

        config = self.config
        
        
        # define a Handler which writes INFO messages or higher to the sys.stderr        
        runTime = time.strftime("%Y-%m-%d %X",time.localtime())
        runTime = runTime.replace(' ', '-')
        runTime = runTime.replace(':', '-')
        
        
        self.logger = logging.getLogger(user_name)
        self.full_file_name = runTime +'_'+ user_name+'.txt'
        handler = logging.FileHandler(self.full_file_name);
        handler.setLevel(logging.NOTSET);
        formatter = logging.Formatter('%(asctime)-16s %(levelname)-8s %(message)s');
        handler.setFormatter(formatter);
        self.logger.addHandler(handler);
        self.logger.critical('%s %s'%(user_name, user_password))
        #self.file_path = ''
        #self.logger.error("This is an error message")
        #self.logger.info("This is an info message")
        #self.logger.critical("This is a critical message")
        
        self.dalService = DalService()
        self._server_ip = None
        self._uri_prefix = None
        if self.enable_gateway:
            self._server_ip = config['Gateway']['ip']
            self._uri_prefix = config['Gateway']['protocol'] + '://' +\
                              config['Gateway']['ip'] + ':' + config['Gateway']['port']
        else:
            self._server_ip  = config['UniaServer']['portal_ip']

            self._uri_prefix = config['UniaServer']['portal_protocol'] + '://' + \
                               config['UniaServer']['portal_ip'] + ':' + config['UniaServer']['portal_port']

        self.session = requests.Session()

        self._headers = {'Content-Type':'application/json', 'User-Agent':'Android'}

        #called only not using ldap conditation
        #call(['ssh','root@'+self._server_ip , 'python',
        #      '/vmi/manager/change_password.py',self.user_name, self.user_password])

        #self.dalService.disable_change_password(self.user_name)

    def _gen_key(self,salt):

        m = hashlib.sha1()
        m.update(salt + self.user_password)

        return m.hexdigest()

    def _gen_pass(self,timestamp):

        key = self._gen_key(self.salt)
        cipher = BFCipher(unhexlify(key))
        return cipher.encrypt( base64.b64encode( unhexlify(key)) + '$' + timestamp + '$' )

    def _decrypt_token( self, token):
        '''used only for ldap
        '''
        t = self.user_password
        m = hashlib.sha1()
        if self.is_enable_ldap:
            t = self.user_name
            t = t[t.find('\\') +1 :]
        m.update(self.salt + t)
        key = m.hexdigest()
        cipher = BFCipher(unhexlify(key))
        dec =  cipher.decrypt(token)
        return dec[:dec.find('$')]

    def login(self):

        #self.dalService.disable_change_password(self.user_name)

        uri = self._uri_prefix + '/api/v1/portal/cfg'

        self.logger.critical(uri)

        payload = {'username':self.user_name}

        r = self.session.post( uri ,json.dumps(payload), headers =
                               self._headers, verify = False)

        #self.logger.critical(uri)
        print r.text
        result = json.loads(r.text)
        self.salt = result['salt']

        self.is_enable_ldap = result['enabled_ldap']

        timestamp = result['timestamp']

        uri = self._uri_prefix + '/api/v1/portal/login'

        self.logger.critical(uri)

        if not self.is_enable_ldap:

            # move to server side cause this action may change server salt.
            #call(['ssh','root@'+self._server_ip , 'python',
            #  '/vmi/manager/change_password.py',self.user_name, self.user_password])

            payload = {'username':self.user_name,
                       'user_agent':'Android/8888',
                       'password':self._gen_pass(timestamp)}

        else:

            key = self._gen_key(self.salt)
            cipher = BFCipher(unhexlify(key))
            password = cipher.encrypt('mac8.6'+'$' + time.asctime())

            payload = {'username':self.user_name,
                       'user_agent':'Android/8888',
                       'password':password}

        #self.logger.critical(uri)

        r = self.session.post(uri, json.dumps(payload), headers =
                              self._headers,verify = False)

        if  r.status_code == 401 :
            r = self.session.post(uri, json.dumps(payload),
                                  auth=HttpNtlmAuth(self.user_name,self.user_password),
                                  headers = self._headers, verify = False)

        result = json.loads(r.text)

        try:

            self.token = result['token']

        except :

            if result['code'] == 4004 and not self.is_enable_ldap:

                self._change_password()

            else:
                print result
                raise ValueError("Fail to login to Unia server")

        uri = self._uri_prefix + '/api/v1/portal/startunia'

        self.logger.critical(uri)

        payload = {"username":self.user_name,"token":self.token,
                   "locale":"en_US","display":{"density":240,"y":800,"mode":0,"x":480}}

        r = self.session.post(uri, json.dumps(payload), headers =
                              self._headers, verify = False)
        print r.text
        result = json.loads(r.text)

        print result
        

        unia = result['unia']

        r = r'(([12][0-9][0-9]|[1-9][0-9]|[1-9])\.){3,3}([12][0-9][0-9]|[1-9][0-9]|[1-9])'

        com = re.compile(r)

        m_iter =  com.search(unia)

        if None is m_iter.group():

            raise ValueError('Cannot dump VNC server ip')

        else:
            self.vnc_ip = str(m_iter.group())
            self.vnc_port = unia[unia.find(':',7)+1:]
            self.logger.critical('vnc server ip is %s'% self.vnc_ip)

        print self.vnc_ip, self.vnc_port, self.salt , self.token, self._decrypt_token(self.token)

        tunnel = None

        if self.enable_gateway:
            config = self.config
            gw_ip = config.get('Gateway','ip')
            gw_port = config.get('Gateway','port')
            tunnel = Tunnel(gw_ip, gw_port, self.vnc_ip, self.vnc_port)
        #threading.Thread(target = connectWithProtocal, args = (self.vnc_ip, self.vnc_port,
        #                                                       self._decrypt_token(self.token))).start()

        #connectWithProtocal ( self.vnc_ip, self.vnc_port, self._decrypt_token(self.token))

        def connection_work( ip, port, token , tunnel = None):
            py_script = os.path.join(os.path.dirname(__file__), 'client','run.py')
            #call(['python', py_script, ip, port, token])
            command = None
            
            self.logger.critical('%s, %s, %s, %s'%(ip,port,token,self.user_name))
            
            if tunnel is None :
                command = ['python',py_script, ip, port ,token]
            else:
                print 'o_port is :', str(tunnel.o_port)
                command = ['python',py_script, 'localhost',str(tunnel.o_port),token]
            #call(command)
            with open(self.full_file_name, "a") as fnull:
                    result = subprocess.call(command, stdout = fnull, stderr = fnull)

        success = False
        for i in range (80):

            if self.check_unia():
                print 'unia is ready'
                success = True
                #
                self.connection_thread = threading.Thread(
                    target = connection_work,
                    args = ( self.vnc_ip,
                             self.vnc_port,
                             self._decrypt_token(self.token),
                             tunnel, ))
                self.connection_thread.start()
                break

            else:
                time.sleep(5)
        if not success:
            print 'start unia failed'


    def check_unia(self):

        uri = self._uri_prefix + '/api/v1/portal/chkunia'
        
        self.logger.critical(uri)

        payload = {'token':self.token, 'username':self.user_name}

        r = self.session.post( uri, json.dumps(payload), headers =
                               self._headers, verify = False)

        try:
            result = json.loads(r.text)
            if result['code'] == 0:
                try:
                    self.token = result['vnc_token']
                except KeyError :
                    print 'no secure'
                return True
            else:
                return False
        except Exception , e:
            print e
            return False

    def _change_password(self):


        uri = self._uri_prefix + '/api/v1/portal/cfg'

        logger.critical(uri)

        payload = {'username':self.user_name}

        r = self.session.post( uri ,json.dumps(payload), headers =
                               self._headers, verify = False)

        self.logger.critical(uri)

        result = json.loads(r.text)
        self.salt = result['salt']
        self.is_enable_ldap = result['enabled_ldap']
        timestamp = result['timestamp']

        uri = self._uri_prefix + '/api/v1/portal/chpwd'

        key = self._gen_key(self.salt)
        cipher = BFCipher(unhexlify(key))

        password = cipher.encrypt( self.user_password + '$' + self.user_password + '$' + timestamp)

        payload = {'username':self.user_name, 'password': self._gen_pass(timestamp)}

        r = self.session.post(uri, json.dumps(payload), headers =
                              self._headers, verify = False)

        result = json.loads(r.text)

        self.token = result['token']

        self.salt = result['salt']


    def logout(self):

        uri = self._uri_prefix + '/api/v1/portal/stopunia'

        payload = {'username' : self.user_name, 'token': self.token}

        self.logger.critical(uri)

        r = self.session.post(uri, json.dumps(payload), headers =
                              self._headers, verify = False)

        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError('Fail to stop unia %s' % self.user_name)
