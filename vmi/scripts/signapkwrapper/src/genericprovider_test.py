#
# Generic apk SSO information provider test
# Author: Wayne Sun
# Date: 2014-05-05
#
#

import os
import shutil
import sys
import time

from util import *
from androidutil import AndroidAnalyzer
from genericprovider import GenericProvider

def test_find_edittext(generic_provider):
    log("\ntest_find_edittext")
    
    generic_provider.find_edittext()
    
    for control_name, control_data in generic_provider.edittext_control_data.items():
        log("%s => {id: %s, type: %s, base_class: %s, access: %s}" % 
            (control_name, 
             control_data["id"], 
             control_data["type"],
             control_data["base_class"],
             str(control_data["access"])))
        
def test_find_editext_in_same_activity(generic_provider):
    log("\ntest_find_editext_in_same_activity")
    
    generic_provider.find_edittext()
    
    edittext_control_data = generic_provider.edittext_control_data
    edittext_in_same_activity = generic_provider.find_controls_in_same_activity(edittext_control_data)
    
    for activity, control_names in edittext_in_same_activity.items():
        log("%s => %s" % (activity, str(control_names)))
        
def test_find_suspicious_login_activity(generic_provider):
    log("\ntest_find_suspicious_login_activity")
    
    generic_provider.find_edittext()
    
    edittext_control_data = generic_provider.edittext_control_data
    edittext_in_same_activity = generic_provider.find_controls_in_same_activity(edittext_control_data)
    
    suspicious_activities = generic_provider.find_suspicious_login_activity(edittext_in_same_activity)
    
    #for suspicious_activity in suspicious_activities:
    #    log("%s" % (str(suspicious_activity)))

def main():
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.dropbox.android-1")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\TestSSO-sample")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.trendmicro.virdroid-2")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.sap.mobi")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.sap.mcm.android")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.sap.mobile.travelexpense")
    android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.evernote.world-2")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.box.android-2")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.sap.mobile.hcm.hrapprovals-1")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.trendmicro.android_appstore")

    android_analyzer.parse_control()

    generic_provider = GenericProvider(android_analyzer)
    generic_provider.refresh_control_data()
    
    #test_find_edittext(generic_provider)
    test_find_editext_in_same_activity(generic_provider)
    test_find_suspicious_login_activity(generic_provider)
    
    
if __name__ == '__main__':
    main();
