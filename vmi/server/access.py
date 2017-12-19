# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Access Configuration Setting
'''

class AccessSetting():

    def __init__(self, ip = None , port = None):

        if ip : self.ip = ip
        if port : self.port = port
        self.reminder= False

    def __eq__(self, other):

        return self.ip == other.ip and self.port == other.port
