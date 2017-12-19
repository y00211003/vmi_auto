'''
Created on 2013-6-7

@author: xinxin_fang
'''

import pexpect
import sys

class PexpectCommander(object):

    def __init__(self, console):
        self.instance = None
        self.shell_prefix = console.console_shell_name
        if console == None:
            self.device_name = '127.0.0.1'+':'+'5554'
        else:  
            self.device_name = console.device_name
            
    def android_adb_connect(self):
        self.android_adb_disconnect()
        pattern1 = "connected to (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})"
        pattern2 = "already connected to (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5})"
        pattern3 = "unable to connect to"

        cmd = "adb connect %s" % self.device_name
        adb_proc = pexpect.spawn(cmd, timeout=1000)
        match_id = adb_proc.expect([pattern1, pattern2, pattern3, pexpect.EOF])
        #print match_id,
        #print adb_proc
        if match_id in [0, 1]:
            self.device_name = adb_proc.match.groups()[0]
            print 'device name:',
            print self.device_name
            self.printAfter(adb_proc.after)
            print '------------' 
            return True
        else:
            print 'connect fail'
            return False

    def android_adb_disconnect(self):
        cmd = "adb disconnect"
        pexpect.run(cmd)        
           
    def SwitchInShellInteractiveMode(self):
        if self.android_adb_connect():
        
            cmd = 'adb -s %s shell'%(self.device_name)
            self.printCmd(cmd)
            adb_proc = pexpect.spawn (cmd)
            adb_proc.expect (self.shell_prefix)
            self.printBefore(adb_proc.before)
            self.printAfter(adb_proc.after)
            print '------------'
            self.instance = adb_proc
            return True
        else:
            print 'switch fail'
            return False
            
    def printCmd(self, content):
        print 'Cmd:' + str(content)
    
    def printBefore(self, content):
        print 'Before:' + str(content)
        
    def printAfter(self, content):
        print 'After:' + str(content)
        
    def checkFileExist(self, path):
            
        if self.SwitchInShellInteractiveMode():
            result  = path.strip().split('/')[-1]
            pattern1 = "\d{1,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2} " + result
            pattern2 = "No such file or directory"
            
            cmd = 'ls -al '+ str(path)
            self.printCmd(cmd)
            self.instance.sendline (cmd)
            match_id = self.instance.expect([pattern1, pattern2, pexpect.EOF])
            self.printBefore(self.instance.before)
            self.printAfter(self.instance.after)
            if match_id == 0:
                if str(self.instance.after).find(result) != -1:
                    result = True
            else:
                result = False
            print '------------'
            self.SwitchOutInteractiveMode()
            return result
        else:
            return result


    def SwitchOutInteractiveMode(self):
        if self.instance != None:
            cmd = 'exit'
            self.instance.sendline(cmd)
            self.instance.expect(pexpect.EOF)
            self.printBefore(self.instance.before)
            self.printAfter(self.instance.after)
            print '------------'
            
