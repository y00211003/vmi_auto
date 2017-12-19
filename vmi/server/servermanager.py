# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Unia Server Manager
'''
from vmi.utility.logger import Logger
from vmi.configure import Configure
from webcommand import *
from vmi.dal.dalservice import DalService
import socket

log = Logger(__name__)

class ServerManager(object):

    def __init__(self):
        self.config = Configure.Instance()
        self.dalService =  DalService()

    def setup_unia_server(self, server):
        SetServerCommand(server)()

    def start_unia_server(self, server, server_id):
        StartServerCommand(server)(server_id)

    def stop_unia_server(self, server, server_id):
        StopServerCommand(server)(server_id)

    def active_license(self, server, ac_code):
        ActiveLicenseCommand(server)( ac_code)

    def upload_native_application(self, server, app):

        app_id = UploadAppCommand(server)(app)

        return app_id

#UploadAppErrorCode
#add by richard
    def upload_workspaceapp_errorcode(self, server, app):
        return UploadAppErrorCode(server)(app)

#Sandbox_UploadAppErrorCode
    def sandbox_UploadApp_ErrorCode(self, server, app):
        return Sandbox_UploadAppErrorCode(server)(app)

#add by richard
    def upload_sandbox_androidapp(self, server, app):

        app_id = Sandbox_UploadAndroidAppCommand(server)(app)

        return app_id

#add by richard
    def upload_sandbox_iosapp(self, server, app):

        app_id = Sandbox_UploadIOSAppCommand(server)(app)

        return app_id

#add by richard
    def get_sandboxapp_packagename(self, server, app_id):
        return GetSandboxAppPackageNameCommand(server)(app_id)

#add by richard
    def get_workspaceapp_packagename(self, server, app_id):
        return GetWorkspaceAppPackeNameCommand(server)(app_id)

    def upload_wallpaper( self, server, wallpaper):

        wp_id = UploadWallpaperCommand(server)(wallpaper)
        return wp_id

#add by richard
    def get_wallpaper_detail(self, server, wp_id):
        return GetWallpaperDetailCommand(server)(wp_id)

#add by richard
    def del_wallpaper(self, server, wp_id):
        return DelWallpaperCommand(server)(wp_id)

#add by richard
    def del_sandbox_app(self, server, app_id):
        return DelSandboxAppCommand(server)(app_id)

#add by richard
    def del_workspace_app(self, server, app_id):
        return DelWorkspaceAppCommand(server)(app_id)

#add by richard
    def disable_workspace_app(self, server, app_id):
        return DisableBuildInAppCommand(server)(app_id)

#add by richard
    def enable_workspace_app(self, server, app_id):
        return EnableBuildInAppCommand(server)(app_id)

#add by richard
    def hide_app(self, server, app_id):
        return HideAppCommand(server)(app_id)

#add by richard
    def unhide_app(self, server, app_id):
        return UnHideAppCommand(server)(app_id)

#add by richard
    def get_app_hidestatus(self, server, app_id):
        return GetAppHideStatusCommand(server)(app_id)

#add by richard
    def edit_workspace_app(self, server, app_id, description_txt):
        return EditWorkspaceAppCommand(server)(app_id, description_txt)

#add by richard
    def edit_sandbox_app(self, server, app_id, description_txt):
        return EditSandboxAppCommand(server)(app_id, description_txt)

#add by richard
    def get_sandboxapp_description(self, server, app_id):
        return GetSandboxAppDescriptionCommand(server)(app_id)

#add by richard
    def edit_webclip(self, server, app_id, description_txt):
        return EditWebclipCommand(server)(app_id, description_txt)

#add by richard
    def create_sandboxprofile(self, server, profile):
        return CreateSandboxProfileCommand(server)(profile)

#add by richard
    def create_bluetoothprofile(self, server, profile):
        return CreateBluetoothProfileCommand(server)(profile)

#add by richard
    def del_sandboxprofile(self, server, profile):
        return DeleteSandboxProfileCommand(server)(profile)

#add by richard
    def change_userprofile(self, server, u_id, p_id):
        return ChangeProfileOnUser(server)(u_id,p_id)

#add by richard
    def change_groupprofile(self, server, g_id, p_id):
        return ChangeProfileOnGroup(server)(g_id,p_id)

#add by richard
    def get_groupprofile(self, server, g_id):
        return GetProfileOnGroup(server)(g_id)

#add by richard
    def get_userprofile(self, server, u_id):
        return GetProfileOnUser(server)(u_id)

#add by richard
    def userBindingOption(self, server, option_id):
        return UserBindingOptionCommand(server)(option_id)

#add by richard
    def importDeviceBindCommand(self, server, txt):
        return ImportDeviceBindCommand(server)(txt)

#add by richard
    def userBindingAction_byNameInfo(self, server, action_id, user_name, device_info):
        return UserBindingActionCommand(server)(action_id,user_name,device_info)

#add by richard
    def getDeviceBindStatus_byNameInfo(self, server, user_name, device_info):
        return GetDeviceBindStatusCommand(server)(user_name,device_info)

#add by richard
    def unia_cfgOptionCommand(self, server, option):
        return Unia_cfgOptionCommand(server)(option)

#add by richard
    def remember_passwdOptionCommand(self, server, option):
        return Remember_passwdOptionCommand(server)(option)

#add by richard
    def auto_alertOptionCommand(self, server, option):
        return Auto_alertOptionCommand(server)(option)

#add by richard
    def ldap_lockOptionCommand(self, server, option, lock_num, interval):
        return Ldap_lockOptionCommand(server)(option,lock_num,interval)

#add by richard
    def password_levelOptionCommand(self, server, level):
        return Password_levelOptionCommand(server)(level)

#add by richard
    def sacfgCommand(self, server, ip, port):
        return SAcfgCommand(server)(ip, port)

#InsertDeviceMysqlCommand
#add by richard
    def insert_mdmDevice_Mysql(self, server, device_type, device_name):
        device_id = InsertDeviceMysqlCommand(server)(device_type,device_name)

        return device_id

#MdmEditDeviceCommand
#add by richard
    def mdm_EditDeviceCommand(self, server, device_id, device_type, device_name, asset_number, ownership, description):
        id = MdmEditDeviceCommand(server)(device_id,device_type,device_name,asset_number,ownership,description)

        return id

#MdmDeleteDeviceCommand
#add by richard
    def mdm_DeleteDeviceCommand(self, server, device_type, device_id):
        statusCode = MdmDeleteDeviceCommand(server)(device_type,device_id)

        return statusCode

#MdmRemoteLocateCommand
#add by richard
    def mdm_RemoteLocateCommand(self, server, device_type, device_id):
        location = MdmRemoteLocateCommand(server)(device_type,device_id)

        return location

#MdmResetPasswdCommand
#add by richard
    def mdm_ResetPasswdCommand(self, server, device_type, device_id):
        statusCode = MdmResetPasswdCommand(server)(device_type,device_id)

        return statusCode
       
#MdmRemoteLockCommand
#add by richard
    def mdm_RemoteLockCommand(self, server, device_type, device_id, phoneNum, message):
        statusCode = MdmRemoteLockCommand(server)(device_type,device_id,phoneNum,message)
        return statusCode

#MdmRemoteWipeCommand
#add by richard
    def mdm_RemoteWipeCommand(self, server, device_type, device_id):
        statusCode = MdmRemoteWipeCommand(server)(device_type,device_id)
        return statusCode
 
    def add_webclip(self, server, url= 'http://www.baidu.com'):

        app_id = AddWebClipCommand(server)(url)

        return app_id

#UpdateCloudAppCommand
#add by richard
    def update_cloudappCommand(self, server, app_id, description, name, sso_enable):
        app_id = UpdateCloudAppCommand(server)(app_id, description, name, sso_enable)
        return app_id

#UpdateSandboxAppSSOCommand
#add by richard
    def updateSandboxAppSSOCommand(self, server, app_id, description, name, sso_enable):
        detail = UpdateSandboxAppSSOCommand(server)(app_id, description, name, sso_enable)
        return detail
#PerformanceSuperlab
#add by richard
    def doPerformanceSuperlab(self, server):
        ret = PerformanceSuperlab(server)()
        return ret

#CollectSysInfo
#add by richard
    def collectSysInfo(self, server):
        ret = CollectSysInfo(server)()
        return ret

#HandleInfoData
#add by richard
    def handleInfoData(self, server):
        ret = HandleInfoData(server)()
        return ret

#HandleUniaLoginTime
#add by richard
    def handleUniaLoginTime(self, server):
        ret = HandleUniaLoginTime(server)()
        return ret

#CountUniaLoginTime
#add by richard
    def countUniaLoginTime(self, server, user_id):
        return CountUniaLoginTime(server)(user_id)    


#Draw_MatplotlibServer
#add by richard
    def draw_MatplotlibServer(self, server):
        ret = Draw_MatplotlibServer(server)()
        return ret

    #used only in local user mode
    def create_group(self, server,group_name):

        group_id = CreateGroupCommand(server)(group_name)

        return group_id

    #used only in local user mode

    def create_user_in_group(self, server, group_id , user_name, password,  policy_id):

        user_id = CreateUserInGroupCommand(server)(group_id, user_name, password,
                                                   'test', 'vmi','test@test.com', policy_id)
        #self.dalService.disable_change_password(user_name)

        return user_id

    def delete_user_by_id(self, server, u_id):
        DeleteUserByID(server)(u_id)

    def set_group_profile(self, server, group_id, profile_id):

        SetGroupProfile(server)(group_id,profile_id)

    def get_group_id_by_name(self, server, group_name):

        return server.get_group_id_by_name(group_name)

    def get_profile_id_by_name(self, server, profile_name):

        return server.get_profile_id_by_name(profile_name)


    def get_user_id_by_name(self, server, user_name):

        return server.get_user_id_by_name(user_name)

    def set_user_profile(self, server, user_id, profile_id):

        SetUserProfile(server)(user_id, profile_id)


    def get_app_id_by_name(self, server, app_name):

        return server.get_app_id_by_name(app_name)

    def create_profile(self, server, profile):

        return CreateProfileCommand(server)(profile)

    def assign_profile_on_user(self, server, u_id, p_id):

        AssignProfileOnUser(server)(u_id,p_id)

    def assign_profile_on_group(self, server, g_id, p_id):

        AssignProfileOnGroup(server)(g_id, p_id)

    def delete_profiles( self, server, *p_ids):
        DeleteProfileCommand(server)(list(p_ids))

    def set_active_directory(self, server, host, port, user, password, enable_tls=False):
        SetActiveDirectory(server)(host, port, user, password, enable_tls= False)

    def disable_active_directory(self, server):
        DisableActiveDirectory(server)()

    def search_group_or_users(self, server, key):
        SearchGroupOrUsersCommand(server)(key)

    def import_group_or_users(self, server, key, o_name, o_type):
        ImportGroupOrUsersCommand(server)(key, o_name,o_type)

    def enable_user_by_id(self, server, user_id ):
        EnableOrDisableUserCommand(server)(user_id, True)

    def disable_user_by_id(self, server , user_id):
        EnableOrDisableUserCommand(server)(user_id, False)

    def wipe_user_by_id(self, server, user_id):
        WipeUserCommand(server)(user_id)

    def clear_workspace_screen_lock_by_id(self, server, user_id):
        ClearWorkspaceScreenLockCommand(server)(user_id)

    def get_access_setting(self, server):
        access = GetConfigAccessCommand(server)()
        return access

    def get_remember_password_setting(self, server):
        return GetConfigRememberPasswordCommand(server)()

    def get_ad_restrict_setting(self, server):
        ad_restrict = GetConfigADRestrictCommand(server)()
        return ad_restrict

    def get_unia_idle_time_setting(self, server):
        return GetConfigUniaIdleTimeCommand(server)()

    def get_vip_number_setting(self, server):
        return GetConfigVIPNumberCommand(server)()

    def get_proxy_setting(self, server):
        return GetConfigProxyCommand(server)()

    #add by gannicus
    def update_profile(self, server, profile):
        return UpdateProfileCommand(server)(profile)

    #add by gannicus
    def update_web_clip_icon(self, server, app_id, icon_filename):
        return UpdateWebclipIconCommand(server)(app_id, icon_filename)

    #add by gannicus
    def edit_admin_info(self, server, email, first_name='', last_name=''):
        return EditAdminInfoCommand(server)(email, first_name, last_name)

    #add by gannicus
    def set_ldap_lock(self, server, lock_num, interval):
        return SetLdapLockCommand(server)(lock_num, interval) 

    #add by gannicus
    def get_instance_limitation(self, server):
        return GetInstanceLimitationCommand(server)()    
    
    def check_server(self, address, port):
        s = socket.socket()
        print "Attempting to connect to %s on port %s" %(address, port)
        try:
            s.connect((address, port))
            print "Connected to %s on port %s" % (address, port)
            s.close()
            return True
        except socket.error, e:
            print "Connection to %s on port %s failed: %s" % (address, port, e)
            return False    

    #add by gannicus
    def restart_vmi(self):
        ESXHOST="10.206.137.14"
        ESXPASSWD="wx2jeacen"
        VMIVM="VMI_AUTO"
        VMIIP="192.168.10.201"        
        os.system('python /root/vmi/vmi/scripts/power_trigger.py -s %s -u root -p %s -t %s -g off'%(ESXHOST, ESXPASSWD, VMIVM))
        time.sleep(10)
        os.system('python /root/vmi/vmi/scripts/power_trigger.py -s %s -u root -p %s -t %s -g on'%(ESXHOST, ESXPASSWD, VMIVM))
        for i in range(60):
            if self.check_server(VMIIP, 443) == True:
                return True
            time.sleep(10)
        raise ValueError('Restart vmi error')

    #add by gannicus
    def set_proxy_setting(self, server, proxy):
        return SetProxySettingCommand(server)(proxy)    

    #add by gannicus
    def get_app_risklevel(self, server, app_id):
        return GetAppRisklevelCommand(server)(app_id)

    #add by gannicus
    def set_vip(self, server, u_name):
        u_id = self.get_user_id_by_name(server, u_name)
        return SetVipCommand(server)(u_id)
 
