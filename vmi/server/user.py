#
# Author : xiang_wang@trendmicro.cm.cn

from enum import IntEnum

class UniaScreenLockType (IntEnum):
    type_none = 1
    type_pattern = 2
    type_pin = 3
    type_password = 4

class User(object):

    def __init__(self, name ,
                 password, email='',
                 screen_lock_type = UniaScreenLockType.type_none,
                 screen_lock_value = None):
        self.username = name
        self.password = password
        self.email = email
        self.screen_lock_type = int(screen_lock_type)
        self.screen_lock_value = screen_lock_value
