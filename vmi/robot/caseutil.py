# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Case Utility
'''

import sys, zipfile, os, os.path
import shutil
import time
from vmi.utility.virtutil import Connection
from subprocess import call
from vmi.configure import Configure
from vmi.server.server import Server
from vmi.server.servermanager  import ServerManager
from subprocess import call

from vmi.utility.logger import Logger
log = Logger(__name__)

class TimeoutException(Exception):
    pass

class TimeoutException(Exception): 
    pass 
class Cases(object) :

    _config = None
    _case_id = None
    _work_dir = None
    _data_dir = None

    def __init__(self):
        self._config = Configure.Instance()
        pass

    @property
    def caseID(self):
        return self._case_id

    @caseID.setter
    def caseID(self, Id):
        self._case_id = Id

    @property
    def workDIR(self):
        return self._work_dir

    @workDIR.setter
    def workDIR(self, work_dir):
        self._work_dir = work_dir

    @property
    def dataDIR(self):
        return self._data_dir

    def setUp(self, module, Id):

        self._case_id = Id
        temp_dir = os.path.join(os.path.join(os.path.dirname(__file__),'..','..','robot','temp'))

        if not os.path.exists( temp_dir):
            os.mkdir(temp_dir)

        self._work_dir = os.path.join(temp_dir, self._case_id)

        if os.path.exists(self._work_dir):
            for root, dirs, files in os.walk(self._work_dir):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        else:
            os.mkdir(self._work_dir)

        self._data_dir = os.path.join(os.path.join(os.path.dirname(__file__),'..','..','robot','testdata',module, self._case_id))

        config = self._config
        host_ip = config.get('UniaServer','web_ip')
        time.sleep(5)
        server = Server()
        sm = ServerManager()
        log.debug("start active ac")
        ac_code = self._config.get('UniaServer','F_AC') #'MW-DUA3-LHTKS-QYP6J-FVXSZ-W5NMN-YPNXK'
        try:
            sm.active_license(server, ac_code)
        except  Exception,e:
            print e
            pass
        try:
            sm.stop_unia_server(server, [1])
        except Exception, e:
            #print e
            pass

        log.debug("start stop")
        server.stop_vmi_engine()
        server.stop_httpd_service()
        server.stop_redis_service()
        log.debug("end stop")
        call(['ssh','root@'+ host_ip , 'service','libvirtd','restart'])
        cmd = 'ssh root@'+ host_ip + ' rm -rf /gluster/users/* /gluster/upload/store/* /vmi/data/users/* /vmi/data/upload/store/* /gluster/upload/wallpaper/* /vmi/data/upload/wallpaper/*'
        os.system(cmd)
        call([ 'ssh' ,'root@' + host_ip , '/usr/bin/mysql -e "drop database vmi;"' ])
        call([ 'ssh','root@' + host_ip , '/vmi/manager/default.sh'])
	#sleep seem not needed
        #time.sleep(8)
        log.debug("start start")
        server.start_redis_service()
        server.start_http_service()
        server.start_vmi_engine()
        call(['ssh','root@'+host_ip, 'service','libvirtd','restart'])        

        log.debug("stop start")
        #sleep time increaseed as server becomes slow
        time.sleep(50) #25
        print "111111111111111"
        sm.start_unia_server(server, [1])
        print "2222222222222222"
        cmd ='sshpass -p ' + config['UniaClientServer']['password'] + \
            ' ssh root@' + config['UniaClientServer']['ip'] + \
            ' /etc/init.d/vmiclient restart'
        os.system(cmd)
        os.environ['case_id']= self.caseID
        os.environ['data_dir'] = self.dataDIR
        os.environ['work_dir']= self.workDIR
        #time.sleep(3)
