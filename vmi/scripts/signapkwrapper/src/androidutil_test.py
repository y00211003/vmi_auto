#
# Android Utility Test
# Author: Wayne Sun
# Date: 2014-04-30
#
#

import os
import shutil
import sys
import time

from util import *
from androidutil import AndroidAnalyzer

def test_get_known_base_class(android_analyzer):
    log("\ntest_get_known_base_class")
    
    target_class = []
    target_class.append("com.dropbox.android.widget.EmailTextView")
    target_class.append("com.actionbarsherlock.internal.widget.CapitalizingButton")
    target_class.append("com.actionbarsherlock.internal.view.menu.ActionMenuItemView")
    target_class.append("com.dropbox.android.widget.OffscreenProgressBar")
    
    i = 0
    while i < len(target_class):
        super_class = android_analyzer.get_known_base_class(target_class[i])
        log("AndroidAnalyzer TEST\nFOUND %s : %s\n" % (target_class[i], super_class))
        i = i + 1
        
def test_is_class_inherit_edittext(android_analyzer):
    log("\ntest_is_class_inherit_edittext")
    
    target_class = []
    target_class.append("com.dropbox.android.widget.EmailTextView")
    target_class.append("com.actionbarsherlock.internal.widget.CapitalizingButton")
    target_class.append("com.actionbarsherlock.internal.view.menu.ActionMenuItemView")
    target_class.append("com.dropbox.android.widget.OffscreenProgressBar")
    
    i = 0
    while i < len(target_class):
        result = android_analyzer.is_class_inherit_edittext(target_class[i])
        if result == 0:
            log("AndroidAnalyzer TEST\n%s is NOT inherited from EditText\n" % (target_class[i]))
        else:
            log("AndroidAnalyzer TEST\n%s is based on %s and inherited from EditText\n" % (target_class[i], result))
        i = i + 1
        
def test_parse_control_id(android_analyzer):
    log("\ntest_parse_control_id")
    
    android_analyzer.parse_control_id()
    for control_name, control_id in android_analyzer.control_name_id_map.items():
        log("%s => %s" % (control_name, control_id))
        
def test_parse_control_type(android_analyzer):
    log("\ntest_parse_control_type")
    
    android_analyzer.parse_control_type()
    for control_name, control_data in android_analyzer.control_data.items():
        log("%s => {id: %s, type: %s}" % (control_name, control_data["id"], control_data["type"]))
    #log("%s" % (str(android_analyzer.control_data)))

def test_parse_control(android_analyzer):
    log("\ntest_parse_control")
    
    android_analyzer.parse_control()
    for control_name, control_data in android_analyzer.control_data.items():
        log("%s => {id: %s, type: %s, access: %s}" % 
            (control_name, 
             control_data["id"], 
             control_data["type"],
             str(control_data["access"])))

def main():
    android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\com.dropbox.android-1")
    #android_analyzer = AndroidAnalyzer("E:\\coding\\apk_wrapper_poc", "E:\\temp\\sso_working\\TestSSO-sample")
    
    test_get_known_base_class(android_analyzer)
    test_is_class_inherit_edittext(android_analyzer)
    #test_parse_control_id(android_analyzer)
    #test_parse_control_type(android_analyzer)
    test_parse_control(android_analyzer)
    
if __name__ == '__main__':
    main();
