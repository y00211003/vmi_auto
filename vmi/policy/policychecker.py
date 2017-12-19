from vmi.server.server import Server
from vmi.configure import Configure
from vmi.policy.profile import Profile
from vmi.unia.unia import Unia
from vmi.server.webcommand import *
from vmi.dal.dalservice import DalService
import unicodedata as ud
from pexpectcommander import *
from deviceconsole import *

def normalize( uni ):
    if type(uni) is unicode:
        return ud.normalize('NFC', uni)
    elif type(uni) is str:
        return ud.normalize('NFC',unicode(uni))
    else:
        raise ValueError

class PolicyChecker:

    def __init__(self):
        self.server = None
        self.unia = None
        
        self.dalService = DalService()
        
        self.config = Configure.Instance()
        
    def check_policy(self, server, unia, profile):
        self.server = server
        self.unia = unia
        if profile.p_id is None:
            return False
        
        if not self._check_policy_in_server(profile):
            return False
        if not self._check_profile_in_unia(profile):
            return False
        return True
    
    def _check_policy_in_server(self, profile):
        
        self.server.update_info()
        
        s_p =  self.server.profiles[profile.p_id]
        print s_p

        try:    
            assert(profile.name == s_p['name'])
            assert(profile.apps == s_p['apps'])
            assert([profile.language , profile.wallpaper.id] == s_p['policies'])
        except AssertionError, e:
            print e
            return False
        return True
           

    def _check_profile_in_unia(self, profile):
        
        device_address = self.unia.vnc_ip
        device_port = 5555
        console = DeviceConsole(device_address, device_port, 'root\@android:\/ \#')
        pexpectCmder = PexpectCommander(console)
        
        for app in profile.apps:
            package_name = self.dalService.get_app_attr_by_id(app,'package')

            package_path = '/data/app/' + package_name + '.apk'
            if not pexpectCmder.checkFileExist(package_path):
                return False
        w_id = profile.wallpaper.id

        w_path = self.dalService.get_wallpaper_path_by_id(w_id)

        wallpaper = '/data/wallpaper/' + w_path
        if not pexpectCmder.checkFileExist(wallpaper):
            return False
        return True
