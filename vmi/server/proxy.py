# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Proxy Settings
'''

class ProxySetting():

    def __init__(self, ip='' , port='', username= '',
                 password = '', enable = True,
                 bypass_address = ''):
        self.ip = ip
        self.port = int(port)
        self.username = username
        self.password = password
        self.enable = enable
        self.bypass_address = bypass_address


    def __eq__(self, other):

        return self.ip == other.ip and \
            self.port == other.port and \
            self.enable == other.enable and \
            self.bypass_address == other.bypass_address
