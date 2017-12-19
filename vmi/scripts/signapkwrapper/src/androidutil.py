#
# Android Utility
# Author: Wayne Sun
# Date: 2014-04-29
#
#

import os
import re

from xml.dom import minidom

from util import *

ACTIVITY_TYPE_ACTIVITY = "Activity"
ACTIVITY_TYPE_FRAGMENT = "Fragment"

RID = "R$id"
PUBLIC_XML = "xml"

PUBLIC_XML_PATH = "res/values/public.xml"
STRINGS_XML_PATH = "res/values/strings.xml"

KNOWN_EDITTEXT_INHERIT = ["android/widget/EditText", 
                           "android/widget/AutoCompleteTextView", 
                           "android/widget/MultiAutoCompleteTextView", 
                           "android/inputmethodservice/ExtractEditText"]
KNOWN_ACTIVITY_INHERIT = ["android/app/Activity", 
                           "android/accounts/AccountAuthenticatorActivity", 
                           "android/app/ActivityGroup", 
                           "android/app/AliasActivity",
                           "android/app/ExpandableListActivity",
                           "android/support/v4/app/FragmentActivity",
                           "android/app/ListActivity",
                           "android/app/NativeActivity",
                           "android/app/TabActivity",
                           "android/preference/PreferenceActivity",
                           "android/app/LauncherActivity",
                           "android/support/v7/app/ActionBarActivity"]
KNOWN_FRAGMENT_INHERIT = ["android/app/Fragment", 
                           "android/app/DialogFragment",
                           "android/app/ListFragment",
                           "android/preference/PreferenceFragment",
                           #"android.webkit.WebViewFragment",
                           "android/support/v4/app/Fragment", 
                           "android/support/v4/app/DialogFragment", 
                           "android/support/v4/app/ListFragment", 
                           "android/support/v7/app/MediaRouteDiscoveryFragment",
                           "android/support/v7/app/MediaRouteControllerDialogFragment",
                           "android/support/v7/app/MediaRouteChooserDialogFragment"]

class AndroidAnalyzer(object):
    def __init__(self, root_path, decompile_dir):
        # VMIWrapper root path (hope to be full path)
        self.root_path = root_path
        # current decompiled files directory (hope to be full path)
        self.decompile_dir = decompile_dir
        # current decompiled smali directory
        self.decompile_smali_dir = os.path.join(self.decompile_dir, "smali")
        
        # direct class inherit cache
        self.class_inherit_cache = {}
        # current package name
        self.package_name = ""
        # R$id or public.xml path
        self.R_id_path = ""
        self.public_xml_path = ""
        # known control name and id map
        self.control_name_id_map = {}
        # known control data
        # {"name" => {"id", "type"}}
        self.control_data = {}
    
    
    def get_class_from_smali_content(self, smali_content):   
        # find class full name
        class_name = re.search(r'.class(.*) L(.+);', smali_content)
        if class_name:
            class_name = class_name.group(2)
            return class_name
        else:
            return ""
        
    def get_super_class_from_smali_content(self, smali_content):
        super_class_name = re.search(r'.super L(.+);', smali_content)
        if super_class_name:
            super_class_name = super_class_name.group(1)
            super_class_name = super_class_name.strip()
            return super_class_name
        else:
            return ""
        
    # Find known base class of give class
    def get_known_base_class(self, class_name):
        class_name = class_name.replace(".", "/")
        #log("Ask: %s" % (class_name));
        if (class_name in KNOWN_EDITTEXT_INHERIT) or (
            class_name in KNOWN_ACTIVITY_INHERIT) or (
            class_name in KNOWN_FRAGMENT_INHERIT):
            #log("Found known: %s " % (class_name))
            return class_name
        
        if class_name in self.class_inherit_cache:
            #log("Found %s : %s" % (class_name, self.class_inherit_cache[class_name]))
            return self.get_known_base_class(self.class_inherit_cache[class_name])
        
        class_smali = fix_win_path(class_name)
        class_smali = "%s.smali" % (class_smali)
        class_smali_file = os.path.join(self.decompile_smali_dir, class_smali)
        if os.path.exists(class_smali_file):
            # try to read super class from class file
            class_file_content = open(class_smali_file, 'rb').read()
            super_class_name = self.get_super_class_from_smali_content(class_file_content)
            if not super_class_name == "":
                self.class_inherit_cache[class_name] = super_class_name
                #log("Found %s : %s" % (class_name, super_class_name))
                return self.get_known_base_class(super_class_name)
        
        # nothing more found
        return class_name
    
    # Detect if class is inherited from EditText
    def is_class_inherit_edittext(self, class_name):
        if class_name == "EditText":
            return "android/widget/EditText"
        if class_name == "AutoCompleteTextView":
            return "android/widget/AutoCompleteTextView"
        if class_name == "MultiAutoCompleteTextView":
            return "android/widget/MultiAutoCompleteTextView"
        if class_name == "ExtractEditText":
            return "android/inputmethodservice/ExtractEditText"
        
        super_class = self.get_known_base_class(class_name)
        if super_class in KNOWN_EDITTEXT_INHERIT:
            return super_class
        else:
            return 0
        
    # Detect if class is inherited from Activity
    def is_class_inherit_activity(self, class_name):
        super_class = self.get_known_base_class(class_name)
        if super_class in KNOWN_ACTIVITY_INHERIT:
            return super_class
        else:
            return 0
        
    # Detect if class is inherited from Fragment
    def is_class_inherit_fragment(self, class_name):
        super_class = self.get_known_base_class(class_name)
        if super_class in KNOWN_FRAGMENT_INHERIT:
            return super_class
        else:
            return 0
    
    # andriod:id is "@id/xxx", return xxx
    def get_android_id_name(self, full_android_id):
        if full_android_id.startswith("@id/"):
            return full_android_id[4:]
    
    def read_android_manifest(self):
        AndroidManifest_path = os.path.join(self.decompile_dir, "AndroidManifest.xml")
        if not os.path.exists(AndroidManifest_path):
            return ""
        
        manifest_content = open(AndroidManifest_path, 'rb').read()
        return manifest_content
    
    def write_android_manifest(self, manifest_content):
        AndroidManifest_path = os.path.join(self.decompile_dir, "AndroidManifest.xml")
        if not os.path.exists(AndroidManifest_path):
            return
        
        manifest_file = open(AndroidManifest_path, 'wb')
        manifest_file.write(manifest_content)
        manifest_file.close()
    
    # Get package name from decompiled AndroidManifest.xml
    def get_package_name(self):   
        manifest_content = self.read_android_manifest()
        package_name = re.search(r'package=\"([^"]+)\"', manifest_content)
        if package_name:
            package_name = package_name.group(1)
            package_name = package_name.strip()
        else:
            package_name = ""
        
        self.package_name = package_name
        
        return package_name
    
    def has_user_permission(self, permission):
        manifest_content = self.read_android_manifest()
        permission_reg = '<uses-permission android:name=\"%s\" \/>' % (permission.replace(".", "\."))
        permission_found = re.search(permission_reg, manifest_content)
        if permission_found:
            return True
        else:
            return False
    
    def add_user_permission(self, permission):
        permission_string = "<uses-permission android:name=\"%s\" />" % (permission)
        
        manifest_content = self.read_android_manifest()
        
        manifest_content = manifest_content.replace("<application ", 
                                                    "%s\n<application " % (permission_string))
        
        self.write_android_manifest(manifest_content)
    
    # Find name->id is in R$id or public.xml
    def get_id_file(self):        
        if not self.R_id_path == "":
            return RID
        
        if not self.public_xml_path == "":
            return PUBLIC_XML
        
        # try to find R$id first
        package_path = self.package_name.replace(".", "/")
        package_path = fix_win_path(package_path)
        R_id_path_local = os.path.join(self.decompile_smali_dir, package_path)
        R_id_path_local = os.path.join(R_id_path_local, "R$id.smali")
        if os.path.exists(R_id_path_local):
            log("Found R$id:\n%s" % (R_id_path_local))
            self.R_id_path = R_id_path_local
            return RID
            
        # try to find public.xml
        relative_xml_path = fix_win_path(PUBLIC_XML_PATH)
        public_xml_path_local = os.path.join(self.decompile_dir, relative_xml_path)
        if os.path.exists(public_xml_path_local):
            log("Found public.xml:\n%s" % (public_xml_path_local))
            self.public_xml_path = public_xml_path_local
            return PUBLIC_XML
            
        return ""
    
    def walk_xml_node(self, xml_node, xml_proc):
        if not xml_node.nodeType == xml_node.ELEMENT_NODE:
            return
        
        xml_proc(xml_node)
        
        # has child nodes
        if xml_node.childNodes:
            for child_node in xml_node.childNodes:
                self.walk_xml_node(child_node, xml_proc)
    
    def walk_java_package(self, package_dir, smali_proc_func):
        #log(package_dir)
        for root, dirs, files in os.walk(package_dir):
            #log(files)
            #for dir in dirs:
            #    dir_full_path = os.path.join(root, dir)
                #log("walk_java_package: %s" % (dir_full_path))
            #    self.walk_java_package(dir_full_path, smali_proc_func)
                
            for file in files:
                if file.endswith((".smali")):
                    file_full_path = os.path.join(root, file)
                    #log("smali_proc_func: %s" % (file_full_path))
                    smali_proc_func(file_full_path)
        
    # Parse all control from R$id or public.xml to get control name and id
    def parse_control_id(self):
        id_file_ret = self.get_id_file()
        control_id_names = 0
        if id_file_ret == RID:
            R_id_content = open(self.R_id_path, 'rb').read()
            control_id_names = re.findall(r'.field public static final (.+):I = (.+)', R_id_content)   
        elif id_file_ret == PUBLIC_XML:
            public_xml_content = open(self.public_xml_path, 'rb').read()
            control_id_names = re.findall(r'<public type=\"id\" name=\"(.+)\" id=\"(.+)\" />', public_xml_content)
                    
        if control_id_names:
            for control_id_name in control_id_names:
                control_name = control_id_name[0]
                control_name = control_name.strip()
                control_id = control_id_name[1]
                control_id = control_id.strip()
                self.control_name_id_map[control_name] = control_id

    def xml_proc_control_type(self, xml_node):
        control_type = xml_node.tagName
        if xml_node.hasAttribute("android:id"):
            control_name = xml_node.getAttribute("android:id")
            control_name = self.get_android_id_name(control_name)
            #log("FOUND android:id: %s, type: %s" % (control_name, control_type))
                
            if control_name in self.control_name_id_map:
                if not control_name in self.control_data:
                    self.control_data[control_name] = {}
                    
                # should have both "type" and "id"
                self.control_data[control_name]["type"] = control_type
                self.control_data[control_name]["id"] = self.control_name_id_map[control_name]
                # which classes are accessing this control
                self.control_data[control_name]["access"] = []
    
    # Parse all control from layout xml files to get control name and type
    def parse_control_type(self):
        layout_dir = fix_win_path("res/layout")
        layout_dir = os.path.join(self.decompile_dir, layout_dir)
        
        layout_xmls = []
        
        # get layout xml files
        for root, dirs, files in os.walk(layout_dir):
            for file in files:
                if file.endswith((".xml")):
                    layout_xmls.append(os.path.join(layout_dir, file))
    
        # parse xml files
        for layout_xml in layout_xmls:
            xml_dom = minidom.parse(layout_xml)
            xml_root = xml_dom.documentElement
            self.walk_xml_node(xml_root, self.xml_proc_control_type)
        
        #log(self.control_data)
            
    def smali_proc_control_access(self, smali_file):
        #log("%s" % (smali_file))
        smali_file_content = open(smali_file, 'rb').read()
        
        class_name = self.get_class_from_smali_content(smali_file_content)
        if class_name == "":
            return
        
        if class_name.endswith("/R") or class_name.endswith("/R$id"):
            return
        
        for control_name, control_data in self.control_data.items():
            control_id = control_data["id"]
            if not smali_file_content.find(control_id) == -1:
                # Found a control id
                #log("Found %s access %s" % (class_name, control_name))
                self.control_data[control_name]["access"].append(class_name)
    
    # Parse all control in smali to find which classes are accessing is       
    def parse_control_access(self):
        self.walk_java_package(self.decompile_smali_dir, self.smali_proc_control_access)
    
    # Parse all control from layout xml files to get control name, id and type
    def parse_control(self):
        log("\nAnalyse Android apk data...")
        
        # 1st, get name and id map
        log("\nSearch control id...")
        self.parse_control_id()
        
        # 2nd, get name, type and id
        log("\nSearch control type...")
        self.parse_control_type()
        
        # 3rd, get id in class
        log("\nSearch Activity/Fragment access known control...")
        self.parse_control_access()
        
    # Get raw control data
    # Call parse_control first
    # control_data[control_name]{id:xxx,type:xxx,access:[xxx,yyy]}
    def get_control_data(self):
        return self.control_data
       
    # Find id of given control name 
    # Call parse_control first
    def get_control_id(self, control_name):
        if control_name in self.control_data:
            # should have id attribute
            control_id = self.control_data[control_name]["id"]
            log("FOUND %s => id: %s" % (control_name, control_id))
            return control_id
        
        return ""
    
    # Find type of given control name 
    # Call parse_control first
    def get_control_type(self, control_name):
        if control_name in self.control_data:
            # should have id attribute
            control_id = self.control_data[control_name]["type"]
            log("FOUND %s => type: %s" % (control_name, control_id))
            return control_id
        
        return ""
    
    def join_smali_path(self, class_name):
        class_name = class_name.replace(".", "/")
        smali_path = os.path.join(self.decompile_smali_dir, fix_win_path(class_name))
        smali_path = "%s.smali" % (smali_path)
        return smali_path
    
    # Read out smali content of given class name
    def read_smali_content(self, class_name):
        smali_path = self.join_smali_path(class_name)
        if os.path.exists(smali_path):
            return open(smali_path, 'rb').read()
        else:
            return -1
        
    # Read out smali content of given class name
    def write_smali_content(self, class_name, smali_content):
        smali_path = self.join_smali_path(class_name)
        if os.path.exists(smali_path):
            smali_file = open(smali_path, 'wb')
            smali_file.write(smali_content)
            smali_file.close()
        
    # Read string name by id from public.xml    
    def get_string_name_by_id(self, string_id):
        id_mangling = string_id
        if id_mangling.startswith("@id/"):
            id_mangling = id_mangling[4:]
        elif id_mangling.startswith("@"):
            id_mangling = id_mangling[1:]
        else:
            return ""
        
        id_mangling = "0x%s" % (id_mangling)
        
        public_xml_path_local = fix_win_path(PUBLIC_XML_PATH)
        public_xml_path_local = os.path.join(self.decompile_dir, public_xml_path_local)
        if os.path.exists(public_xml_path_local):
            public_xml_content = open(public_xml_path_local, 'rb').read()
            string_name = re.search(r'<public type=\"string\" name=\"(.+)\" id=\"%s\" />' % (id_mangling), 
                                    public_xml_content)
            if string_name:
                string_name = string_name.group(1)
                return string_name
        
        return ""
    
    # Read string by name from strings.xml    
    def get_string_by_name(self, string_name):
        strings_xml_path_local = fix_win_path(STRINGS_XML_PATH)
        strings_xml_path_local = os.path.join(self.decompile_dir, strings_xml_path_local)
        if os.path.exists(strings_xml_path_local):
            strings_xml_content = open(strings_xml_path_local, 'rb').read()
            string_value = re.search(r'<string name=\"%s\">(.+)</string>' % (string_name), 
                                     strings_xml_content)
            if string_value:
                string_value = string_value.group(1)
                return string_value
        
        return ""
    
    # Read string by id
    def get_string_by_id(self, string_id):
        string_name = self.get_string_name_by_id(string_id)
        if string_name == "":
            return ""
        
        return self.get_string_by_name(string_name)
