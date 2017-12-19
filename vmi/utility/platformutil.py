'''
Created on 2012-11-8

@author: joshua_liu
'''

import struct

def is_x86():
    return 8 * struct.calcsize("P") == 32

def is_x64():
    return 8 * struct.calcsize("P") == 64