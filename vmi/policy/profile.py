from vmi.dal.dalservice import DalService
from vmi.configure import Configure
from vmi.server.application import Application

import os

class Language :

    (en_US, zh_CN, ja_JP) = (7,8,9)

    def __init__(self):
        pass

class WallPaper:

    def __init__(self, file_path = None, value = None, detail = None):
        self.id = None if not value is None else 11
        self.value = value if value is not None else  '/admin/images/wallpaper/red.jpg'
        self.detail = detail if detail is not None else 'red.jpg'
        self._wallpaper_data_path = os.path.join( os.path.dirname(__file__), '..','data','wallpapers')
        if not file_path is None and os.path.exists( os.path.join(self._wallpaper_data_path , file_path) ):
            self.local_file_path =  os.path.join(self._wallpaper_data_path , file_path)
            self.file_name = os.path.basename(file_path)
        else:
            self.local_file_path = None

    def dump_data(self):

        if not self.local_file_path is None:
            body = open(self.local_file_path , 'rb').read()
            return body
        else:
            return None

class Profile(object):

    def __init__(self, name =None, detail=None):
        '''
        This is the default profile content
        '''
        self.p_id = None
        self.name = name
        self.detail = detail
        self.language = Language.en_US
        self.wallpaper = WallPaper()
        self.apps = []
        self.applied_groups = []
        self.applied_users = []
        self.priority = 1
        self.single_app = False
        self.storage_limit = 0
	self.site_info = 1
	self.watermark_enable = False
	self.watermark_text = ""

    def add_app(self, app_id):
        self.apps.append(app_id)

class SandboxProfile(object):

    def __init__(self, name =None, detail=None, sandbox_setting=None, offline_period=None, local_apps=None, mdm_enable=None):
        '''
        This is the default profile content
        '''
        self.p_id = None
        self.name = name
        self.detail = detail
        self.language = Language.en_US
        self.wallpaper = WallPaper()
        self.apps = []
        self.applied_groups = []
        self.applied_users = []
        self.priority = -1
        self.single_app = False
        self.storage_limit = 0
        self.site_info = 1
        self.watermark_enable = False
        self.watermark_text = ""
        self.profile_type = 2
        self.sandbox_setting = sandbox_setting
        self.offline_period = offline_period
        self.local_apps = local_apps
        self.mdm_enable = mdm_enable

    def add_app(self, app_id):
        self.apps.append(app_id)

class BluetoothProfile(object):

    def __init__(self, name =None, detail=None, bluetooth_enable=None, bluetooth_filter_kind=None, bluetooth_name=None, bluetooth_kind=None, bluetooth_enable_rule=None, device_uuid=None, service_uuid=None, out_channel=None, in_channel=None):
        '''
        This is the default profile content
        '''
        self.p_id = None
        self.name = name
        self.detail = detail
        self.language = Language.en_US
        self.wallpaper = WallPaper()
        self.apps = []
        self.applied_groups = []
        self.applied_users = []
        self.priority = 1
        self.single_app = False
        self.storage_limit = 0
        self.site_info = 1
        self.watermark_enable = False
        self.watermark_text = ""
        self.bluetooth_enable = bluetooth_enable
        self.bluetooth_filter_kind = bluetooth_filter_kind
        self.bluetooth_name = bluetooth_name
        self.bluetooth_kind = bluetooth_kind
        self.bluetooth_enable_rule = bluetooth_enable_rule
        self.device_uuid = device_uuid
        self.service_uuid = service_uuid
        self.out_channel = out_channel
        self.in_channel = in_channel
        '''
        self.bluetooth_list = [{"bluetooth_name":, "bluetooth_kind": }]
        self.bluetooth_rule_list = [{"device_uuid":, "service_uuid":, "out_channel":, "in_channel":}]
        '''

    def add_app(self, app_id):
        self.apps.append(app_id)

