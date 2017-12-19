# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Unia Client Manager
'''
from vmi.utility.logger import Logger
from vmi.configure import Configure
import rpyc

from unia import Unia
from uniacommand import DeviceCommand

class UniaManager(object):

    def __init__(self):

        self.config = Configure.Instance()

    def login(self, unia):
        command = DeviceCommand(unia, 'login')
        command.execute()

    def logout(self, unia):
        command = DeviceCommand ( unia, 'logout')
        command.execute()
