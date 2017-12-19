#
# Generic apk SSO information provider
# Author: Wayne Sun
# Date: 2014-05-05
#
#

import os
import shutil
import sys
import time

from util import *
from androidutil import *
from providercommon import *

SUSPICIOUS_LOGIN_ACTIVITY_KEYWORDS = ["login", "logon", "signin", "connect", "auth", "credent", "cert", "config", "main"]
SUSPICIOUS_LOGIN_USERNAME_KEYWORDS = ["loginname", "user", "usr", "email"]
SUSPICIOUS_LOGIN_PASSWORD_KEYWORDS = ["password", "pswd", "pwd", "passward"] # passward is just for TDH

class GenericProvider(object):
    def __init__(self, android_analyzer):
        self.android_analyzer = android_analyzer
        self.control_data = {}
        self.edittext_control_data = {}
        
    # Make sure AndroidAnalyzer.parse_control() is called
    def refresh_control_data(self):
        self.control_data = self.android_analyzer.get_control_data()
        
    # Find controls in the same Activity/Fragment
    # Return activity_control_map[activity] => [control_name1, control_name2]
    def find_controls_in_same_activity(self, local_control_data):
        log("\nFind controls in the same activity...")
        
        activity_control_map = {}
        for control_name, control_data in local_control_data.items():
            # control_data["access"] is an array
            activities = control_data["access"]
            for activity in activities:
                if not activity in activity_control_map:
                    # empty array
                    activity_control_map[activity] = []
                
                # stringify
                activity_control_map[activity].append(str(control_name))
                
        return activity_control_map
    
    # Find EditText data from control data
    # EditText is the control we can manipulate
    def find_edittext(self):
        log("\nFind EditText controls...")
        
        if len(self.control_data) == 0:
            # Call refresh_control_data first
            log("No control data here!")
            return
    
        for control_name, control_data in self.control_data.items():
            control_type = control_data["type"]
            #log("%s => %s" % (control_name, control_type))
            inherit_edittext = self.android_analyzer.is_class_inherit_edittext(control_type)
            if not inherit_edittext == 0:
                # We found an EditText
                self.edittext_control_data[control_name] = control_data
                # Add base_class field
                self.edittext_control_data[control_name]["base_class"] = inherit_edittext
    
    # Find suspicious login Activity/Fragment
    def find_suspicious_login_activity(self, local_activity_control_map):
        log("\nFind suspicious login activities...")
        
        global KEY_USERNAME
        global KEY_PASSWORD
        
        suspicious_activities = []
        
        for activity, control_names in local_activity_control_map.items():
            found_username = 0
            username_control = ""
            found_password = 0
            password_control = ""
            
            for control_name in control_names:
                # lower
                control_name_mangling = control_name.lower()
                # remove "_"
                control_name_mangling = control_name_mangling.replace("_", "")
                
                if find_strings_in_string(SUSPICIOUS_LOGIN_USERNAME_KEYWORDS, 
                                          control_name_mangling):
                    found_username = 1
                    username_control = control_name
                if find_strings_in_string(SUSPICIOUS_LOGIN_PASSWORD_KEYWORDS, 
                                          control_name_mangling):
                    found_password = 1
                    password_control = control_name
                    
            if found_username:
                #lower
                activity_mangling = activity.lower()
                if find_strings_in_string(SUSPICIOUS_LOGIN_ACTIVITY_KEYWORDS, 
                                          activity_mangling):
                    suspicious_activity = {}
                    suspicious_activity["activity"] = activity
                    
                    if self.android_analyzer.is_class_inherit_activity(activity):
                        suspicious_activity["activity_type"] = ACTIVITY_TYPE_ACTIVITY
                    elif self.android_analyzer.is_class_inherit_fragment(activity):
                        suspicious_activity["activity_type"] = ACTIVITY_TYPE_FRAGMENT
                    else:
                        # We don't know how to manipulate other type
                        log("Unknown Activity type: %s" % (activity))
                        continue
                    
                    suspicious_activity[KEY_USERNAME] = username_control
                    
                    # Maybe no password
                    if found_password:
                        suspicious_activity[KEY_PASSWORD] = password_control
                        
                    log("GenericProvider FOUND suspicious login Activity/Fragment:\n%s\nControls in Activity/Fragment:\n%s" % 
                        (str(suspicious_activity), control_names))
                    suspicious_activities.append(suspicious_activity)
                    
        return suspicious_activities
    
