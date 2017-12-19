# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Web Related Actions
'''
import requests
from requests.adapters import HTTPAdapter
requests.adapters.DEFAULT_RETRIES=1000
import os , time, commands, datetime
import simplejson as json
from vmi.configure import Configure
from vmi.utility.logger import Logger
from vmi.utility.timeutil import current_time_millis
from vmi.server.access import AccessSetting
from vmi.server.adrestrict import ADRestrictSetting
from vmi.server.proxy import ProxySetting
from application import Application, Paper
from subprocess import call
import unicodedata as ud
from vmi.dal.dalservice import DalService
from vmi.utility.cipher import encode_with_pkcs7_bf
import base64, urllib
import random
import pexpect

log = Logger(__name__)

class WebCommand(object):

    _receiver = None
    _description = None

    def __init__(self):

        self.session = requests.Session()


        self.config = Configure.Instance()

        config = self.config
	self.dalService = DalService()

        web_port = config['UniaServer']['web_port']
        if web_port == '80' or web_port == '443':
            self._uri_prefix = config['UniaServer']['web_protocol'] + '://' + \
                               config['UniaServer']['web_ip']
        else:
            self._uri_prefix = config['UniaServer']['web_protocol'] + '://' + \
                               config['UniaServer']['web_ip'] + ':' + config['UniaServer']['web_port']
        self.session.mount(self._uri_prefix, HTTPAdapter(max_retries=100))
        self._login_vmi_server()

    def __call__(self):

        raise NotImplementedError

    def _login_vmi_server(self):

        config = self.config

        uri = self._uri_prefix +  '/api/v1/account/login/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        payload = {'username':config['WebUI']['account'],
                    'password':config['WebUI']['password']}
        headers = {'content-type': 'application/json'}
	r = self.session.post(uri, json.dumps(payload), headers=headers, verify = False)
	result = json.loads(r.text)
        if not r.status_code == 200 :
            if result['code'] == 5003:
                pass
            else:
                raise ValueError("Fail to login to Unia Server")

        if not result['code'] is 0 and not result['code'] == 5003: raise ValueError('Fail to login to Unia Server with error code %d' % result['code'])
        self._cookies = r.cookies
        self._csr_token = r.cookies['csrftoken']
        self._headers = {'content-type': 'application/json','X-CSRFToken':self._csr_token}

class SetServerCommand(WebCommand):
    '''
    Set up Servers
    '''
    def __init__(self,receiver):

        super(SetServerCommand,self).__init__()
        self._description = 'Set up Servers'

    def __call__(self):

        config = self.config

        uri = self._uri_prefix + '/api/v1/system/servers/detail/1/'

        r = self.session.post(uri,'', headers = self._headers, verify = False)

        result = json.loads(r.text)

        payload = result['data']

        if not result['code'] is 0:
            raise ValueError("Get Server List failed with error code %d" % result['code'])

        managedIP = result['data']['managedIP']

        uri = self._uri_prefix + '/api/v1/system/servers/probe/0/'

        data = { 'managedIP' : managedIP }

        r = self.session.post(uri, json.dumps(data), headers= self._headers, verify = False)

        result = json.loads(r.text)
        payload['ifs'] = result['data']['ifs']

        payload['ifs'][1]['netmask'] = config['Servers']['netmask']
        payload['ifs'][1]['gateway'] = config['Servers']['gateway']
        payload['ifs'][1]['range'] = config['Servers']['ip_range']
        payload['ifs'][1]['configure'] = 'bridge'
        payload['changed'] = True
        payload['action'] = 'connect'

        r = self.session.put(uri, data = json.dumps(payload), headers = self._headers, verify=False)
        result = json.loads(r.text)
        if not result['code'] is 0:
            raise ValueError("Fail to Set Servers up with error code %d" % result['code'])

class StartServerCommand(WebCommand):

    def __init__(self,receiver):
        super(StartServerCommand,self).__init__()
        self._description = 'Start Server'
        self._receiver = receiver

    def __call__(self, server_ids):

        config = self.config

        uri = self._uri_prefix + '/api/v1/system/servers/start/0/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/servers/index.html'

        r = self.session.post(uri,json.dumps({'ids': server_ids}), headers = headers, verify= False)
        result = json.loads(r.text)

        if not r.status_code is 200: raise ValueError ("Fail to start server")
        if not result['code'] == 5000 : raise ValueError ("Fail to start server")

        # uri = self._uri_prefix + '/api/v1/system/hypervisors/tree/0/'

        # r = self.session.post(uri,'', headers = headers , verify = False)

        # result = json.loads(r.text)
        # print r.text
        # if result[0]['id'] != server_ids : raise ValueError('Fail to start server')

class StopServerCommand(WebCommand):

    def __init__(self, receiver):
        super(StopServerCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, server_ids):

        uri = self._uri_prefix + '/api/v1/system/servers/stop/0/'
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/server/index.html'
        r = self.session.post(uri,json.dumps({'ids': server_ids}), headers = headers, verify = False)

        result = json.loads(r.text)

        if not result['code'] is 0:
            raise ValueError("Get Server List failed with error code %d" % result['code'])

        uri = self._uri_prefix + '/api/v1/system/servers/ping/0/'
        server_num = len(server_ids)
        for i in range (100) :

            count = 0
            r = self.session.post(uri, json.dumps({'ids': server_ids}), headers =
                                  headers , verify = False)
            result = json.loads(r.text)
            for item in result:
               if item['id'] in server_ids:
                   if item['state'] == 1:
                       count = count +1
            if count == server_num :
                break
            time.sleep(2)

class ActiveLicenseCommand(WebCommand):

    def __init__(self, receiver):
        super(ActiveLicenseCommand, self).__init__()
        self._receiver = receiver

    def __call__( self, ac_code):

        uri = self._uri_prefix + '/api/v1/cfg/license/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/licenseFirstNewAC.htm?error_id=50003'
        payload = json.dumps({'ac':ac_code})
        r = self.session.post(uri, data = payload , headers = headers, verify =False)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ("Fail to Active License with code %s" % ac_code)
        else:
            self._receiver.update_info()

class UploadAppCommand(WebCommand):

    def __init__(self,receiver):
        super(UploadAppCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, app):

        uri = self._uri_prefix + '/api/v1/app/upload/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)

        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/apps/addMobileApp.htm?type=1&frame_id=button_add'
        r = self.session.post(uri, data = {u'filename':app.file_name,
                                           u'csrfmiddlewaretoken':self._csr_token},
                              files= {u'app_file_path': app.dump_data()},
                              headers = headers , verify = False)
        print r.text
        result = json.loads(r.text)

        result['rating'] = 3

        uri = self._uri_prefix + '/api/v1/app/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers['content-type'] = 'application/json'

        r = self.session.post( uri, data = json.dumps(result), headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )

        self._receiver.applications[result['id']] = result

        return result['id']

#add by richard
class UploadAppErrorCode(WebCommand):

    def __init__(self,receiver):
        super(UploadAppErrorCode,self).__init__()
        self._receiver = receiver

    def __call__(self, app):

        uri = self._uri_prefix + '/api/v1/app/upload/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)

        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/apps/addMobileApp.htm?type=1&frame_id=button_add'
        r = self.session.post(uri, data = {u'filename':app.file_name,
                                           u'csrfmiddlewaretoken':self._csr_token},
                              files= {u'app_file_path': app.dump_data()},
                              headers = headers , verify = False)
        print r.text
        result = json.loads(r.text)
         
        return str(result['code'])

#add by richard
class Sandbox_UploadAppErrorCode(WebCommand):

    def __init__(self,receiver):
        super(Sandbox_UploadAppErrorCode,self).__init__()
        self._receiver = receiver

    def __call__(self, app):

        uri = self._uri_prefix + '/api/v1/app/upload/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)

        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/apps/addWrapApp.htm?type=1&frame_id=button_add'
        r = self.session.post(uri, data = {u'filename':app.file_name,
                                           u'csrfmiddlewaretoken':self._csr_token},
                              files= {u'app_file_path': app.dump_data()},
                              headers = headers , verify = False)
        print r.text
        result = json.loads(r.text)

        return str(result['code'])

#add by richard
class Sandbox_UploadAndroidAppCommand(WebCommand):

    def __init__(self,receiver):
        super(Sandbox_UploadAndroidAppCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, app):

        uri = self._uri_prefix + '/api/v1/app/upload/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)

        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/apps/addWrapApp.htm?type=1&frame_id=button_add'
        r = self.session.post(uri, data = {u'filename':app.file_name,
                                           u'csrfmiddlewaretoken':self._csr_token},
                              files= {u'app_file_path': app.dump_data()},
                              headers = headers , verify = False)
        print r.text
        result = json.loads(r.text)

        #result['rating'] = 3

        uri = self._uri_prefix + '/api/v1/app/loc-app/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers['content-type'] = 'application/json'

        r = self.session.post( uri, data = json.dumps(result), headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )

        self._receiver.applications[result['id']] = result

        return result['id']

#add by richard
class Sandbox_UploadIOSAppCommand(WebCommand):

    def __init__(self,receiver):
        super(Sandbox_UploadIOSAppCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, app):

        uri = self._uri_prefix + '/api/v1/app/upload/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)

        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/apps/addWrapApp.htm?type=2&frame_id=button_add_Webclip'
        #print app.file_name
        #print app.dump_data()
        r = self.session.post(uri, data = {u'filename':app.file_name,
                                           u'type':2,
                                           u'csrfmiddlewaretoken':self._csr_token},
                              files= {u'app_file_path': app.dump_data()},
                              headers = headers , verify = False)
        print r.text
        result = json.loads(r.text)

        #result['rating'] = 3

        uri = self._uri_prefix + '/api/v1/app/loc-app/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers['content-type'] = 'application/json'

        r = self.session.post( uri, data = json.dumps(result), headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )

        self._receiver.applications[result['id']] = result

        return result['id']

#add by richard
class UploadWallpaperCommand(WebCommand):

    def __init__( self, receiver):
        super(UploadWallpaperCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, wallpaper):

        uri = self._uri_prefix + '/api/v1/policy/upload/wallpaper/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)
        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/profiles/wallpaper.htm'
       # headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
       # headers['Accept-Encoding'] = 'gzip, deflate, br'
       # headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
       # headers['Connection'] = 'keep-alive' 
        headers['Upgrade-Insecure-Requests'] = 1 
        
        print 'filenamexxxxxxxxxxxxxx',wallpaper.file_name
        #print 'wallpaperdump_datassssssss',wallpaper.dump_data() 
        r = self.session.post( uri, data = {u'filename': wallpaper.file_name,
                                            u'csrfmiddlewaretoken': self._csr_token},
                               files={u'wallpaper_file_path': wallpaper.dump_data(),
                                      u'name': wallpaper.file_name},
                               headers = headers, verify= False)


        print 'text',r.text
        result = json.loads(r.text)
        print 'ssssssssssss',result
        print 'sssssssssid',result['id']
        print 'detailssssssssssss',result['detail']
        #self._receiver.wallpapers[result['id']] = result
        
        return result['id']

#add by richard
class GetWallpaperDetailCommand(WebCommand):
    def __init__(self,receiver):
        super(GetWallpaperDetailCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, wp_id):
        uri = self._uri_prefix + '/api/v1/policy/?page_size=1000&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/profiles/wallpaper.htm'

        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)
        print 'sssssss',result
        
        #res = result['results']['values']
        for item in result['results']:
            log.debug(item['title'])
            if item['title'] == 'Wallpaper':
                for item in item['values']:
                    if item['id'] == wp_id:
                        break
                break
        print 'idxxxxxxxxxxxxx',item['id']
        print 'detailxxxxxxxxxxx',str(item['detail']) 
        return str(item['detail'])

#add by richard
class DelWallpaperCommand(WebCommand):
    def __init__(self,receiver):
        super(DelWallpaperCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, wp_id):
        uri = self._uri_prefix + '/api/v1/policy/remove/wallpaper/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        
        headers['Referer'] = self._uri_prefix + '/profiles/wallpaper.htm'
        payload = {'ids':[wp_id]}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to delete wallpaper')
        return result['detail']

#add by richard
class DelSandboxAppCommand(WebCommand):
    def __init__(self,receiver):
        super(DelSandboxAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/remove-wrapapp/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/local_app.htm?app_id=null&t=' + str ( int ( time.time()* 1000))
        payload = {'ids':[app_id]}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to delete sandbox app')
        return result['detail']

#add by richard
class DelWorkspaceAppCommand(WebCommand):
    def __init__(self,receiver):
        super(DelWorkspaceAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/remove-apps/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/index.htm?app_id=1103&t=' + str ( int ( time.time()* 1000))
        payload = {'ids':[app_id]}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to delete app')
        return result['detail']

#add by richard
class DisableBuildInAppCommand(WebCommand):
    def __init__(self,receiver):
        super(DisableBuildInAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/disable-buildin-app/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/index.htm'
        payload = {'id':app_id}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to disable app')
        return result['detail']

#add by richard
class EnableBuildInAppCommand(WebCommand):
    def __init__(self,receiver):
        super(EnableBuildInAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/enable-buildin-app/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/index.htm'
        payload = {'id':app_id}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to enable app')
        return result['detail']

#add by richard
class HideAppCommand(WebCommand):
    def __init__(self,receiver):
        super(HideAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/showapp/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/hideapp_list.htm'
        payload = {'show_type':1,'ids':[int(app_id)]}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to hide app')
        return result['detail']

#add by richard
class UnHideAppCommand(WebCommand):
    def __init__(self,receiver):
        super(UnHideAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/showapp/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/hideapp_list.htm'
        payload = {'show_type':0,'ids':[int(app_id)]}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify= False)
        log.debug(r.text)
        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to unhide app')
        return result['detail']

#add by richard
class GetAppHideStatusCommand(WebCommand):
    def __init__(self,receiver):
        super(GetAppHideStatusCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/showapp/?page_size=99999&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/hideapp_list.htm'
        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        for item in result['results']:
            log.debug(item['id'])
            if item['id'] == int(app_id):
                break

        return str(item['hide_flag'])

#add by richard
class EditWorkspaceAppCommand(WebCommand):
    def __init__(self,receiver):
        super(EditWorkspaceAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, description_txt):
        uri = self._uri_prefix + '/api/v1/app/' + str(int (app_id)) + '/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/editMobileApp.htm?type=1&rank=5&variskbitmap=0&app_id=' + str(int (app_id)) + '&frame_id=link_' +str(int (app_id))
        payload = {'description':description_txt}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.put(uri,json.dumps(payload), headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        print 'lllllllllll',result['description']

        return result['description']

#add by richard
class EditWebclipCommand(WebCommand):
    def __init__(self,receiver):
        super(EditWebclipCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, description_txt):
        uri = self._uri_prefix + '/api/v1/app/' + str(int (app_id)) + '/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/editMobileApp.htm?type=2&rank=0&variskbitmap=0&app_id=' + str(int (app_id)) + '&frame_id=link_' +str(int (app_id))
        payload = {'description':description_txt}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.put(uri,json.dumps(payload), headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        print 'lllllllllll',result['description']

        return result['description']

#add by richard
class EditSandboxAppCommand(WebCommand):
    def __init__(self,receiver):
        super(EditSandboxAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, description_txt):
        uri = self._uri_prefix + '/api/v1/app/local_app_edit/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/wrapSettingApp.htm?type=0&app_id=' + str(int (app_id)) + '&frame_id=link_' +str(int (app_id))
        payload = {'description':description_txt, 'id':int (app_id)}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post(uri,json.dumps(payload), headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        print 'lllllllllll',result['detail']

        if not result['code'] == 0:
            raise ValueError ('Fail to edit sandboxapp')
        return result['detail']

#add by richard
class CreateSandboxProfileCommand(WebCommand):

    def __init__(self, receiver):
        super(CreateSandboxProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, profile):

        uri = self._uri_prefix + '/api/v1/policy/template/'

#def __init__(self, name =None, detail=None, sandbox_setting=None, offline_period=None, local_apps=None, mdm_enable=None)


        self.session.mount(uri, HTTPAdapter(max_retries=100))

        sandbox_setting_arr = profile.sandbox_setting.split(',')
        print 'ssssssssssssss',sandbox_setting_arr
#        for item in sandbox_setting_arr:
        restrict_cut = bool( int (sandbox_setting_arr[0]) )
        restrict_share = bool( int (sandbox_setting_arr[1]) )
        restrict_capture = bool( int (sandbox_setting_arr[2]) )
        enforce_encryption = bool( int (sandbox_setting_arr[3]) )
        root_check = bool( int (sandbox_setting_arr[4]) )
        print 'llllllllllllll',root_check

        offline_period = int (profile.offline_period)
#        sandbox_setting_dict = json.dumps({'restrict_cut': restrict_cut, 'restrict_share': restrict_share,
#                                        'restrict_capture': restrict_capture, 'enforce_encryption': enforce_encryption,
#                                        'root_check': root_check, 'offline_period': offline_period})            
        print 'xxxxxxxxxxxxx',profile.local_apps
        local_apps = int(profile.local_apps)
        mdm_enable = bool( int (profile.mdm_enable)) 
        payload = {'name' : profile.name, 'detail' : profile.detail,
                   'priority':profile.priority, 'profile_type':profile.profile_type, "policies" : [ profile.language, profile.wallpaper.id ],
                   'apps' : profile.apps, 'single_app': profile.single_app ,
                   'storage_limit' : profile.storage_limit,
                   'site_info' : profile.site_info,
                   'watermark_enable' : profile.watermark_enable,
                   'watermark_text' : profile.watermark_text,
                   'sandbox_setting' : {'restrict_cut': restrict_cut, 'restrict_share': restrict_share,
                                        'restrict_capture': restrict_capture, 'enforce_encryption': enforce_encryption,
                                        'root_check': root_check, 'offline_period': offline_period}, 
                   'bluetooth_enable':bool(0),'bluetooth_filter_kind':0,'bluetooth_list':[],'bluetooth_enable_rule':bool(0),'bluetooth_rule_list':[],
                   'local_apps': [local_apps],
                   'mdm_enable': mdm_enable
        }

        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix +'/profiles/create.htm?t=' + str ( int ( time.time()* 1000))

        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)
        print 'resultssssssssssss',result
        profile.p_id = result['id']

        self._receiver.profiles[result['id']] = result

        return result["id"]

#add by richard
class DeleteSandboxProfileCommand(WebCommand):
    def __init__(self, receiver):
        super(DeleteSandboxProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__( self, p_ids):

        uri = self._uri_prefix + '/api/v1/policy/template/batch/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        payload = {"action":"delete", "ids":[p_ids]}

        headers = dict(self._headers)
        headers['Referer']= self._uri_prefix + '/profiles/index.htm?t=' + str ( int ( time.time()* 1000))
        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)
        print 'resultssssssssssss',result
        if not result['code'] == 0:
            raise ValueError ('Fail to delete profiles')

        return result['detail']

#add by richard
class ChangeProfileOnUser(WebCommand):

    def __init__(self,receiver):
        super(ChangeProfileOnUser,self).__init__()
        self._receiver = receiver

    def __call__(self,u_id, p_id):

        uri = self._uri_prefix + '/api/v1/account/user/' + str(u_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy': p_id}
        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/users/changeUserProfile.htm?id=' + str ( int ( time.time()* 1000))
        r = self.session.put(uri, json.dumps(payload),headers = headers, verify=False)

        result = json.loads(r.text)

        if not result['id'] == u_id:
            raise ValueError('Invalid User ID on profile assignment')
        
#add by richard
class ChangeProfileOnGroup(WebCommand):

    def __init__(self, receiver):
        super(ChangeProfileOnGroup,self).__init__()
        self._receiver = receiver

    def __call__(self, g_id, p_id):

        uri = self._uri_prefix + '/api/v1/account/group/'+ str(g_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy':p_id}
        print 'xxxxxxxxxxx',p_id
        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/editGroup.htm?id='+ str(g_id)

        r = self.session.put(uri, json.dumps(payload), headers = headers,
                             verify = False)

        result = json.loads(r.text)

        if not result['id'] == g_id:

            raise ValueError('Invalid Group id on profile assignment')

#add by richard
class GetProfileOnGroup(WebCommand):

    def __init__(self, receiver):
        super(GetProfileOnGroup,self).__init__()
        self._receiver = receiver

    def __call__(self, g_id):

        uri = self._uri_prefix + '/api/v1/account/group/'+ str(g_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = str ( int ( time.time()* 1000))

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/index.htm'

        r = self.session.get(uri, data=payload, headers = headers,
                             verify = False)

        result = json.loads(r.text)
        print 'ssssssssssssss',result
        
        policy =  result['policy']
        log.debug(policy['id'])
        p_id = int (policy['id'])
        
        return p_id      

#add by richard
class GetProfileOnUser(WebCommand):

    def __init__(self, receiver):
        super(GetProfileOnUser,self).__init__()
        self._receiver = receiver

    def __call__(self, u_id):

        uri = self._uri_prefix + '/api/v1/account/user/'+ str(u_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = str ( int ( time.time()* 1000))

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/index.htm'

        r = self.session.get(uri, data=payload, headers = headers,
                             verify = False)

        result = json.loads(r.text)
        print 'ssssssssssssss',result

        policy =  result['policy']
        log.debug(policy['id'])
        p_id = int (policy['id'])

        return p_id

#add by richard
class UserBindingOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(UserBindingOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, option_id):

        uri = self._uri_prefix + '/api/v1/account/device/user_bind/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'enable':bool(option_id)}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/device.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)
        print 'ssssssssss',r.status_code
        #result = json.loads(r.text)
        #print 'ssssssssssssss',result

        return str(r.status_code)

#add by richard
class ImportDeviceBindCommand(WebCommand):

    def __init__( self, receiver):
        super(ImportDeviceBindCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, txt):

        uri = self._uri_prefix + '/api/v1/account/device/import/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict(self._headers)
        del headers['content-type']

        headers['Referer'] = self._uri_prefix + '/users/device.htm'
        headers['Upgrade-Insecure-Requests'] = 1

        print 'filenamexxxxxxxxxxxxxx',txt.file_name
        r = self.session.post( uri, data = {u'ext':'txt', u'filename': txt.file_name,
                                            u'csrfmiddlewaretoken': self._csr_token},
                               files={u'filename': txt.dump_data()},
                               headers = headers, verify= False)


        print 'text',r.text
        result = json.loads(r.text)
        print 'detailssssssssssss',result['data']
        
        resultData = result['data']
        print 'llllllllssssssssssss',resultData['success']
        #self._receiver.wallpapers[result['id']] = result

        return str(resultData['success'] )

#add by richard
class UserBindingActionCommand(WebCommand):

    def __init__(self, receiver):
        super(UserBindingActionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, action_id, user_name, device_info):

        uri = self._uri_prefix + '/api/v1/account/device/bind/?page=1&order_field=6&order_by=desc&platform=0&page_size=20&_=' + str ( int ( time.time()* 1000))

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict( self._headers)
        headers['content-type'] = 'application/json'
        headers['Referer'] = self._uri_prefix + '/users/device.htm'
        r = self.session.get( uri, headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )
        
        results = result['results']
        for item in results:
           if (item['username'] == user_name) and (item['device_info'] == device_info):
               device_id = item['id']
               break
        print 'dddddddddd',device_id
#******************************************************************************************************#
        uri = self._uri_prefix + '/api/v1/account/device/bind_action/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'action':int(action_id),'ids':[device_id]}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/device.htm'

        rr = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)
        print 'ssssssssss',rr.status_code

        return str(rr.status_code)

#add by richard
class GetDeviceBindStatusCommand(WebCommand):

    def __init__(self, receiver):
        super(GetDeviceBindStatusCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, user_name, device_info):

        uri = self._uri_prefix + '/api/v1/account/device/bind/?page=1&order_field=6&order_by=desc&platform=0&page_size=20&_=' + str ( int ( time.time()* 1000))

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        headers = dict( self._headers)
        headers['content-type'] = 'application/json'
        headers['Referer'] = self._uri_prefix + '/users/device.htm'
        r = self.session.get( uri, headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )

        results = result['results']
        for item in results:
           if (item['username'] == user_name) and (item['device_info'] == device_info):
               device_status = item['status']
               break
        print 'dddddddddd',device_status
        return str(device_status)

#add by richard
class Unia_cfgOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(Unia_cfgOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, option):

        uri = self._uri_prefix + '/api/v1/cfg/unia_cfg/'
        
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        
        option_arr = option.split(',')
        print 'ssssssssssssss',option_arr
#        for item in sandbox_setting_arr:
        option_anti_screen = bool( int (option_arr[0]) )
        option_root_or_jailbreak = bool( int (option_arr[1]) )
        option_input_method = bool( int (option_arr[2]) )
        option_audio_video = bool( int (option_arr[3]) )
        print 'llllllllllllll',option_root_or_jailbreak
    
        payload = {'anti_screen':option_anti_screen,'root_or_jailbreak':option_root_or_jailbreak,'input_method':option_input_method,'audio_video':option_audio_video,'play_video':0,'play_audio':0,'record_audio':0}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)
        print 'ssssssssss',r.status_code
        #result = json.loads(r.text)
        #print 'ssssssssssssss',result

        return str(r.status_code)

#add by richard
class Remember_passwdOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(Remember_passwdOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, option):

        uri = self._uri_prefix + '/api/v1/cfg/cli_remember_passwd/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        option_remember_passwd = bool( int (option) )

        payload = {'enabled':option_remember_passwd}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)

        return str(r.status_code)

#add by richard
class Auto_alertOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(Auto_alertOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, option):

        uri = self._uri_prefix + '/api/v1/cfg/alert_submit_auto/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        option_remember_passwd = bool( int (option) )

        payload = {'enabled':option_remember_passwd}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)

        return str(r.status_code)

#add by richard
class Ldap_lockOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(Ldap_lockOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, option, lock_num, interval):

        uri = self._uri_prefix + '/api/v1/cfg/ldap_lock/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        option_ldap_lock = bool( int (option) )

        payload = {'enabled':option_ldap_lock,'lock_num':int(lock_num),'interval':int(interval)}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)

        return str(r.status_code)

#add by richard
class Password_levelOptionCommand(WebCommand):

    def __init__(self, receiver):
        super(Password_levelOptionCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, level):

        uri = self._uri_prefix + '/api/v1/cfg/password_level/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        passwdlevel = int (level)

        payload = {'password_level':passwdlevel}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)

        return str(r.status_code)

#add by richard
class SAcfgCommand(WebCommand):

    def __init__(self, receiver):
        super(SAcfgCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, ip, port):

        uri = self._uri_prefix + '/api/v1/cfg/access/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        payload = {'ip':ip,'port':int(port),'reminder':bool(0)}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers,
                             verify = False)

        return str(r.status_code)

#add by richard 2017/04/05
class InsertDeviceMysqlCommand(WebCommand):
#mysql -e "insert into vmi.device_android (user_id, device_name, vendor, model, imei) values(2, 'Android-Sony-E6553', 'Sony', 'E6553', '359057061661440');"
#ssh root@192.168.10.201 "mysql -e \"insert into vmi.device_android (user_id, device_name, vendor, model, imei) values(2, 'Android-Sony-E6553', 'Sony', 'E6553', '359057061661440');\""
    def __init__(self,receiver):
        super(InsertDeviceMysqlCommand,self).__init__()
        self._receiver = receiver

    def __call__(self,device_type,device_name):
       
        random_imei = [random.randrange(0,9) for i in range(1,16)]
        device_imei = ''.join([str(i) for i in random_imei])
        print str(device_imei)

        if device_type == 'android':
            call(['ssh','root@'+self._receiver.host_ip , "mysql -e \"insert into vmi.device_android (user_id, device_name, vendor, model, imei) values(2, '"+str(device_name)+"', 'Sony', 'E6553', '"+str(device_imei)+"');\""])
        else:
            call(['ssh','root@'+self._receiver.host_ip , "mysql -e \"insert into vmi.device_ios (user_id, device_name, vendor, model, imei) values(2, '"+str(device_name)+"', 'Apple', 'MD540ZP', '"+str(device_imei)+"');\""])
#99 000240 139827 4

        uri = self._uri_prefix + '/api/v1/devices/?page=1&order_field=6&order_by=desc&platform=0&page_size=20&_=' + str ( int ( time.time()* 1000))

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers = dict( self._headers)
        headers['content-type'] = 'application/json'
        headers['Referer'] = self._uri_prefix + '/devices/index.htm'
 
        r = self.session.get( uri, headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )
        
        results = result['results']
        for item in results:
           if (item['device_name'] == str(device_name)) and (item['imei'] == str(device_imei)):
               device_id = item['id']
               break
        print 'dddddddddd',device_id
        return str(device_id)

#add by richard 2017/04/06
class MdmEditDeviceCommand(WebCommand):

    def __init__(self,receiver):
        super(MdmEditDeviceCommand,self).__init__()
        self._receiver = receiver

    def __call__(self,device_id,device_type,device_name,asset_number,ownership,description):

        uri = self._uri_prefix + '/api/v1/devices/' + str(device_type) + '/' + str (device_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers = dict( self._headers)
        headers['content-type'] = 'application/json'
        headers['Referer'] = self._uri_prefix + '/devices/editDevice.htm?platform=' + str(device_type) + '&deviceid=' + str (device_id)

        payload = {'id':int(device_id), 'admin_device_name':device_name,
                   'asset_number':asset_number, 'ownership':int(ownership), 'description':description}

        r = self.session.put(uri, data = json.dumps(payload), headers = headers, verify=False)        
        print r.text
        result = json.loads( r.text )

        id = result['id']
        print 'iiiiiidddddd',str(id)
        return str(id)        

#add by richard
class MdmDeleteDeviceCommand(WebCommand):

    def __init__(self, receiver):
        super(MdmDeleteDeviceCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, device_type, device_id):

        uri = self._uri_prefix + '/api/v1/devices/' + str(device_type) + '/' + str(device_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/devices/index.htm'

        r = self.session.delete(uri, headers = headers, verify = False)

        return str(r.status_code)

#add by richard 2017/04/10
class MdmRemoteLocateCommand(WebCommand):
#insert into vmi.device_locationhistory(1, '123.5', '54.8')
#/api/v1/devices/locate-device/android/
#ssh root@192.168.10.201 "mysql -e \"insert into vmi.device_android (user_id, device_name, vendor, model, imei) values(2, 'Android-Sony-E6553', 'Sony', 'E6553', '359057061661440');\""
    def __init__(self,receiver):
        super(MdmRemoteLocateCommand,self).__init__()
        self._receiver = receiver

    def __call__(self,device_type,device_id):

        random_latitude = random.uniform(1, 40)
        device_latitude = round(random_latitude, 5)
        print str(device_latitude)

        random_longitude = random.uniform(1, 140)
        device_longitude = round(random_longitude, 6)

        uri = self._uri_prefix + '/api/v1/devices/locate-device/' + str(device_type) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        headers = dict( self._headers)
        headers['content-type'] = 'application/json'
        headers['Referer'] = self._uri_prefix + '/devices/locateUser.htm?platform=' + str(device_type) + '&deviceid=' + str(device_id)

        payload = {'id':int(device_id)}

        call(['ssh','root@'+self._receiver.host_ip , "mysql -e \"insert into vmi.device_locationhistory ("+str(device_type)+"_id, latitude, longitude) values("+str(device_id)+", '"+str(device_latitude)+"', '"+str(device_longitude)+"');\""])
        
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify = False)
        print r.text
        result = json.loads( r.text )

        result_location = result['location']
        print 'lllooooooccccaaaaaatttiion',result_location
        return str(result_location)

#add by richard
class MdmResetPasswdCommand(WebCommand):

    def __init__(self, receiver):
        super(MdmResetPasswdCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, device_type, device_id):

        uri = self._uri_prefix + '/api/v1/devices/reset-password/' + str(device_type) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/devices/index.htm'
        
        payload = {'id':int(device_id)}
        
        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify = False)

        return str(r.status_code)

#/api/v1/devices/lock-device/ios/
#add by richard
class MdmRemoteLockCommand(WebCommand):

    def __init__(self, receiver):
        super(MdmRemoteLockCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, device_type, device_id, phoneNum, message):

        uri = self._uri_prefix + '/api/v1/devices/lock-device/' + str(device_type) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/devices/lockDevice.htm?platform='+str(device_type)+'&deviceid='+str(device_id)

        payload = {'id':int(device_id),
                   'phone_number':phoneNum, 'message':message}

        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify = False)

        return str(r.status_code)

#add by richard
class MdmRemoteWipeCommand(WebCommand):

    def __init__(self, receiver):
        super(MdmRemoteWipeCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, device_type, device_id):

        uri = self._uri_prefix + '/api/v1/devices/wipe-device/' + str(device_type) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/devices/index.htm'

        payload = {'id':int(device_id)}

        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify = False)

        return str(r.status_code)

class AddWebClipCommand(WebCommand):

    def __init__(self, receiver):
        super(AddWebClipCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, url):

        uri = self._uri_prefix + '/api/v1/app/add-webclip/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'webclip':url}
	headers = dict(self._headers)
	headers['Referer'] = self._uri_prefix + '/apps/addWebApp.htm?type=2'
        r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify=False)
        result = r.text
        uri = self._uri_prefix + '/api/v1/app/'
        payload = json.loads(result)
        payload['rating']=3
        log.debug(json.dumps(payload))
	r = self.session.post( uri, data = json.dumps(payload), headers = headers, verify = False)
        result = json.loads(r.text)
	log.debug(result)
        #print result
        self._receiver.applications[result['id']] = result

        return result['id']

class GetCurrentProfiles(WebCommand):

    def __init__(self, receiver):
        super(GetCurrentProfiles,self).__init__()
        self._receiver = receiver
        self._receiver.profiles = {}

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/policy/template/?page=1&page_size=10000'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        r = self.session.get(uri, headers= self._headers, verify=False)

        result = json.loads(r.text)
        log.debug('There are %d profiles in currrent VMI server'% result['count'])

        for profile in result['results']:
            self._receiver.profiles[ profile['id'] ] = profile


class GetCurrentApplications(WebCommand):

    def __init__(self, receiver):
        super(GetCurrentApplications,self).__init__()
        self._receiver = receiver
        self._receiver.applications = {}

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/app/?page_size=999999'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        r = self.session.get(uri, headers= self._headers, verify=False)

        result = json.loads(r.text)
        log.debug('There are %d applications in current VMI server' % result['count'])

        for app in result['results']:
            self._receiver.applications[ app['id'] ] = app


class CreateGroupCommand(WebCommand):

    '''{"policy": {"id": 1, "name": "Default Profile", "inherited": true}, "last_modified": "2013-07-22T05:39:58.589Z", "removable": true, "id": 3, "name": "group1", "permissions": []}
'''
    def __init__(self, receiver):

        super(CreateGroupCommand,self).__init__()

        self._receiver = receiver

    def __call__(self, group_name='group'):

        uri = self._uri_prefix + '/api/v1/account/group/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'name':group_name, 'policy':'-1'}
        headers = self._headers
        headers['Referer'] = self._uri_prefix + '/users/createGroup.htm?policy=Default%20Profile'
        r = self.session.post(uri, data = json.dumps(payload), headers= headers, verify = False)
        result = json.loads(r.text)
        log.debug(result)
        return result['id']

class CreateUserInGroupCommand(WebCommand):

    '''{"id": 2, "username": "xiang_wang", "is_active": true, "email": "xiang_wang@test.com", "date_joined": "2013-07-22T06:08:21.717586+00:00", "last_login": "2013-07-22T06:08:21.716720+00:00", "first_name": "xiang", "last_name": "wang", "status": 0, "groups": [3], "group_names": ["group1"], "policy": {"id": 2, "name": "profile1", "inherited": true}, "last_modified": "2013-07-22T06:08:21.734Z"}
'''

    def __init__(self,receiver):
        super(CreateUserInGroupCommand,self).__init__()
        self._receiver = receiver

    def __call__(self, group_id , user_name , password ,first_name, last_name , email, policy_id):

        uri = self._uri_prefix + '/api/v1/account/user/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'username': user_name, 'first_name':first_name,
                   'last_name':last_name, 'email':email,
                   'groups':[group_id],'policy':policy_id}

        headers = self._headers
        headers['Referer'] = self._uri_prefix + '/users/createUser.htm?group_id=7&policy=Default%20Profile'
        r = self.session.post(uri, data = json.dumps(payload), headers= headers, verify = False)

        result = json.loads(r.text)
        log.debug(result)
        if  'code' in result and result['code'] == 4007 : raise ValueError('Failed to create user')
        call(['ssh','root@'+self._receiver.host_ip , 'python',
              '/vmi/manager/change_password.py',user_name, password ])

        self.dalService.disable_change_password(user_name)

        u_id = result['id']
        self._receiver.auth_users[u_id] = result
        return u_id
'''
class DeleteUserByID(WebCommand):

    def __init__(self, receiver):
        super(DeleteUserByID, self).__init__()
        self._receiver = receiver

    def __call__(self, u_id):

        uri = self._uri_prefix + '/api/v1/account/user/' + str(u_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)

        r = self.session.delete(uri, headers = self._headers, verify=False)

        result = r.text
        if ud.normalize('NFC', result) == ud.normalize('NFC', unicode(u_id)):
            raise ValueError("Fail to delete user with id %d "% u_id)
'''
class DeleteUserByID(WebCommand):

    def __init__(self, receiver):
        super(DeleteUserByID, self).__init__()
        self._receiver = receiver

    def __call__(self, u_id):

        uri = self._uri_prefix + '/api/v1/account/user/batch/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'action':'delete','ids':[int(u_id)]}
        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/users/index.htm'
        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)


class SetGroupProfile(WebCommand):

    def __init__(self,receiver):
        super(SetGroupProfile, self).__init__()
        self._receiver =receiver

    def __call__(self, group_id, policy_id):

        uri = self._uri_prefix + '/api/v1/account/group/' + str(group_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy':str(policy_id)}

        r = self.session.put(uri, data = json.dumps(payload), headers = self._headers, verify=False)

        result = json.loads(r.text)

        if not  result['id'] == group_id :

            raise ValueError("Fail to set group profile")


class GetCurrentGroups(WebCommand):

    def __init__(self,receiver):
        super(GetCurrentGroups, self).__init__()
        self._receiver = receiver
        self._receiver.groups = {}

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/account/tree/?id=1'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        log.debug(uri)
        r = self.session.get(uri,headers= self._headers, verify=False)
        result = json.loads(r.text)

        for group in result:
            self._receiver.groups[group['id']] = group

'''
class GetProfileIDByName(WebCommand):

    def __init__(self,receiver):
        super(GetProfileIDByName, self).__init__()
        self._receiver = receiver

    def __call__(self, profile_name):

        uri = self._uri_prefix + '/api/v1/policy/template/?page=1&page_size=10000'

        r = self.session.get(uri)

        result = json.loads(r.text)

        for profile in result['results']:
            if profile['name'] == profile_name:
                return profile['id']

        raise ValueError("Invalid profile name %s to find profile id" % profile_name)

'''
class GetCurrentUsers(WebCommand):

    def __init__(self,receiver):

        super(GetCurrentUsers,self).__init__()
        self._receiver = receiver
        self._receiver.auth_users = {}
    def __call__(self):

        uri = self._uri_prefix + '/api/v1/account/user/?page=1&page_size=10000&groups=1'
        headers = dict(self._headers)
        headers['Referer'] =self._uri_prefix + '/usr/index.html'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        r = self.session.get(uri,headers = headers, verify = False)
        result = json.loads(r.text)

        for user in result['results']:
            self._receiver.auth_users[ user['id'] ] = user

#replaced by assign_profile_on_user
class SetUserProfile(WebCommand):

    def __init__(self,receiver):

        super(SetUserProfile,self).__init__()
        self._receiver = receiver

    def __call__(self, user_id, profile_id):

        uri = self._uri_prefix + '/api/v1/account/user/' + str(user_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy':profile_id}
        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/users/changeUserProfile.htm'
        r = self.session.put(uri, data = json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)

        if not result['id'] == user_id:
            raise ValueError("Invalid User to set profile")

class CreateProfileCommand(WebCommand):

    def __init__(self, receiver):
        super(CreateProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, profile):

        uri = self._uri_prefix + '/api/v1/policy/template/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'name' : profile.name, 'detail' : profile.detail,
                   'priority':-1, "policies" : [ profile.language, profile.wallpaper.id ],
                   'apps' : profile.apps, 'single_app': profile.single_app ,
                   'storage_limit' : profile.storage_limit,
		   'site_info' : profile.site_info,
		   'watermark_enable' : profile.watermark_enable,
                   'watermark_text' : profile.watermark_text,
                   'bluetooth_enable':bool(0),'bluetooth_filter_kind':0,'bluetooth_list':[],'bluetooth_enable_rule':bool(0),'bluetooth_rule_list':[]	
        }

        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix +'/profiles/create.htm?t=' + str ( int ( time.time()* 1000))

        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)

        profile.p_id = result['id']

        self._receiver.profiles[result['id']] = result

        return result["id"]

class AssignProfileOnUser(WebCommand):

    def __init__(self,receiver):
        super(AssignProfileOnUser,self).__init__()
        self._receiver = receiver

    def __call__(self,u_id, p_id):

        uri = self._uri_prefix + '/api/v1/account/user/' + str(u_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy': p_id}
        headers = dict( self._headers)
        headers['Referer'] = self._uri_prefix + '/users/changeUserProfile.htm'
        r = self.session.put(uri, json.dumps(payload),headers = headers, verify=False)

        result = json.loads(r.text)

        if not result['id'] == u_id:
            raise ValueError('Invalid User ID on profile assignment')

class AssignProfileOnGroup(WebCommand):

    def __init__(self, receiver):
        super(AssignProfileOnGroup,self).__init__()
        self._receiver = receiver

    def __call__(self, g_id, p_id):

        uri = self._uri_prefix + '/api/v1/account/group/'+ str(g_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'policy':p_id}

        headers = dict( self._headers)

        headers['Referer'] = self._uri_prefix + '/users/editGroup.htm'

        r = self.session.put(uri, json.dumps(payload), headers = headers,
                             verify = False)

        result = json.loads(r.text)

        if not result['id'] == g_id:

            raise ValueError('Invalid Group id on profile assignment')

class DeleteProfileCommand(WebCommand):
    def __init__(self, receiver):
        super(DeleteProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__( self, p_ids):

        uri = self._uri_prefix + '/api/v1/policy/template/batch/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        payload = {"action":"delete", "ids":p_ids}

        headers = dict(self._headers)
        headers['Referer']= self._uri_prefix + '/profiles/index.htm'
        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)

        if not result['code'] == 0:
            raise ValueError ('Fail to delete profiles')

class SetActiveDirectory(WebCommand):
    def __init__(self, receiver):
        super(SetActiveDirectory, self).__init__()
        self._receiver = receiver

    def __call__(self, host, port = 389, user = 'user', password='pass', enable_tls=False):

        uri = self._uri_prefix + '/api/v1/cfg/?page_size=1000000&group=ldap'
	self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers= self._headers, verify=False)

        result = json.loads(r.text)
        ldap_payload = result['results']

	uri = self._uri_prefix + '/api/v1/cfg/ldap/'
	self.session.mount(uri, HTTPAdapter(max_retries=100))

        encrypt = encode_with_pkcs7_bf('#$vmi4trend', password)

        payload = { 'basedn_input' : '', 'btn_sync_ldap':'Manual Update',
                    'ldap_enable_ldap':True ,
                    'ldap_group_attr_map_email':'mail',
                    'ldap_group_attr_map_user':'member',
                    'ldap_group_search_filter':'(objectClass=group)',
                    'ldap_host' : host,
                    'ldap_password': encrypt,
                    'ldap_port' : port,
                    'ldap_use_tls' : enable_tls,
                    'ldap_user' : user,
                    'ldap_user_attr_map':'mail',
                    'ldap_user_attr_map_first_name':'givenNanme',
                    'ldap_user_attr_map_last_name' : 'sn',
                    'ldap_user_attr_map_username' : 'sAMAccountName',
                    'ldap_user_search_filter': '(objectClass=person)',
                    'proxy_port' :'',
                    'select_base_dn' :''}
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)
        result = json.loads(r.text)
        if not result['code'] == 0: raise ValueError('Failed to setup AD')
        base_dns = result['detail']['base_dn']
        #  ["DC=tw,DC=trendnet,DC=org", "DC=trendnet,DC=org"]
        base_dns_str = None
        if len(base_dns) > 1 :
            base_dns_str = ";".join(base_dns)
        else:
            base_dns_str = base_dns[0]
        uri = self._uri_prefix + '/api/v1/cfg/'
	self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'
        for i in range(len(ldap_payload)):
            if ldap_payload[i]['name'] == 'host' : ldap_payload[i]['value'] =host
            elif ldap_payload[i]['name'] == 'port' : ldap_payload[i]['value'] = port
            elif ldap_payload[i]['name'] == 'user' : ldap_payload[i]['value'] = user
            elif ldap_payload[i]['name'] == 'password' : ldap_payload[i]['value'] = encrypt
            elif ldap_payload[i]['name'] == 'use_tls' : ldap_payload[i]['value'] = enable_tls
            elif ldap_payload[i]['name'] == 'enable_ldap' : ldap_payload[i]['value'] = True
            elif ldap_payload[i]['name'] == 'base_dns' : ldap_payload[i]['value'] = base_dns_str
            elif ldap_payload[i]['name'] == 'select_base_dn' : ldap_payload[i]['value'] =  base_dns[0]
        payload = {'results': ldap_payload}
        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)
        if not json.loads(r.text)['code'] == 0 : raise ValueError('Failed to setup Active Directory')

class DisableActiveDirectory(WebCommand):

    def __init__(self, receiver):
        super(DisableActiveDirectory, self).__init__()
        self._receiver = receiver

    def __call__(self):
        uri = self._uri_prefix + '/api/v1/cfg/?page_size=1000000&group=ldap'
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers= self._headers, verify=False)

        result = json.loads(r.text)
        ldap_payload = result['results']

 	uri = self._uri_prefix + '/api/v1/cfg/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

	for i in range(len(ldap_payload)):
	    if ldap_payload[i]['name'] == 'enable_ldap' : ldap_payload[i]['value'] = False

	payload = {'results': ldap_payload}

        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)
        if not json.loads(r.text)['code'] == 0 : raise ValueError('Failed to disable Active Directory')

class SearchGroupOrUsersCommand(WebCommand):

    def __init__(self, receiver):
        super(SearchGroupOrUsersCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, key):

        uri = self._uri_prefix + '/api/v1/account/ldap/groupou/?key='\
              + urllib.quote(key) + '&size=30&type=3'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        r = self.session.get(uri, headers= self._headers, verify=False)

        print r.text

        return r.text

class ImportGroupOrUsersCommand(WebCommand):

    def __init__(self, receiver):

        super(ImportGroupOrUsersCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, key, o_name, o_type):

        uri = self._uri_prefix + '/api/v1/account/ldap/groupou/?key='\
              + urllib.quote(key) + '&size=30&type=3'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        r = self.session.get(uri, headers= self._headers, verify=False)

        result = json.loads(r.text)
        print result
        find = False
        dn = None
        for item in result:
            for cns in item['cn']:
                if cns == o_name and item['type'] == o_type:
                    if item['is_in_db'] == True: raise ValueError('%s is already imported'%(o_name))
                    find = True
                    dn = item['dn']
                    break

        if not find : raise ValueError('%s is not found'%(o_name))

        uri = self._uri_prefix + '/api/v1/account/import-groups/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/users/importGroup.htm'
        payload = [{'name': o_name, 'dn': dn, 'type':o_type}]
        print payload
        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)
        log.debug(r.text)
        if not result['code'] == 0: raise ValueError('Failed to import user %s'
                                                     % (o_name))


class EnableOrDisableUserCommand(WebCommand):

    def __init__(self, receiver):
        super(EnableOrDisableUserCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, user_id ,  is_enable=False):

        uri = self._uri_prefix + '/api/v1/account/user/' + str(user_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer']= self._uri_prefix + '/users/index.htm'

        payload = {'is_active': is_enable }
        r = self.session.put(uri, json.dumps(payload), headers= headers, verify= False)

        result = json.loads(r.text)
        log.debug(r.text)
        if not int(result['id']) == int(user_id):
            raise ValueError('Failed to enable or disable user')



class WipeUserCommand(WebCommand):

    def __init__(self, receiver):
        super(WipeUserCommand, self).__init__()
        self._receiver = receiver


    def __call__(self, user_id):

        uri = self._uri_prefix + '/api/v1/account/user/wipe-data/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers =  dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/users/index.htm'

        payload = {'id' : int(user_id)}

        r = self.session.post(uri , json.dumps(payload),
                              headers = headers ,
                              verify = False)

        log.debug(r.text)
        result = json.loads(r.text)
        if not 'code' in result or not result['code'] == 0 :
            raise ValueError ('Failed to wipe user')

class ClearWorkspaceScreenLockCommand(WebCommand):

    def __init__(self, receiver):
        super(ClearWorkspaceScreenLockCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, user_id):

        uri = self._uri_prefix + '/api/v1/account/user/rest-pattern/'
        self.session.mount(uri,HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/users/index.htm'

        r = self.session.post(uri, json.dumps({'id': str(user_id)}) ,
                              headers = headers,
                              verify = False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'code' in result or not result['code'] == 0:
            raise valueError('Failed to clear workspace screen lock')

class GetConfigAccessCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigAccessCommand, self).__init__()
        self._receiver = receiver

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/access/?_=' + str(current_time_millis())
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri , headers = headers, verify= False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'ip' in result and not 'port' in result:
            raise ValueError('Failed to get access configuration')

        return AccessSetting(result['ip'], result['port'])

class GetConfigRememberPasswordCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigRememberPasswordCommand, self).__init__()
        self._receiver = receiver


    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/cli_remember_passwd/?_=' + str(current_time_millis())
        self.session.mount(uri , HTTPAdapter(max_retries= 100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers = headers , verify = False)

        log.debug(r.text)

        result = json.loads(r.text)
        if not 'enabled' in result :
            raise ValueError('Failed to get remember password config')

        return result['enabled']


class GetConfigADRestrictCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigADRestrictCommand, self).__init__()
        self._receiver = receiver


    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/ldap_lock/?_=' + str(current_time_millis())
        self.session.mount(uri, HTTPAdapter(max_retries= 100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers = headers, verify = False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'lock_num' in result:
            raise ValueError('Failed to get ad restrict setting')

        ad_restrict = ADRestrictSetting(result['lock_num'],
                                        result['interval'])

        if result['enable']:

            ad_restrict.enable= 'enabled'
        else:
            ad_restrict.enable = 'disabled'

        return ad_restrict


class GetConfigUniaIdleTimeCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigUniaIdleTimeCommand, self).__init__()
        self._receiver = receiver

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/unia_idletime/?_=' + str(current_time_millis())
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers= headers, verify = False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'idle_time' in result :
            raise ValueError('Failed to get unia idle time')

        return result['idle_time']


class GetConfigVIPNumberCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigVIPNumberCommand, self).__init__()
        self._receiver = receiver

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/vip_number/?_=' + str(current_time_millis())
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers = headers , verify = False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'vip_number' in result:
            raise ValueError('Failed to get vip number')

        return result['vip_number']


class GetConfigProxyCommand(WebCommand):

    def __init__(self, receiver):
        super(GetConfigProxyCommand, self).__init__()
        self._receiver = receiver

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/cfg/proxy/?_=' + str(current_time_millis())
        self.session.mount(uri, HTTPAdapter(max_retries=100))

        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'

        r = self.session.get(uri, headers= headers, verify = False)

        log.debug(r.text)

        result = json.loads(r.text)

        if not 'ip' in result and not 'port' in result:
            raise ValueError('Failed to get proxy setting')

        proxy = ProxySetting( result['ip'], result['port'], result['username'],
                              result['password'])
	log.debug(proxy)
        #if result['enable'] :
        #    proxy.enable = 'enabled'
        #else:
        #    proxy.enable = 'disabled'

        proxy.bypass_address = result['bypass_address']

        return proxy


#add by gannicus
class UpdateProfileCommand(WebCommand):

    def __init__(self, receiver):
        super(UpdateProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, profile):

        uri = self._uri_prefix + '/api/v1/policy/template/' + str(profile.p_id) + '/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'name' : profile.name, 'detail' : profile.detail,
                   'priority':-1, "policies" : [ profile.language, profile.wallpaper.id ],
                   'apps' : profile.apps, 'single_app': profile.single_app ,
                   'storage_limit' : profile.storage_limit,
                   'site_info' : profile.site_info,
                   'watermark_enable' : profile.watermark_enable,
                   'watermark_text' : profile.watermark_text,
                   'bluetooth_enable':bool(0),'bluetooth_filter_kind':0,'bluetooth_list':[],'bluetooth_enable_rule':bool(0),'bluetooth_rule_list':[]
        }

        headers = dict(self._headers)

	headers['Referer'] = self._uri_prefix +'/profiles/edit.htm?profile_id='+str(profile.p_id)+'&order=1'
	log.debug(json.dumps(payload))
        r = self.session.put(uri, json.dumps(payload), headers = headers, verify = False)
        
	result = json.loads(r.text)
	log.debug(result)
        profile.p_id = result['id']

        self._receiver.profiles[result['id']] = result

        return result["id"]


#add by gannicus
class UpdateWebclipIconCommand(WebCommand):
    def __init__(self, receiver):
        super(UpdateWebclipIconCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, icon_filename):

        uri = self._uri_prefix + '/api/v1/app/upload-icon/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {u'filename' : icon_filename, u'csrfmiddlewaretoken':self._csr_token}
        headers = dict(self._headers)
	del headers['content-type']
	headers['Referer'] = self._uri_prefix +'/apps/editMobileApp.htm?type=2&rank=0&variskbitmap=0&app_id=' + str(app_id) + '&frame_id=link_' + str(app_id)
        log.debug(payload)
	r = self.session.post(uri, data = payload, files= {u'icon_file_path': open(os.path.join(os.path.dirname(__file__), '..', 'data', 'icons', icon_filename) , 'rb').read()}, headers = headers, verify = False)
        
	result = json.loads(r.text)
	result[u'description'] = ''
	result[u'icon_url'] = result[u'icon']
	log.debug(result)
	uri = self._uri_prefix + '/api/v1/app/' + str(app_id) + '/'
	self.session.mount(uri, HTTPAdapter(max_retries=100))
	headers['content-type'] = 'application/json'
	r = self.session.put(uri, data = json.dumps(result), headers = headers, verify = False)
	
	log.debug(r.text)
	result = json.loads(r.text)
	log.debug(result)
	if not result['id'] == app_id:
	    raise ValueError('Update icon error')	
	
        return result["id"]


#add by gannicus
class EditAdminInfoCommand(WebCommand):

    def __init__(self, receiver):
        super(EditAdminInfoCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, email, first_name='', last_name=''):

	uri = self._uri_prefix + '/api/v1/account/user-admin/1/'

	self.session.mount(uri, HTTPAdapter(max_retries=100))
	payload = {'username' : 'admin', 'first_name' : first_name,
	           'last_name':last_name, "email" : email
	}

	headers = dict(self._headers)

	headers['Referer'] = self._uri_prefix + '/administration/admin_profile.htm'
	r = self.session.put(uri, json.dumps(payload), headers = headers, verify = False)

	status = r.status_code
	if not status == 200:
	    raise ValueError('Edit admin error')



#add by gannicus
class EditAdminInfoCommand(WebCommand):

    def __init__(self, receiver):
        super(EditAdminInfoCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, email, first_name='', last_name=''):

	uri = self._uri_prefix + '/api/v1/account/user-admin/1/'

	self.session.mount(uri, HTTPAdapter(max_retries=100))
	payload = {'username' : 'admin', 'first_name' : first_name,
	           'last_name':last_name, "email" : email
	}

	headers = dict(self._headers)

	headers['Referer'] = self._uri_prefix + '/administration/admin_profile.htm'
	r = self.session.put(uri, json.dumps(payload), headers = headers, verify = False)

	status = r.status_code
	if not status == 200:
	    raise ValueError('Edit admin error')



#add by gannicus
class EditAdminInfoCommand(WebCommand):

    def __init__(self, receiver):
        super(EditAdminInfoCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, email, first_name='', last_name=''):

	uri = self._uri_prefix + '/api/v1/account/user-admin/1/'

	self.session.mount(uri, HTTPAdapter(max_retries=100))
	payload = {'username' : 'admin', 'first_name' : first_name,
	           'last_name':last_name, "email" : email
	}

	headers = dict(self._headers)

	headers['Referer'] = self._uri_prefix + '/administration/admin_profile.htm'
	r = self.session.put(uri, json.dumps(payload), headers = headers, verify = False)

	status = r.status_code
	log.debug(status)
	if not status == 200:
	    raise ValueError('Edit admin error')

#add by gannicus
class SetLdapLockCommand(WebCommand):
    def __init__(self, receiver):
        super(SetLdapLockCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, lock_num = 2, interval = 30):

	uri = self._uri_prefix + '/api/v1/cfg/ldap_lock/'

	self.session.mount(uri, HTTPAdapter(max_retries=100))
	payload = {'lock_num' : lock_num, 'interval' : interval, 'enabled': True}

	headers = dict(self._headers)

	headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'
	r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

	status = r.status_code
	if not status == 200:
	    raise ValueError('Set LDAP lock error')

#add by gannicus
class GetInstanceLimitationCommand(WebCommand):

    def __init__(self, receiver):
        super(GetInstanceLimitationCommand, self).__init__()
        self._receiver = receiver

    def __call__(self):

        uri = self._uri_prefix + '/api/v1/system/servers/hypervisor/1/?_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/servers/index.htm'
        r = self.session.get(uri, headers = headers , verify = False)
        
        log.debug(r.text)
        result = json.loads(r.text)
        if not 'data' in result:
            raise ValueError('Failed to get capacity')
        return result['data']['servers'][0]['capacity']


#add by gannicus
class SetProxySettingCommand(WebCommand):
    def __init__(self,receiver):
        super(SetProxySettingCommand, self).__init__()
        self._receiver =receiver

    def __call__(self, proxy):
        uri = self._uri_prefix + '/api/v1/cfg/proxy/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {u'username':proxy.username, u'port':proxy.port, u'password':proxy.password, u'ip':proxy.ip, u'enable':proxy.enable, u'bypass_address':proxy.bypass_address}
	headers = dict(self._headers)
	headers['Referer'] = self._uri_prefix + '/administration/systemsettings.htm'	
	log.debug(payload)
        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify=False)
        #result = json.loads(r.text)


#add by gannicus
class GetAppRisklevelCommand(WebCommand):
    def __init__(self,receiver):
	super(GetAppRisklevelCommand, self).__init__()
	self._receiver = receiver
	
    def __call__(self, app_id):
	uri = self._uri_prefix + '/api/v1/app/?page_size=999999&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/apps/index.htm'

        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

	for item in result['results']:
	    log.debug(item['id'])
	    if item['id'] == app_id:
		break
	
	return str(item['risklevel'])

#add by richard
class GetWorkspaceAppPackeNameCommand(WebCommand):
    def __init__(self,receiver):
        super(GetWorkspaceAppPackeNameCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/?page_size=999999&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/apps/index.htm'

        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        for item in result['results']:
            log.debug(item['id'])
            if item['id'] == app_id:
                break

        return str(item['package'])

#add by richard
class GetSandboxAppPackageNameCommand(WebCommand):
    def __init__(self,receiver):
        super(GetSandboxAppPackageNameCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/loc-app/?page_size=999999&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/apps/index.htm'

        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        for item in result['results']:
            log.debug(item['id'])
            if item['id'] == app_id:
                break

        return str(item['package'])	

#add by richard
class GetSandboxAppDescriptionCommand(WebCommand):
    def __init__(self,receiver):
        super(GetSandboxAppDescriptionCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id):
        uri = self._uri_prefix + '/api/v1/app/loc-app/?page_size=999999&_=' + str ( int ( time.time()* 1000))
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)
        headers['Referer'] = self._uri_prefix + '/apps/index.htm'

        r = self.session.get(uri, headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        for item in result['results']:
            log.debug(item['id'])
            if item['id'] == app_id:
                break

        return str(item['description'])

#add by richard 20170725
class CreateBluetoothProfileCommand(WebCommand):

    def __init__(self, receiver):
        super(CreateBluetoothProfileCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, profile):

        uri = self._uri_prefix + '/api/v1/policy/template/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        '''
        bluetooth profile content:
            self.bluetooth_enable = bluetooth_enable
            self.bluetooth_filter_kind = 0
            self.bluetooth_name = bluetooth_name
            self.bluetooth_kind = bluetooth_kind
            self.bluetooth_enable_rule = False
            self.device_uuid = device_uuid
            self.service_uuid = service_uuid
            self.out_channel = out_channel
            self.in_channel = in_channel
        bluetooth_list = [{"bluetooth_name":, "bluetooth_kind": }]
        //00:12:36:2A:23:4D
        bluetooth_rule_list = [{"device_uuid":, "service_uuid":, "out_channel":, "in_channel":}]
        //0000FFE0-0000-1000-8000-00805F9B34FB
        '''

        print 'ssssssssssssss',profile.bluetooth_filter_kind 
        if int(profile.bluetooth_filter_kind) == 0:

            a_bluetooth_list = []
        else:
            a_bluetooth_list = [{"bluetooth_name": profile.bluetooth_name, "bluetooth_kind": profile.bluetooth_kind}]


        if 0 == int(profile.bluetooth_enable_rule):
            a_bluetooth_rule_list = []
        else:
            a_bluetooth_rule_list = [{"device_uuid": profile.device_uuid, "service_uuid": profile.service_uuid, "out_channel": profile.out_channel, "in_channel": profile.in_channel}]


        payload = {'name' : profile.name, 'detail' : profile.detail,
                   'priority':-1, "policies" : [ profile.language, profile.wallpaper.id ],
                   'apps' : profile.apps, 'single_app': profile.single_app ,
                   'storage_limit' : profile.storage_limit,
                   'site_info' : profile.site_info,
                   'watermark_enable' : profile.watermark_enable,
                   'watermark_text' : profile.watermark_text,
                   'bluetooth_enable': bool(profile.bluetooth_enable),
                   'bluetooth_filter_kind': profile.bluetooth_filter_kind,
                   'bluetooth_list': a_bluetooth_list,
                   'bluetooth_enable_rule': bool(profile.bluetooth_enable_rule),
                   'bluetooth_rule_list': a_bluetooth_rule_list
        }

        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix +'/profiles/create.htm?t=' + str ( int ( time.time()* 1000))

        r = self.session.post(uri, json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)

        profile.p_id = result['id']

        self._receiver.profiles[result['id']] = result

        return result["id"]

#add by richard 0727
class UpdateCloudAppCommand(WebCommand):
    def __init__(self, receiver):
        super(UpdateCloudAppCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, description, name, sso_enable):

        uri = self._uri_prefix + '/api/v1/app/' + str(app_id) + '/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {u'description' : description, u'name':name, u'sso_enable': bool(sso_enable)}
        headers = dict(self._headers)
        del headers['content-type']

        headers['Referer'] = self._uri_prefix +'/apps/editMobileApp.htm?type=1&rank=100&upload_status=0&variskbitmap=0&app_id=' + str(app_id) + '&frame_id=link_' + str(app_id)
        headers['content-type'] = 'application/json'

        r = self.session.put(uri, data = json.dumps(payload), headers = headers, verify = False)

        result = json.loads(r.text)
        log.debug(result)
        if not result['id'] == app_id:
            raise ValueError('Update app error')

        return result["id"]

#add by richard 0727
class UpdateSandboxAppSSOCommand(WebCommand):
    def __init__(self, receiver):
        super(UpdateSandboxAppSSOCommand, self).__init__()
        self._receiver = receiver

    def __call__(self, app_id, description, name, sso_enable):
        uri = self._uri_prefix + '/api/v1/app/local_app_edit/'
        self.session.mount(uri, HTTPAdapter(max_retries=100))
        headers = dict(self._headers)

        headers['Referer'] = self._uri_prefix + '/apps/wrapSettingApp.htm?type=0&app_id=' + str(int (app_id)) + '&frame_id=link_' +str(int (app_id))
        payload = {'description':description, 'id':int (app_id), 'name': name, 'sso_enable': bool(sso_enable)}
        print 'sssssssssss',json.dumps(payload)
        r = self.session.post(uri,json.dumps(payload), headers = headers , verify = False)
        log.debug(r.text)
        result = json.loads(r.text)

        print 'lllllllllll',result['detail']

        if not result['code'] == 0:
            raise ValueError ('Fail to edit sandboxapp sso')
        return result['detail']

class PerformanceSuperlab(WebCommand):
    def __init__(self,receiver):
        super(PerformanceSuperlab,self).__init__()
        self._receiver = receiver

    def __call__(self):

        self.config = Configure.Instance()

        config = self.config

        ip = config['Superlab']['host']
        passwd = config['Superlab']['password']
        cmd = "cd /root/vmi_client; ./run_test_3user.sh & > /home/run_test.log"

        ret = -1
        
        ssh = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd))
        try:
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=15)
            if i == 0 :
                ssh.sendline(passwd)
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect('password: ')
                ssh.sendline(passwd)
            ssh.sendline(cmd)
            r = ssh.read()
            print r
            ret = 0
        except pexpect.EOF:
            print "EOF"
            ssh.close()
            ret = -1
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh.close()
            ret = -2

        return str(ret)

class CollectSysInfo(WebCommand):

    def __init__(self,receiver):
        super(CollectSysInfo,self).__init__()
        self._receiver = receiver

    def __call__(self):

        self.config = Configure.Instance()

        config = self.config

        ip = config['UniaServer']['web_ip']
        passwd = config['UniaServer']['password']
        cmd1 = "rm -rf /home/tmvmi/sar*.txt;sar -u 2 300 >> /home/tmvmi/sarCpuData.txt &"
        cmd2 = "sar -r 2 300 >> /home/tmvmi/sarMemData.txt &"

        ret = -1

        ssh1 = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd1))
        try:
            ssh1.sendline(cmd1)
            r1 = ssh1.read()
            print r1
            ret = 0
        except pexpect.EOF:
            print "EOF"
            ssh1.close()
            ret = -1

        ssh2 = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd2))
        try:
            ssh2.sendline(cmd2)
            r2 = ssh2.read()
            print r2
            ret = 0
        except pexpect.EOF:
            print "EOF"
            ssh2.close()
            ret = -1

        return str(ret)

class HandleInfoData(WebCommand):

    def __init__(self,receiver):
        super(HandleInfoData,self).__init__()
        self._receiver = receiver

    def __call__(self):

        self.config = Configure.Instance()

        config = self.config

        ip = config['UniaServer']['web_ip']
        passwd = config['UniaServer']['password']
        cmdline = 'scp root@%s:/home/tmvmi/* /root/vmi/' % (ip)   
        ret = -1

        ssh = pexpect.spawn(cmdline)
        try:  
            ssh.sendline(cmdline)
            r = ssh.read()
            print r
            ret = 0
            print "uploading"
        except pexpect.EOF:
            print "EOF"
            ssh.close()
            ret = -1

        return str(ret)

class HandleUniaLoginTime(WebCommand):

    def __init__(self,receiver):
        super(HandleUniaLoginTime,self).__init__()
        self._receiver = receiver

    def __call__(self):

        self.config = Configure.Instance()

        config = self.config

        ip = config['Superlab']['host']
        passwd = config['Superlab']['password']
        cmdline = 'scp root@%s:/root/vmi_client/log/superlab-*.log /root/vmi/' % (ip)
        ret = -1

        ssh = pexpect.spawn(cmdline)
        try:
            ssh.sendline(cmdline)
            ssh.expect(['root@%s\'s' % (ip),'password:'], timeout=15)
            ssh.sendline(passwd)
            r = ssh.read()
            print r
            ret = 0
            print "uploading"
        except pexpect.EOF:
            print "EOF"
            ssh.close()
            ret = -1

        return str(ret)

class CountUniaLoginTime(WebCommand):

    def __init__(self,receiver):
        super(CountUniaLoginTime,self).__init__()
        self._receiver = receiver

    def __call__(self, user_id):

        self.config = Configure.Instance()

        config = self.config
        userID = user_id

        cmd_start = 'grep \'INFO | LoginManager | request the login API\' /root/vmi/superlab-%s.log |awk \'{print $2}\'' % (userID)
        cmd_end = 'grep \'DEBUG | UniaEngine | onUniaImageReady\' /root/vmi/superlab-%s.log |awk \'{print $2}\'' % (userID)

        login_start = commands.getoutput(cmd_start)
        login_end = commands.getoutput(cmd_end)
        print login_start
        print login_end
        time_start = datetime.datetime.strptime(login_start,"%H:%M:%S:%f")
        time_end = datetime.datetime.strptime(login_end,"%H:%M:%S:%f")
        #login_time = (time_end-time_start).seconds
        
        startTime = time.mktime(time_start.timetuple()) * 1000 + time_start.microsecond / 1000
        endTime = time.mktime(time_end.timetuple()) * 1000 + time_end.microsecond / 1000
        print 'startTime',startTime
        print 'endTime',endTime        
        login_time = endTime - startTime
        print 'login_time',login_time
        
        cmd_record = 'echo -e %s >> /root/vmi/%s.txt' % (str(login_time), userID)
        os.system(cmd_record) 
        return str(login_time)

class Draw_MatplotlibServer(WebCommand):

    def __init__(self,receiver):
        super(Draw_MatplotlibServer,self).__init__()
        self._receiver = receiver

    def __call__(self):

        self.config = Configure.Instance()

        config = self.config

        ip = config['MatplotlibServer']['host']
        passwd = config['MatplotlibServer']['password']
        cmdline = 'scp /root/vmi/10001001001.txt /root/vmi/10001001002.txt /root/vmi/10001001003.txt /root/vmi/droidLoginTime.txt root@%s:/home/y00211003/' % (ip)
        ret = -1

        ssh = pexpect.spawn(cmdline)
        try:
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=15)
            if i == 0 :
                ssh.sendline(passwd)
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect(['root@%s\'s' % (ip),'password:'], timeout=15)
                ssh.sendline(passwd)
            ssh.sendline(cmdline)
            r = ssh.read()
            print r
            ret = 0
        except pexpect.EOF:
            print "EOF"
            ssh.close()
            ret = -1
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh.close()
            ret = -2

#            ssh.sendline(cmdline)
#            ssh.expect(['root@%s\'s' % (ip),'password:'], timeout=15)
#            ssh.sendline(passwd)
#            r = ssh.read()
#            print r
#            ret = 0
#            print "uploading"
#        except pexpect.EOF:
#            print "EOF"
#            ssh.close()
#            ret = -1

        cmd2 = "cd /home/y00211003;./matplotlib_vmi.sh &"
        ssh2 = pexpect.spawn('ssh root@%s "%s"' % (ip, cmd2))
        try:
            i = ssh2.expect(['password:', 'continue connecting (yes/no)?'], timeout=15)
            if i == 0 :
                ssh2.sendline(passwd)
            elif i == 1:
                ssh2.sendline('yes\n')
                ssh2.expect(['root@%s\'s' % (ip),'password:'], timeout=15)
                ssh2.sendline(passwd)
            ssh2.sendline(cmd2)
            r2 = ssh2.read()
            print r2
            ret2 = 0
        except pexpect.EOF:
            print "EOF"
            ssh2.close()
            ret = -1
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh2.close()
            ret = -2

        cmd3 = 'scp root@%s:/home/y00211003/*.png /root/vmi/' % (ip)
        ssh3 = pexpect.spawn(cmd3)
        try:
            i = ssh3.expect(['password:', 'continue connecting (yes/no)?'], timeout=15)
            if i == 0 :
                ssh3.sendline(passwd)
            elif i == 1:
                ssh3.sendline('yes\n')
                ssh3.expect(['root@%s\'s' % (ip),'password:'], timeout=15)
                ssh3.sendline(passwd)
            ssh3.sendline(cmd3)
            r3 = ssh3.read()
            print r3
            ret3 = 0
        except pexpect.EOF:
            print "EOF"
            ssh3.close()
            ret = -1
        except pexpect.TIMEOUT:
            print "TIMEOUT"
            ssh3.close()
            ret = -2

        return str(ret)

#add by gannicus
class SetVipCommand(WebCommand):
    def __init__(self,receiver):
        super(SetVipCommand, self).__init__()
        self._receiver =receiver

    def __call__(self, u_id):

        uri = self._uri_prefix + '/api/v1/account/user/vip/'

        self.session.mount(uri, HTTPAdapter(max_retries=100))
        payload = {'id' : [u_id], 'is_vip' : True}
	log.debug(payload)
	headers = dict(self._headers)
	headers['Referer'] = self._uri_prefix + '/users/index.htm'	
        r = self.session.post(uri, data = json.dumps(payload), headers = headers, verify=False)
	
	uri = self._uri_prefix + '/api/v1/account/user/' + str(u_id) + '/?_=' + str ( int ( time.time()* 1000))
	r = self.session.get(uri, headers = headers, verify=False)
	result = json.loads(r.text)
	if result['is_vip'] != True:
	    raise ValueError('Set user vip error')


