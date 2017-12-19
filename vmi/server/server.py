# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Unia Server
'''

from vmi.configure import Configure
from vmi.utility.logger import Logger
from webcommand import *
from subprocess import call
from vmi.policy.profile import Profile
import time

log = Logger(__name__)

class Server(object):

    def __init__(self):

        self.config = Configure.Instance()
        config = self.config

        self.host_ip = config.get('UniaServer','web_ip')
        self.host_port = config.get('UniaServer','web_port')

        self.portal_ip = config.get('UniaServer', 'portal_ip')
        self.portal_port = config.get('UniaServer', 'portal_port')

        self.applications = None
        self.profiles = None
        self.auth_users = None
        self.groups = None
        self.wallpapers = None
        #self.update_info()

    def update_info(self):

        GetCurrentUsers(self)()
        GetCurrentProfiles(self)()
        GetCurrentApplications(self)()
        GetCurrentGroups(self)()


    def get_profile_id_by_name(self, p_name):

        for p_id in self.profiles.keys():
            if self.profiles[p_id]['name'] == p_name:
                return p_id
        return None

    def get_profile_by_name(self, p_name):

        profile = Profile()
        profile.p_id = self.get_profile_id_by_name(p_name)
        p_id = profile.p_id
        profile.name = self.profiles[p_id]['name']
        profile.detail = self.profiles[p_id]['detail']

        profile.apps = self.profiles[p_id]['apps']
        profile.language = self.profiles[p_id]['policies'][0]
        profile.wallpaper.id = self.profiles[p_id]['policies'][1]
        profile.applied_groups = self.profiles[p_id]['applied_groups']
        profile.applied_users = self.profiles[p_id]['applied_users']
        return profile

    def get_user_id_by_name(self, u_name):
        self.update_info()
        for u_id in self.auth_users.keys():
            if self.auth_users[u_id]['username'] == u_name:
                return u_id
        return None

    def get_group_id_by_name(self, g_name):
        self.update_info()
        for g_id in self.groups.keys():
            if self.groups[g_id]['name'] == g_name:
                return g_id
        return None

    def get_app_id_by_name( self, app_name):

        for app_id in self.applications.keys():
            if self.applications[app_id]['name'] == app_name:
                return app_id
        return None

    def get_app_attr_by_id(self, app_id, attr_name):

        return self.applications[app_id][attr_name]

    def stop_vmi_engine(self):

        call(['ssh','root@'+self.host_ip , 'service','vmiengine','stop'])

    def start_vmi_engine(self):
        call(['ssh','root@'+self.host_ip , 'service','vmiengine','start'])
        #time.sleep(5)

    def restart_vmi_engine(self):
        self.stop_vmi_engine()
        time.sleep(5)
        self.start_vmi_engine()

    def stop_httpd_service(self):
        call(['ssh','root@'+self.host_ip, 'service','httpd','stop'])

    def start_http_service(self):
        call(['ssh','root@'+self.host_ip, 'service','httpd','start'])
        #time.sleep(5)

    def restart_httpd_service(self):
        self.stop_httpd_service()
        time.sleep(5)
        self.start_http_service()


    def stop_redis_service(self):
        call(['ssh','root@' + self.host_ip, 'service','redis','stop'])

    def start_redis_service(self):
        call(['ssh','root@' + self.host_ip, 'service','redis','start'])
        #time.sleep(5)


    def restart_redis_service(self):
        self.stop_redis_service()
        time.sleep(5)
        self.start_redis_service()
