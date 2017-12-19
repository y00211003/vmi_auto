'''
Created on Jul 30, 2012

@author: xiang_wang@trendmicro.com.cn
'''
from vmi.server.servermanager import ServerManager
from vmi.unia.uniamanager import UniaManager
from vmi.server.server import Server
from vmi.server.application import Application, Paper, TXT
from vmi.unia.unia import Unia
from vmi.droid.droid import Android, DroidAPI
from vmi.policy.profile import Profile, SandboxProfile, BluetoothProfile
from vmi.policy.policychecker import PolicyChecker
from vmi.server.user import User
from vmi.server.access import AccessSetting
from vmi.server.adrestrict import ADRestrictSetting
from vmi.server.proxy import ProxySetting

class VMIInstanceFactory:

    def __init__(self):

        self.__class_dict= { 'Unia': Unia, 'Server': Server, 'Application':Application,
                             'UniaManager':UniaManager, 'ServerManager':ServerManager,
			     'PolicyChecker':PolicyChecker, 'Profile':Profile, 'Paper':Paper, 'SandboxProfile':SandboxProfile, 'BluetoothProfile':BluetoothProfile, 'TXT':TXT,
                             'Android' :Android, 'DroidAPI' : DroidAPI,
                             'User' : User, 'AccessSetting': AccessSetting,
                             'ADRestrictSetting': ADRestrictSetting, 'ProxySetting': ProxySetting
        }

    def build_instance(self, class_name, *args):
        if not class_name in self.__class_dict.keys():
            raise ValueError

        instance = self.__class_dict[class_name](*args)
        return instance


    @staticmethod
    def call_with_args( instance, *args):
        return instance(*args)
