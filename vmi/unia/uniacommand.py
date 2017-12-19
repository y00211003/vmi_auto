# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Device commands
'''

class DeviceCommand(object):
    def __init__(self, receiver, action, *args):
        self.receiver = receiver
        self.action = action
        self.args = args

    def execute(self):
        if not hasattr(self.receiver, self.action):
            raise NotImplementedError("The action " + self.action +
                " is not allowed or implemented for " +
                self.receiver.__class__.__name__)
        method = getattr(self.receiver, self.action)
        method(*(self.args))
