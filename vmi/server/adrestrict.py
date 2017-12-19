# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  AD Restrict Setting
'''


class ADRestrictSetting():

    def __init__(self, lock_num = 1 , interval = 30, enable= 'enabled'):
        ''' enabled option should be string type, cause robotframework can only
        accept string type as parameters.
        '''
        self.lock_num = int(lock_num)
        self.lock_interval = int(interval)
        self.enable = enable

    def __eq__(self, other):
        return self.lock_num == other.lock_num and \
                               self.interval == other.interval and \
                                                    self.enabled == other.enabled
