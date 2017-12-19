#
# Auto wrapper for debug
# Author: Wayne Sun
# Date: 2014-05-05
#
#

import json
import os
import re
import shutil
import sys

from util import *
from androidutil import *

ON_CREATE_VIEW = ".method public onCreateView(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;"
ON_CREATE_VIEW_ORIG = ".method private onCreateViewOrig(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;"

ON_CREATE_PUBLIC = ".method public onCreate(Landroid/os/Bundle;)V"
ON_CREATE_PROTECTED = ".method protected onCreate(Landroid/os/Bundle;)V"
ON_CREATE_ORIG = ".method private onCreateOrig(Landroid/os/Bundle;)V"

FRAGMENT_CLASS_NAME = "$FRAGMENT_CLASS_NAME$"
ACTIVITY_CLASS_NAME = "$ACTIVITY_CLASS_NAME$"

STUB_SMALI_DIR = "stub_smali"

class VMIDebugWrapper(object):
    def __init__(self, root_path, decompile_dir):
        # VMIWrapper root path (hope to be full path)
        self.root_path = root_path
        # smali stub file directory (hope to be full path)
        self.stub_smali_dir = os.path.join(self.root_path, fix_win_path(STUB_SMALI_DIR));
        # current decompiled files directory (hope to be full path)
        self.decompile_dir = decompile_dir
        # AndroidAnalyzer instance
        self.android_analyzer = AndroidAnalyzer(root_path, decompile_dir)
        # current package name
        self.package_name = ""
        # read sso info from SSO information json file
        self.sso_info = {}
        # wrapper infor of current package
        self.wrapper_info = {}
    
    # Insert code for Activity
    def edit_activity(self, activity_class_name, smali_content):
        log("Edit Activity...")
        
        if (smali_content.find(ON_CREATE_PUBLIC) == -1) and (
            smali_content.find(ON_CREATE_PROTECTED) == -1):
            return smali_content
        
        # Maybe public or protected
        smali_content = smali_content.replace(ON_CREATE_PUBLIC, ON_CREATE_ORIG)
        smali_content = smali_content.replace(ON_CREATE_PROTECTED, ON_CREATE_ORIG)
        
        fragment_path = os.path.join(self.stub_smali_dir, "activity.debug.smali");
        fragment_part = open(fragment_path, 'rb').read()
        full_class_name = "L%s;" % (activity_class_name)
        fragment_part = fragment_part.replace(ACTIVITY_CLASS_NAME, full_class_name)
        
        smali_content = "%s \n\n %s" % (smali_content, fragment_part)
        
        return smali_content
        
    # Insert code for Fragment
    def edit_fragment(self, activity_class_name, smali_content):
        log("Edit Fragment...")
        
        if smali_content.find(ON_CREATE_VIEW) == -1:
            return smali_content
        
        smali_content = smali_content.replace(ON_CREATE_VIEW, ON_CREATE_VIEW_ORIG)
        
        fragment_path = os.path.join(self.stub_smali_dir, "fragment.debug.smali");
        fragment_part = open(fragment_path, 'rb').read()
        full_class_name = "L%s;" % (activity_class_name)
        fragment_part = fragment_part.replace(FRAGMENT_CLASS_NAME, full_class_name)
        
        smali_content = "%s \n\n %s" % (smali_content, fragment_part)
        
        return smali_content
            
    def search_activity(self, smali_file):
        #log(smali_file)
        write_back = 0
        
        smali_content = open(smali_file, 'rb').read()
        class_name = self.android_analyzer.get_class_from_smali_content(smali_content)
        if (not class_name in KNOWN_ACTIVITY_INHERIT) and (
            not self.android_analyzer.is_class_inherit_activity(class_name) == 0):
            log("FOUND App Activity: %s" % (class_name))
            smali_content = self.edit_activity(class_name, 
                               smali_content)
            write_back = 1
        elif (not class_name in KNOWN_FRAGMENT_INHERIT) and (
            not self.android_analyzer.is_class_inherit_fragment(class_name) == 0):
            log("FOUND App Fragment: %s" % (class_name))
            smali_content = self.edit_fragment(class_name, 
                               smali_content)
            write_back = 1
            
        if write_back:
            # Write back
            smali_file = open(smali_file, 'wb')
            smali_file.write(smali_content)
            smali_file.close()
    
    def do_debugwrapper(self):
        log("Do debug wrapper...")
        
        log("Find target Activity/Fragment..")
        self.package_name = self.android_analyzer.get_package_name()
        log("Package name: %s" % (self.package_name))
        
        log("\nAdd debug code...")
        self.android_analyzer.walk_java_package(self.decompile_dir, self.search_activity)
        #self.add_code()
        
        log("\nDONE debug wrapper...\n")
