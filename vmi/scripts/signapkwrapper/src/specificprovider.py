#
# Manual specific SSO information provider
# Author: Wayne Sun
# Date: 2015-01-14
#
#

import os
import shutil
import sys
import time

from util import *
from androidutil import *
from providercommon import *

global KEY_USERNAME
global KEY_USERNAME_WITHOUT_DOMAIN
global KEY_USERNAME_EMAIL
global KEY_PASSWORD
global KEY_EXCHANGE_SERVER
global KEY_OTHER_SERVER
global KEY_OTHER_SERVER_PORT

global KEY_VALUE_MAP

global SPECIAL_KEY
global SPECIAL_VALUE

SSO_INFO_JSON = "data/sso_info.json"

class SpecificProvider(object):
    def __init__(self, root_path, android_analyzer):
        self.root_path = root_path
        self.sso_info_json_file = os.path.join(self.root_path, fix_win_path(SSO_INFO_JSON))
        self.android_analyzer = android_analyzer
        
        self.wrapper_activities = []
        self.special_app_data = {}
        
        # Let's load known information from file.
        log("\nSpecificProvider load information...")
        
        if not os.path.exists(self.sso_info_json_file):
            log("CANNOT find SSO json file: %s" % (self.sso_info_json_file))
            return
        
        sso_info_json_raw = open(self.sso_info_json_file, 'rb').read()
        sso_info_data = {}
        
        try:
            sso_info_data = json.loads(sso_info_json_raw)
            #log(str(sso_activity_data))
        except:
            log("json.loads file: %s, failed!" % (self.sso_info_json_file))
        
        sso_activity_data = sso_info_data["activity_data"]
        
        activity_count = len(sso_activity_data)
        i = 0
        while i < activity_count:
            activity_itr = sso_activity_data[i]
            
            target_activity = {}
            target_activity["class_name"] = str(activity_itr["class_name"])
            target_activity["text_views"] = []
            
            text_view_count = len(activity_itr["text_views"])
            j = 0
            while j < text_view_count:
                text_view_itr = activity_itr["text_views"][j]
                
                text_view = {}
                text_view["control_id"] = str(text_view_itr["control_id"])
                text_view["sso_key"] = KEY_VALUE_MAP[str(text_view_itr["sso_key"])]
                
                target_activity["text_views"].append(text_view)
                
                j += 1
            
            #log(str(target_activity))
            self.wrapper_activities.append(target_activity)
        
            i += 1
            
        sso_app_data = sso_info_data["app_data"]
        app_count = len(sso_app_data)
        i = 0
        while i < app_count:
            app_itr = sso_app_data[i]
            
            app = {}
            app["package_name"] = str(app_itr["package_name"])
            app["special_values"] = []
            
            special_value_count = len(app_itr["special_values"])
            j = 0
            while j < special_value_count:
                special_value_itr = app_itr["special_values"][j]
                
                special_value = {}
                special_value[SPECIAL_KEY] = str(special_value_itr["key"])
                special_value[SPECIAL_VALUE] = str(special_value_itr["value"])
                
                app["special_values"].append(special_value)
                
                j += 1
                
            #log(str(app))
            self.special_app_data[app["package_name"]] = app["special_values"]
            
            i += 1
                
        
    def find_specific_login_activity(self, local_activity_control_map):
        
        specific_login_activities = []
        
        for wrapper_activity in self.wrapper_activities:
            activity_class_name = wrapper_activity["class_name"]
            if activity_class_name in local_activity_control_map:
                control_names = local_activity_control_map[activity_class_name]
                
                check_text_views = True
                
                for text_view in wrapper_activity["text_views"]:
                    if not text_view["control_id"] in control_names:
                        check_text_views = False
                        break
                
                if check_text_views:
                    log("SpecificProvider FOUND %s" % (activity_class_name))
                    
                    activity = activity_class_name
                    
                    activity_data = {}
                    activity_data["activity"] = activity
                        
                    if self.android_analyzer.is_class_inherit_activity(activity):
                        activity_data["activity_type"] = ACTIVITY_TYPE_ACTIVITY
                    elif self.android_analyzer.is_class_inherit_fragment(activity):
                        activity_data["activity_type"] = ACTIVITY_TYPE_FRAGMENT
                    else:
                        # We don't know how to manipulate other type
                        log("Unknown Activity type: %s" % (activity))
                        continue
                     
                    for text_view in wrapper_activity["text_views"]:
                        activity_data[text_view["sso_key"]] = text_view["control_id"]
                    
                    specific_login_activities.append(activity_data)
            
        return specific_login_activities
    
