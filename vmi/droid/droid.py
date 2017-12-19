'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Web Related Actions
'''

from vmi.server.server import Server
from vmi.server.user import User

from vmi.configure import Configure

import inspect
import datetime
from time import sleep

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

from functools import partial, wraps
from vmi.utility.logger import Logger
import os , sys, time, commands

log = Logger(__name__)

SCREEN_WIDTH = 480
SCREEN_HEIGHT= 800
PADDING = 10

def exception_hook(func):
    @wraps(func)
    def wrapper(*args):
        try:
            return func(*args)
        except Exception , e:
            args[0].take_screenshot()
            args[0].collect_device_log()
            raise e
    return wrapper


class Android( object ):

    def __init__(self):
        super(Android, self).__init__()
        self.config = Configure.Instance()
        config = self.config

        self.desired_caps = {'platformName' : 'Android', 'platformVersion' : '4.4',
                             'deviceName' :'4.4H',
                             'app' : config.get('DroidAutoClient', 'android_app'),
                             'newCommandTimeout': 600,
                             'appWaitActivity' : 'com.trendmicro.virdroid.ui.EulaActivity', 'sessionOverride': 'True',
                             'noSign': 'True' #add by gannicus
        }



class Droid(object):

    def __init__(self):
        #super(Droid, self).__init__()
        self.config = Configure.Instance()

        config = self.config

        self.remote_hub = 'http://' + config.get('DroidAutoClient','ip') +\
                          ':' + config.get('DroidAutoClient', 'port') + \
                          '/wd/hub'

        self.driver = None

    def __del__(self):

        if None != self.driver:
            self.driver.quit()
            self.driver = None

    def _invoke_device(self, device):
        if self.driver == None:
            self.driver = webdriver.Remote(self.remote_hub, device.desired_caps)
        else:
            pass

    def _click_button_at_index (self,  index ):

        buttons = self.driver.find_elements_by_class_name('android.widget.Button')
        buttons[index].click()
        sleep(2)


    def check_is_in_activity( self, activity_name):
        if self.driver == None:
            raise ValueError ('No driver')

        current_activity = self.driver.current_activity

        if current_activity.find(activity_name) != -1:
            return True
        else:
            return False

    def _wait_for_activity_with_timeout(self, activity_name, secs , interval = 5):

        s = 0

        if self.check_is_in_activity(activity_name): return

        sleep(interval)

        while not self.check_is_in_activity(activity_name) :
            s+=5
            if s > secs : raise ValueError('Failed to wait activity ' +  activity_name)
            sleep(interval)


    def click_remember_password(self, device ):

        self._invoke_device(device)
        self._wait_for_activity_with_timeout('LoginAccountActivity', 10)

        checkboxs = self.driver.find_elements_by_class_name('android.widget.CheckBox')
        try:
            checkboxs[0].click()
        except Exception as e:
            raise ValueError ('Fail to set remember password')

#updated by richard
    def _input_edit_text_at_index_with_content(self, index, content):

        if self.driver == None:
            raise ValueError ('No driver')

        text_fields = self.driver.find_elements_by_class_name('android.widget.EditText')
        text_fields[index].click()
        sleep(1)   #waiting for 1 second is important, otherwise 'select all' doesn't work. However, it perform this from my view
        self.driver.press_keycode(29,28672)   # 29 is the keycode of 'a', 28672 is the keycode of META_CTRL_MASK
        self.driver.press_keycode(112)   # 112 is the keycode of FORWARD_DEL, of course you can also use 67

        text_fields[index].send_keys(content)


    def input_server_address_and_get_config(self, ip ):

        self._wait_for_activity_with_timeout('LoginServerActivity', 10)
        self._input_edit_text_at_index_with_content(0, ip)
        self._click_button_at_index(0)


    def input_user_name (self, username):

        self._wait_for_activity_with_timeout('LoginAccountActivity', 10)
        self._input_edit_text_at_index_with_content(0, username)



    def input_password_and_login(self, password):

        self._wait_for_activity_with_timeout('LoginAccountActivity', 10)
        self._input_edit_text_at_index_with_content(1, password)

        self._click_button_at_index(0)


    def unlock_unia_with_password(self, password):
        self._wait_for_activity_with_timeout('PasswordUnlockActivity', 10)
        self._input_edit_text_at_index_with_content(0, password)
        self.press_enter_key()

    def unlock_unia_with_pin (self, pin):
        self._wait_for_activity_with_timeout('PasswordUnlockActivity', 10)
        self._input_edit_text_at_index_with_content(0, pin)
        self.press_enter_key()


    def _perform_press_keycode(self, keycode):
        if self.driver == None: raise ValueError ('No driver')
        self.driver.press_keycode(keycode)

    def _perform_long_press_keycode(self, keycode):
        if self.driver == None: raise ValueError('No driver')
        self.driver.long_press_keycode(keycode)

    def press_enter_key (self):
        self._perform_press_keycode(66)

    def press_menu_key (self):
        self._perform_press_keycode(82)

    def press_home_key (self):
        self._perform_press_keycode(3)

    def press_back_key(self):
        self._perform_press_keycode(4)

    def perform_click(self, x, y):
        if self.driver == None : raise ValueError('No driver')
        self.driver.tap([(x,y)])

    def launch_app (self):
        if self.driver == None: raise ValueError('No driver')
        self.driver.launch_app()

    def close_app(self):
        self.driver.close_app()

    # navigate from hybrid to local launcher

    def _perform_swipe(self, x1 , y1 , x2, y2 , high_quality_mode):
        if high_quality_mode:
            self.driver.swipe(x1, y1, x2, y2, 50)
        else:
            self.driver.swipe(x1/2, y1/2, x2/2, y2, 50)

    def navigate_to_launcher(self):

        if self.check_is_in_activity('HybridActivity'): self.press_back_key()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        for counter in range(10):
            try:
                e1 = self.driver.find_element_by_id("view_prepare")
                log.debug("Wait Connect")
                sleep(3)
            except Exception,e:
                log.debug('No wait')
                break

    def superlab_navigate_to_launcher(self):

        if self.check_is_in_activity('HybridActivity'): 
            self.press_back_key()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        for counter in range(30):
            try:
                e1 = self.driver.find_element_by_id("view_prepare")
                log.debug("Wait Connect")
                sleep(1)
            except Exception,e:
                log.debug('No wait')
                break
        #cmd_end = 'date|awk \'{print $4}\''
        #current_time = commands.getoutput(cmd_end)
        #cmd_record = 'echo %s > /root/vmi/droidLoginTime_end.txt' % (str(current_time))
        #os.system(cmd_record)
        time_end = datetime.datetime.now()
        return str(time_end)

    def superlab_countLoginTime(self,login_start,login_end):
        format = '%Y-%m-%d %H:%M:%S.%f'
        time_start = datetime.datetime.strptime(str(login_start), format)
        time_end = datetime.datetime.strptime(str(login_end), format)

        startTime = time.mktime(time_start.timetuple()) * 1000 + time_start.microsecond / 1000
        endTime = time.mktime(time_end.timetuple()) * 1000 + time_end.microsecond / 1000
        print 'startTime',startTime
        print 'endTime',endTime
        login_time = endTime - startTime
        print 'login_time',login_time

        cmd_record = 'echo -e %s >> /root/vmi/droidLoginTime.txt' % (str(login_time))
        os.system(cmd_record)
        return str(login_time)


#######################################################
#added by richard
    def eula_accept(self):

        self._wait_for_activity_with_timeout('EulaActivity', 10)

        self._click_button_at_index(0)

    def eula_reject(self):

        self._wait_for_activity_with_timeout('EulaActivity', 10)

        self._click_button_at_index(1)

    def navigate_to_Sandboxlauncher(self):

        self._wait_for_activity_with_timeout('SandboxLauncherActivity', 10)

    def secure_warning_back(self):

        buttons = self.driver.find_elements_by_class_name('android.widget.Button')
        try:
            buttons[0].click()
        except Exception as e:
            raise ValueError ('Fail to back')

    def secure_warning_remeberCheck(self):

        CheckBoxs = self.driver.find_elements_by_class_name('android.widget.CheckBox')
        try:
            CheckBoxs[0].click()
        except Exception as e:
            raise ValueError ('Fail to back')

    def secure_warning_continue(self):
        self.driver.find_elements_by_class_name('android.widget.Button')[1].click()
'''        buttons = self.driver.find_elements_by_class_name('android.widget.Button')
        try:
            buttons[1].click()
        except Exception as e:
            raise ValueError ('Fail to continue')
'''

class DroidAPI(Droid):

    def __init__(self):
        super(DroidAPI, self).__init__()


    #Call before anyother API
    @exception_hook
    def invoke_device(self, device):

        self._invoke_device(device)

    @exception_hook
    def reinvoke_device(self, device):
        if not self.driver == None:
            self.driver.quit()
            self.driver = None
        self._invoke_device(device)

    @exception_hook
    def login_server_with_remember_password(self, server, user):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_continue()
        self.input_user_name(user.username)
        self.click_remember_password()
        self.input_password_and_login(user.password)

    @exception_hook
    def login_server_without_remember_password(self, server, user):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_continue()
        self.input_user_name(user.username)
        self.input_password_and_login(user.password)

    @exception_hook
    def login_server_without_input_server_address(self, server, user):
        self.input_user_name(user.username)
        self.input_password_and_login(user.password)

    @exception_hook
    def superlab_login_server_without_input_server_address(self, server, user):
        self.input_user_name(user.username)
        self.input_password_and_login(user.password)

#        cmd_start = 'date|awk \'{print $4}\''
#        current_time = commands.getoutput(cmd_start)
#        cmd_record = 'echo %s > /root/vmi/droidLoginTime.txt' % (str(current_time))
#        os.system(cmd_record)
        time_start = datetime.datetime.now()
        return str(time_start)  

    #add by gannicus
    @exception_hook
    def login_server_name_psw_without_remember_password(self, server, username, password):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_continue()
        self.input_user_name(username)
        self.input_password_and_login(password)
        
    #add by gannicus
    @exception_hook
    def login_server_name_psw_without_input_server_address(self, server, username, password):
        self.input_user_name(username)
        self.input_password_and_login(password)

    @exception_hook
    def set_unia_lock_screen_none( self , user ):
        self._wait_for_activity_with_timeout('ChooseLockGeneric', 10)
        self._click_button_at_index(0)

        self._wait_for_activity_with_timeout('PagedLauncher', 10)

    @exception_hook
    def set_unia_lock_screen_pin(self, user):

        self._wait_for_activity_with_timeout('ChooseLockGeneric', 10)
        self._click_button_at_index(2)

        self._wait_for_activity_with_timeout('ChooseLockPassword', 10)

        if user.screen_lock_type == 3:
            self._input_edit_text_at_index_with_content(0,user.screen_lock_value)
            self._click_button_at_index(1)
            self._input_edit_text_at_index_with_content(0,user.screen_lock_value)
            self._click_button_at_index(1)

        else:
            raise ValueError('invalid user setting')

        self._wait_for_activity_with_timeout('PagedLauncher', 10)

    @exception_hook
    def set_unia_lock_screen_password(self, user):

        self._wait_for_activity_with_timeout('ChooseLockGeneric', 10)
        self._click_button_at_index(3)

        self._wait_for_activity_with_timeout('ChooseLockPassword', 10)

        if user.screen_lock_type == 4:
            self._input_edit_text_at_index_with_content(0,user.screen_lock_value)
            self._click_button_at_index(1)
            self._input_edit_text_at_index_with_content(0,user.screen_lock_value)
            self._click_button_at_index(1)

        else:
            raise ValueError('invalid user setting')

        self._wait_for_activity_with_timeout('PagedLauncher', 10)

    @exception_hook
    def signout_from_launcher(self):
        sleep (2)
        if self.check_is_in_activity('HybridActivity'):
            self.navigate_to_launcher()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        self.press_menu_key()
        self.driver.find_elements_by_class_name('android.widget.Button')[0].click()
        self._click_button_at_index(1)


    def confirm_spn(self, choice= False):
        #self._wait_for_activity_with_timeout('LoginServerActivity', 150)
        pass

    @exception_hook
    def expected_current_activity(self, activity_name):

        self._wait_for_activity_with_timeout(activity_name, 10)

    @exception_hook
    def launch_app_from_unia(self, app_name):
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
	e1 = self.driver.find_elements_by_name('Got It')
	if len(e1) != 0:
	    e1[0].click()
	log.debug(e1)
        self.driver.find_elements_by_name(app_name)[0].click()
        #self._wait_for_activity_with_timeout('HybridActivity',10)
	self._wait_for_activity_with_timeout('NetworkIndicatorGuideActivity',10)

    #add by gannicus
    @exception_hook
    def check_app_exist(self, app_name):
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        self.driver.find_elements_by_name(app_name)[0] 

    #should not add exception hook
    def take_screenshot(self):
        sleep(3)
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        work_dir = os.environ['work_dir']
        file_path = os.path.join(work_dir, "%s.png"%name)

        self.driver.get_screenshot_as_file(file_path)
        self.driver.save_screenshot(file_path)

    #should not add exception hook
    def collect_device_log(self):
        name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        work_dir = os.environ['work_dir']
        file_path = os.path.join(work_dir, "%s.txt"%name)


        logs = self.driver.get_log('logcat')

        log_file = open(file_path , 'w')

        for line in logs :
            for k,v in line.items():
                log_file.write('%r|' % unicode(v))
            log_file.write('\n')
        log_file.close()

    @exception_hook
    def switch_to_background_for_secs(self, sec):
        self.driver.background_app(sec)

    @exception_hook
    def lock_device(self):
        self.driver.lock(10)

    @exception_hook
    def open_notification(self):
        self.driver.open_notifications()

    #add by gannicus
    @exception_hook
    def check_retry_in_seconds(self):
        el = self.driver.find_element_by_id("com.trendmicro.virdroid5:id/tv_error_message")
        log.debug(el.text)
        if not "Please retry in" in el.text:
            raise ValueError('Show retry in seconds error') 

############################################
#added by richard
    @exception_hook
    def eula_action(self, option):
        eula_option = str(option)        
        if eula_option == 'accept':
            self.eula_accept()
        else:
            self.eula_reject()

    @exception_hook
    def check_sandboxapp_exist(self, app_name):
        self._wait_for_activity_with_timeout('SandboxLauncherActivity', 10)
        self.driver.find_elements_by_name(app_name)[0]

    @exception_hook
    def login_server_without_input_server_address_setunialockscreen_none(self, server, user):
        self.input_user_name(user.username)
        self.input_password_and_login(user.password)
        self._wait_for_activity_with_timeout('ChooseLockGeneric', 10)
        self._click_button_at_index(0)

        self._wait_for_activity_with_timeout('PagedLauncher', 10)

    @exception_hook
    def signout_from_sandboxlauncher(self):
        if self.check_is_in_activity('SandboxLauncherActivity'):
            self.navigate_to_Sandboxlauncher()
        self.press_menu_key()
        self.driver.find_elements_by_class_name('android.widget.Button')[0].click()
        self._click_button_at_index(1)

    @exception_hook
    def login_server_securewarning_remember(self, server, user):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_remeberCheck()
        self.secure_warning_continue()
        self.input_user_name(user.username)
        self.input_password_and_login(user.password)

    @exception_hook
    def login_server_securewarning_back(self, server, user):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_remeberCheck()
        self.secure_warning_back()

    @exception_hook
    def bandwidth_test(self):
        if self.check_is_in_activity('HybridActivity'):
            self.navigate_to_launcher()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        self.press_menu_key()
        self.driver.find_elements_by_class_name('android.widget.Button')[1].click()
        sleep (3)
        self.press_menu_key()
 
    @exception_hook
    def virtualHome_command(self):
        if self.check_is_in_activity('HybridActivity'):
            self.navigate_to_launcher()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        self.press_menu_key()
        self.driver.find_elements_by_class_name('android.widget.CheckBox')[0].click()
        self.press_menu_key()

    @exception_hook
    def networkIndicator_command(self):
        if self.check_is_in_activity('HybridActivity'):
            self.navigate_to_launcher()
        self._wait_for_activity_with_timeout('PagedLauncher', 10)
        self.press_menu_key()
        self.driver.find_elements_by_class_name('android.widget.CheckBox')[1].click()
        self.press_menu_key()

#versionView
    @exception_hook
    def protocolChange_command(self):
        sleep (5)
#        if self._wait_for_activity_with_timeout('LoginServerActivity', 10):
#            self.check_is_in_activity('LoginServerActivity')
#        else:
#            self._wait_for_activity_with_timeout('LoginAccountActivity', 10)
#            self.check_is_in_activity('LoginAccountActivity')
        try:
            for i in range (5) :
                self.driver.tap([(500,1760)],100)
                sleep(0.05)
            sleep (2)
        except Exception as e:
            raise ValueError ('Fail to click')

    @exception_hook
    def log_collect_command(self):
        sleep (5)
#        if self._wait_for_activity_with_timeout('LoginServerActivity', 10):
#            self.check_is_in_activity('LoginServerActivity')
#        else:
#            self._wait_for_activity_with_timeout('LoginAccountActivity', 10)
#            self.check_is_in_activity('LoginAccountActivity')
        try:
            self.driver.tap([(500,1760)],1100)
            sleep (2)
        except Exception as e:
            raise ValueError ('Fail to click')

    @exception_hook
    def login_server_notInputUser(self, server):
        self.input_server_address_and_get_config(server.portal_ip)
        sleep (3)
        self.secure_warning_remeberCheck()
        self.secure_warning_continue()


