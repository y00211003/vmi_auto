#
# Auto wrapper for SSO
# Author: Wayne Sun
# Date: 2014-04-15
#
#

import json
import os
import re
import shutil
import sys

from util import *
from androidutil import *
from genericprovider import *
from providercommon import *
from specificprovider import *

global KEY_USERNAME
global KEY_USERNAME_WITHOUT_DOMAIN
global KEY_USERNAME_EMAIL
global KEY_PASSWORD
global KEY_EXCHANGE_SERVER
global KEY_OTHER_SERVER
global KEY_OTHER_SERVER_PORT

global CONTROL_KEYS

global SPECIAL_KEY
global SPECIAL_VALUE

global STUB_WAIT_TIME
global STUB_OTHER_SERVER
global STUB_OTHER_SERVER_PORT

global DEFAULT_WAIT_TIME
global DEFAULT_OTHER_SERVER
global DEFAULT_OTHER_SERVER_PORT

global DEFAULT_DATA_MAP

# In apk's Fragment, onCreateView maybe final, need some handle later.
ON_CREATE_VIEW = ".method public onCreateView"
ON_CREATE_VIEW_ORIG = ".method private onCreateViewOrig"
ON_CREATE_VIEW_SIGNATURE = "(Landroid/view/LayoutInflater;Landroid/view/ViewGroup;Landroid/os/Bundle;)Landroid/view/View;"

ON_CREATE_PUBLIC = ".method public onCreate"
ON_CREATE_ORIG = ".method private onCreateOrig"
ON_CREATE_SIGNATURE = "(Landroid/os/Bundle;)V"

INVOKE_METHOD = "$INVOKE_METHOD$"
FRAGMENT_CLASS_NAME = "$FRAGMENT_CLASS_NAME$"
ACTIVITY_CLASS_NAME = "$ACTIVITY_CLASS_NAME$"
ADD_USERNAME_CONTROL = "$ADD_USERNAME_CONTROL$"
ADD_PASSWORD_CONTROL = "$ADD_PASSWORD_CONTROL$"
ADD_CONTROL_VALUE = "$ADD_CONTROL_VALUE$"
USERNAME_CONTROL_ID = "$USERNAME_CONTROL_ID$"
PASSWORD_CONTROL_ID = "$PASSWORD_CONTROL_ID$"
PART_CONTROL_ID = "$CONTROL_ID$"
PART_DATA_KEY = "$DATA_KEY$"

SSO_INFO_JSON = "data/sso_info.json"
STUB_SMALI_DIR = "stub_smali"

VIRDROID_SIGN = "3082035a30820242a00302010202044e48ec12300d06092a864886f70d0101050500306f310b3009060355040613025457310f300d0603550408130654616977616e310f300d06035504071306546169706569311a3018060355040a13115472656e64204d6963726f2c20496e632e310f300d060355040b13064d6f62696c653111300f060355040313086a61636b206c6975301e170d3131303831353039353131345a170d3338313233313039353131345a306f310b3009060355040613025457310f300d0603550408130654616977616e310f300d06035504071306546169706569311a3018060355040a13115472656e64204d6963726f2c20496e632e310f300d060355040b13064d6f62696c653111300f060355040313086a61636b206c697530820122300d06092a864886f70d01010105000382010f003082010a0282010100a56b106bf71d093dc3147e21cbf9b0ae14b0b613f733c8b1600bf357aad53347e7725c0c6eec75846584f1ba4ae2a4941ede784d23d2a7a73617cc13223ebf916d16d69bf4cfa7d6bf721e0e01605649890732c5e9fc51c0389b7e696e91817c8953690f04fc0e8a26643e31cad612d19feffb131796cdb03e3e8a5e55a44811597ff76a37be29b9a9125ece952e46e486656f338261976257f109923aaf6b44dd6a0d60042620c685591b0cd59973dbb5f5b3f4205e14f455ddb7b5cd2f4b878d9cd0c67bc06e24123bd04b5e86e90a760f0bd2565eaa431fd931c2913bbf18110a70fef20fdb399f10828c67049b5b2fe1d8b984d68f59abdd46918e087f910203010001300d06092a864886f70d0101050500038201010054380329c4be27c750b6e2e3f13fa78eca14ba18e0e3424abbec0ddd34ace69f62c41d1e72dc930897610fc69fdea2d1b86069bd7602fec9afb6864619db1c961a231ed43ad8965cecb09e0a1f2f8e025c5042bbeca7e5225fa39361b140d542e3db9e174653a4cbaed282a46d44e523d4899aea67b4e9d2863d3d2f031085cf94f86c223aefe213579ce5ce13eec21f18438f4c92d187464e7dea64ea8d783eff2e3bb870f4fbdce1bc2bb80881cbbddf5fb1a95d57a3f9447c8afefae3604f4dc50c8834cc4e53c6ffae4022dd30f7e9b694540e05bdf1412cfc52995802c5c9dd692263fe39068837aebf4c9bb0bd3749c0cc66fb5a9fcdf656d30eb5fedc"
WRAPPER_SIGN = "3082039d30820285a003020102020474c35fcf300d06092a864886f70d01010b0500307e310b3009060355040613023836310b3009060355040813024a53310b3009060355040713024e4a31173015060355040a130e636f6d2e7472656e646d6963726f311f301d060355040b1316636f6d2e7472656e646d6963726f2e77726170706572311b3019060355040313125472656e644d6963726f20577261707065723020170d3134303630333037353333305a180f33313039303830323037353333305a307e310b3009060355040613023836310b3009060355040813024a53310b3009060355040713024e4a31173015060355040a130e636f6d2e7472656e646d6963726f311f301d060355040b1316636f6d2e7472656e646d6963726f2e77726170706572311b3019060355040313125472656e644d6963726f205772617070657230820122300d06092a864886f70d01010105000382010f003082010a0282010100c408141f8ec892572a05e92c94894f59723a4896a27d538d4fad641556a57b6b66f474e4a4f253f37d88b1b102418c4784613d71001d61912d22094f7557e074caed13db3b48ca9b1b82f376ff0065f708a267e17107f27ae45a038bfa6df89094f1a20b2220ad44a37725d1f968bfcac59938df1c03ad59abbf6679549d380fb4e9356e8fde8cfbd98d585d7b86e0179e209e0319f20ecbd3ecaf54018b794a50aa47e095d7a23c6ac18a413eab710495025bd472a5f9fd2969ae4a0abd76c079cb8d6ab14291fb04146ed61bdf2c3a21b89c18b481e59f17156e703afb7cc7a4a8b148527392180e89210d55fff387578bbeb58ba7ce23a3c6af128aec1e370203010001a321301f301d0603551d0e04160414d7b3a542cfef8ed5f9c4f7ab9bc0152a172207bd300d06092a864886f70d01010b0500038201010020a7ba622a42824dead345f7f57208ffa8fc0b70efd0d09dc69ea636c790c200cb05c9c53f34b05e545f3eab1a0bde28570e743b471ef60ebb05f8732dce0860d318576bd2aaf8698dd08dbd057a83439b561b4f3573775b38e13cde1ab22f584a39b4bdec19a7f42780795aa21936be43b8c4c299da123ef1d69f4d763932d30a501caa3136701124c6c5476e5032aa43ff41d1bcabd3cff9c77aa99be3ce71aded2656b78a960ca14c838947643703077201cdc537de1fc5be98c42c504de3133bef4e2119db3001d7c3d237c4781213d4f6eb8261558038b4e0032d3b227a81d7cb77be6ff63565349079a32e3bbb0e063d58f9ade153d020920e262ac2d0"


class VMISSOWrapper(object):
    def __init__(self, root_path, decompile_dir, android_analyzer):
        # VMIWrapper root path (hope to be full path)
        self.root_path = root_path
        # SSO information json file path (hope to be full path)
        self.sso_info_json = os.path.join(self.root_path, fix_win_path(SSO_INFO_JSON));
        # smali stub file directory (hope to be full path)
        self.stub_smali_dir = os.path.join(self.root_path, fix_win_path(STUB_SMALI_DIR));
        # current decompiled files directory (hope to be full path)
        self.decompile_dir = decompile_dir
        # AndroidAnalyzer instance
        self.android_analyzer = android_analyzer
        # GenericProvider instance
        self.generic_provider = GenericProvider(self.android_analyzer)
        # current package name
        self.package_name = ""
        # sso info for packages
        self.sso_info = {}
        # wrapper info of current package
        self.wrapper_info = {}
        # special wrapper data for packages
        self.special_app_data = {}
    
    # Prepare smali part
    # control_key_id_map have [KEY_USERNAME => control_id, KEY_PASSWORD => control_id]
    def prepare_smali_part(self, control_key_id_map, smali_content):
        for data_key in control_key_id_map:
            fragment_path = os.path.join(self.stub_smali_dir, "control.part.smali");
            fragment_part = open(fragment_path, 'rb').read()
            fragment_part = fragment_part.replace(PART_CONTROL_ID, control_key_id_map[data_key])
            fragment_part = fragment_part.replace(PART_DATA_KEY, ("\"%s\"" % data_key))
            smali_content = smali_content.replace(ADD_CONTROL_VALUE, fragment_part)
            
        smali_content = smali_content.replace(ADD_CONTROL_VALUE, "")
            
        return smali_content
    
    def find_target_function_on_inherit_chain(self, current_class, current_class_smali, function_name, function_signature):
        base_class = self.android_analyzer.get_super_class_from_smali_content(current_class_smali)
        
        if (not base_class.find("android/app/") == -1) or (not base_class.find("android/preference/") == -1):
            # in framework
            return base_class
        
        reg_signature = function_signature.replace("/", "\\/")
        reg_signature = reg_signature.replace("(", "\\(")
        reg_signature = reg_signature.replace(")", "\\)")
        reg_function_signature = r".method (public|protected)( | final )%s%s" % (function_name, reg_signature)
        
        smali_content = self.android_analyzer.read_smali_content(base_class)
        if smali_content == -1:
            return -1
        
        result = re.search(reg_function_signature, smali_content)
        if result:
            return base_class
        else:
            return self.find_target_function_on_inherit_chain(base_class, 
                                                              smali_content, 
                                                              function_name, 
                                                              function_signature)
            
    def find_function_visibility(self, target_class, function_name, function_signature):
        reg_signature = function_signature.replace("/", "\\/")
        reg_signature = reg_signature.replace("(", "\\(")
        reg_signature = reg_signature.replace(")", "\\)")
        reg_function_signature = r".method (public|protected)( | final )%s%s" % (function_name, reg_signature)
        
        smali_content = self.android_analyzer.read_smali_content(target_class)
        if smali_content == -1:
            return ""

        result = re.search(reg_function_signature, smali_content)
        if result:
            visibility = result.group(1)
            log("Found %s->%s is %s" % (target_class, function_name, visibility))
            return visibility
        
        return ""
    
    def change_function_to_nonfinal(self, target_class, function_name, function_signature):
        reg_signature = function_signature.replace("/", "\\/")
        reg_signature = reg_signature.replace("(", "\\(")
        reg_signature = reg_signature.replace(")", "\\)")
        reg_function_signature = r".method (public|protected)( | final )%s%s" % (function_name, reg_signature)
        
        smali_content = self.android_analyzer.read_smali_content(target_class)
        if smali_content == -1:
            return

        result = re.search(reg_function_signature, smali_content)
        if result:
            visibility = result.group(1)
            finalble = result.group(2)
            finalble = finalble.strip()
            if finalble == "final":
                old_funtion_decl = ".method %s final %s%s" % (visibility, function_name, function_signature)
                #log(old_funtion_decl)
                new_funtion_decl = ".method %s %s%s" % (visibility, function_name, function_signature)
                #log(new_funtion_decl)
                smali_content = smali_content.replace(old_funtion_decl, new_funtion_decl)
                self.android_analyzer.write_smali_content(target_class, smali_content)
                log("Remove final attribute on %s->%s" % (target_class, function_name))
    
    # Insert code for Activity
    def edit_activity(self, activity_class_name, smali_content, control_key_id_map):
        log("\nEdit Activity: %s" % (activity_class_name))
        
        func_on_create_public = "%s%s" % (ON_CREATE_PUBLIC, ON_CREATE_SIGNATURE)
        func_on_create_public_final = func_on_create_public.replace(" public ", " public final ")
        func_on_create_protected = func_on_create_public.replace(" public ", " protected ")
        func_on_create_protected_final = func_on_create_public.replace(" protected ", " protected final ")
        
        smali_path = os.path.join(self.stub_smali_dir, "activity.part.smali");
        smali_part = open(smali_path, 'rb').read()
        
        if (smali_content.find(func_on_create_public) == -1) and (
            smali_content.find(func_on_create_public_final) == -1) and (
            smali_content.find(func_on_create_protected) == -1) and (
            smali_content.find(func_on_create_protected_final) == -1):
            log("NOT FOUND target function: onCreate, try to find it on inherit chain.")
            log("Use invoke-super method.")
            
            # Not found target function in target Activity.
            # Try to find target function on inherit chain.
            # Add code into target Activity, invoke-super to original function on inherit chain.
            base_class = self.find_target_function_on_inherit_chain(activity_class_name, 
                                                                    smali_content, 
                                                                    "onCreate", 
                                                                    ON_CREATE_SIGNATURE)
            if base_class == -1:
                return -1
            
            visibility = "public"
            orig_visibility = self.find_function_visibility(base_class,
                                                            "onCreate", 
                                                            ON_CREATE_SIGNATURE)
            log(orig_visibility)
            if orig_visibility == "protected":
                visibility = "protected"
            
            self.change_function_to_nonfinal(base_class, 
                                             "onCreate", 
                                             ON_CREATE_SIGNATURE)
            
            log("invoke-super %s" % (base_class))
            
            smali_part = smali_part.replace(INVOKE_METHOD, "invoke-super")
            
            full_class_name = "L%s;" % (base_class)
            smali_part = smali_part.replace(ACTIVITY_CLASS_NAME, full_class_name)
            smali_part = smali_part.replace("onCreateOrig", "onCreate")
            smali_part = smali_part.replace(".method public onCreate(Landroid/os/Bundle;)V", 
                                            ".method %s onCreate(Landroid/os/Bundle;)V" % (visibility))
            
        else: 
            log("FOUND target function: onCreate")
            log("Use invoke-direct method.")
            
            # Maybe public or protected or final, only one will hit
            func_on_create_orig = "%s%s" % (ON_CREATE_ORIG, ON_CREATE_SIGNATURE)
            smali_content = smali_content.replace(func_on_create_public, func_on_create_orig)
            smali_content = smali_content.replace(func_on_create_public_final, func_on_create_orig)
            smali_content = smali_content.replace(func_on_create_protected, func_on_create_orig)
            smali_content = smali_content.replace(func_on_create_protected_final, func_on_create_orig)
            
            smali_part = smali_part.replace(INVOKE_METHOD, "invoke-direct")
            
            full_class_name = "L%s;" % (activity_class_name)
            smali_part = smali_part.replace(ACTIVITY_CLASS_NAME, full_class_name)
            
        smali_part = self.prepare_smali_part(control_key_id_map, smali_part)
            
        smali_content = "%s \n\n %s" % (smali_content, smali_part)
            
        log("Done edit Activity...\n")
        return smali_content
    
    # We need to find function
    # View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState)
    # in target support/v4/app/Fragment
    # Some times, app will obfuscate code.
    # onCreateView may have another name, but its signature is always the same.
    # So we will find the name in this function.
    def find_fragment_target_function(self, activity_class_name):
        base_class = self.android_analyzer.get_known_base_class(activity_class_name)
        
        # If it is not inherited from support/v4/app/Fragment,
        # there is no possible on code obfuscation
        if base_class.find("support/v4/app") == -1:
            return "onCreateView"
        
        support_v4_app_Fragment = "android/support/v4/app/Fragment"
        on_create_view_signature = r".method public (.+)\(Landroid\/view\/LayoutInflater;Landroid\/view\/ViewGroup;Landroid\/os\/Bundle;\)Landroid\/view\/View;"
        
        fragment_base_smali_content = self.android_analyzer.read_smali_content(support_v4_app_Fragment)
        
        func_name = re.search(on_create_view_signature, fragment_base_smali_content)
        if func_name:
            func_name = func_name.group(1)
            log("FOUND android/support/v4/app/Fragment target function: %s" % (func_name))
            return func_name
        
        # no can do
        return -1
        
    # Insert code for Fragment
    def edit_fragment(self, activity_class_name, smali_content, control_key_id_map):
        log("\nEdit Fragment: %s" % (activity_class_name))
        
        func_on_create_view = self.find_fragment_target_function(activity_class_name)
        if func_on_create_view == -1:
            return -1 # failed
        
        smali_path = os.path.join(self.stub_smali_dir, "fragment.part.smali");
        smali_part = open(smali_path, 'rb').read()
        
        func_on_create_view_orig = "%sOrig" % (func_on_create_view)
        
        obfuscate_func_on_create_view = "%s%s" % (ON_CREATE_VIEW, ON_CREATE_VIEW_SIGNATURE)
        obfuscate_func_on_create_view = obfuscate_func_on_create_view.replace("onCreateView", 
                                                                    func_on_create_view)
        obfuscate_func_on_create_view_final = obfuscate_func_on_create_view.replace(" public ", 
                                                                    " public final ")
        
        obfuscate_func_on_create_view_orig = "%s%s" % (ON_CREATE_VIEW_ORIG, ON_CREATE_VIEW_SIGNATURE)
        obfuscate_func_on_create_view_orig = obfuscate_func_on_create_view_orig.replace("onCreateViewOrig", 
                                                                              func_on_create_view_orig)
        
        if (smali_content.find(obfuscate_func_on_create_view) == -1) and (
            smali_content.find(obfuscate_func_on_create_view_final) == -1):
            log("NOT FOUND target function: %s, try to find it on inherit chain." % (func_on_create_view))
            log("Use invoke-super.")
            
            # Not found target function in target Fragment.
            # Try to find target function on inherit chain.
            # Add code into target Fragment, invoke-super to original function on inherit chain.
            base_class = self.find_target_function_on_inherit_chain(activity_class_name, 
                                                                    smali_content, 
                                                                    func_on_create_view, 
                                                                    ON_CREATE_VIEW_SIGNATURE)
            if base_class == -1:
                return -1
            
            # Fragment onCreateView seems not able to be protected.
#             visibility = "public"
#             orig_visibility = self.find_function_visibility(base_class,
#                                                             func_on_create_view, 
#                                                             ON_CREATE_VIEW_SIGNATURE)
#             log(orig_visibility)
#             if orig_visibility == "protected":
#                 visibility = "protected"
            
            self.change_function_to_nonfinal(base_class, 
                                             func_on_create_view, 
                                             ON_CREATE_VIEW_SIGNATURE)
            
            log("invoke-super %s" % (base_class))
            
            smali_part = smali_part.replace(INVOKE_METHOD, "invoke-super")
            
            full_class_name = "L%s;" % (base_class)
            smali_part = smali_part.replace(FRAGMENT_CLASS_NAME, full_class_name)
            
            # invoke-super function
            func_on_create_view_orig_part = "->%s" % (func_on_create_view)
            smali_part = smali_part.replace("->onCreateViewOrig", func_on_create_view_orig_part)
        else:
            log("FOUND target function: %s" % (func_on_create_view))
            log("Use invoke-direct.")
            
            # Found target function in target Fragment.
            # Add code into target Fragment, invoke-direct to original function.
            
            smali_content = smali_content.replace(obfuscate_func_on_create_view, obfuscate_func_on_create_view_orig)
            smali_content = smali_content.replace(obfuscate_func_on_create_view_final, obfuscate_func_on_create_view_orig)
            
            smali_part = smali_part.replace(INVOKE_METHOD, "invoke-direct")
            
            full_class_name = "L%s;" % (activity_class_name)
            smali_part = smali_part.replace(FRAGMENT_CLASS_NAME, full_class_name)
            
            # invoke-direct function, need change to original one
            func_on_create_view_orig_part = "->%s" % (func_on_create_view_orig)
            smali_part = smali_part.replace("->onCreateViewOrig", func_on_create_view_orig_part)
          
        func_on_create_view_part = ".method public %s" % (func_on_create_view)
        smali_part = smali_part.replace(".method public onCreateView", func_on_create_view_part)
          
        smali_part = self.prepare_smali_part(control_key_id_map, smali_part)
            
        smali_content = "%s \n\n %s" % (smali_content, smali_part)
        
        log("Done edit Fragment...\n")
        return smali_content
    
    # Read prepared sso information    
    def read_sso_info(self):
        log("\nRead SSO information...")
        if not os.path.exists(self.sso_info_json):
            log("CANNOT find SSO json file: %s" % (self.sso_info_json))
            return
        
        sso_info_json_data = open(self.sso_info_json, 'rb').read()
        sso_info_json = json.loads(sso_info_json_data)
        #log(str(sso_info_json))
        count = len(sso_info_json)
        i = 0
        while i < count:
            sso_info_itr = sso_info_json[i]
            apk_name = str(sso_info_itr["name"])
            #log(str(sso_info_itr))
            self.sso_info[apk_name] = []
            
            sso_datas = sso_info_itr["data"]
            for sso_data_itr in sso_datas:
                sso_data = {}
                sso_data["activity"] = str(sso_data_itr["activity"])
                sso_data["activity_type"] = str(sso_data_itr["activity_type"])
                sso_data["username"] = str(sso_data_itr["username"])
                sso_data["password"] = str(sso_data_itr["password"])
                
                self.sso_info[apk_name].append(sso_data)
            
            i += 1
            
        #log(str(self.sso_info))
        log("Read SSO information DONE")
        
    # Find sso information
    def get_wrapper_info(self):
        if self.package_name in self.sso_info:
            return self.sso_info[self.package_name]
    
        return {}
    
    # Copy sso stub into target smali directory   
    def copy_stub(self):
        log("\nCopy smali stub...\n")
        
        source_dir_path = os.path.join(self.stub_smali_dir, "com")
        target_dir_path = os.path.join(self.decompile_dir, "smali")
        target_dir_path = os.path.join(target_dir_path, "com")
        copy_dir(source_dir_path, target_dir_path)
        
    # Add wrapper code into target class smali file
    def add_code(self):
        log("\nAdd wrapper code into target class smali code...\n")
        
        # all False, add_code failed
        result = False
        
        for wrapper_info_itr in self.wrapper_info:
            control_key_id_map = {}
            
            for control_key in CONTROL_KEYS:
                if control_key in wrapper_info_itr:
                    control_name = str(wrapper_info_itr[control_key])
                    control_key_id_map[control_key] = self.android_analyzer.get_control_id(control_name)
            
            activity_class_name = str(wrapper_info_itr["activity"])
            smali_content = self.android_analyzer.read_smali_content(activity_class_name)
                
            # Edit smali
            if str(wrapper_info_itr["activity_type"]) == ACTIVITY_TYPE_ACTIVITY:
                smali_content = self.edit_activity(activity_class_name, 
                                                    smali_content, 
                                                    control_key_id_map)
            elif str(wrapper_info_itr["activity_type"]) == ACTIVITY_TYPE_FRAGMENT:
                smali_content = self.edit_fragment(activity_class_name, 
                                                    smali_content, 
                                                    control_key_id_map)
            
            if smali_content == -1:
                log("Failed to inject code.")
                result = result or False
                continue
            
            # Write back
            self.android_analyzer.write_smali_content(activity_class_name, smali_content)
            # This succeed
            result = result or True
            
        return result
            
    def auto_analyse_sso_info(self):
        if self.package_name in self.sso_info:
            # We already know this
            log("FOUND %s in SSO json file" % (self.package_name))
            return
        
        suspicious_activities = []
        
        self.generic_provider.refresh_control_data()
        self.generic_provider.find_edittext()
    
        edittext_control_data = self.generic_provider.edittext_control_data
        #log(edittext_control_data)
        edittext_in_same_activity = self.generic_provider.find_controls_in_same_activity(edittext_control_data)
        #log(edittext_in_same_activity)
        
        specific_provider = SpecificProvider(self.root_path ,self.android_analyzer)
        
        self.special_app_data = specific_provider.special_app_data
        
        suspicious_activities = specific_provider.find_specific_login_activity(edittext_in_same_activity)
        
        if len(suspicious_activities) == 0:
            # No specific login Activity found
            suspicious_activities = self.generic_provider.find_suspicious_login_activity(edittext_in_same_activity)
        
        self.sso_info[self.package_name] = []
        for suspicious_activity in suspicious_activities:
            activity_sso_info = {}
            activity_sso_info["activity"] = str(suspicious_activity["activity"])
            activity_sso_info["activity_type"] = str(suspicious_activity["activity_type"])
            
            for optional_key in CONTROL_KEYS:
                if optional_key in suspicious_activity:
                    activity_sso_info[optional_key] = str(suspicious_activity[optional_key])
                
            log(str(activity_sso_info))
            
            self.sso_info[self.package_name].append(activity_sso_info)
    
    # Add user-permission into AndroidManifest.xml
    def add_permission(self):
        GET_ACCOUNTS = "android.permission.GET_ACCOUNTS"
        
        if not self.android_analyzer.has_user_permission(GET_ACCOUNTS):
            self.android_analyzer.add_user_permission(GET_ACCOUNTS)
        
        #if not self.android_analyzer.has_user_permission(MANAGE_ACCOUNTS):
        #    self.android_analyzer.add_user_permission(MANAGE_ACCOUNTS)
            
        #if not self.android_analyzer.has_user_permission(MANAGE_ACCOUNTS):
        #    self.android_analyzer.add_user_permission(MANAGE_ACCOUNTS)
    
    def replace_virdriod_sign(self, smali_file):
        smali_file_content = open(smali_file, 'rb').read()
        if smali_file_content.find(VIRDROID_SIGN) >= 0:
            log("Found VMI signature: %s" % (smali_file))
            smali_file_content = smali_file_content.replace(VIRDROID_SIGN, WRAPPER_SIGN)
            smali_file_obj = open(smali_file, 'wb')
            smali_file_obj.write(smali_file_content)
            smali_file_obj.close()
            
    def replace_smali_with_data(self, smali_file, data_array):
        #log("replace_smali_with_data: %s" % (smali_file))
        smali_file_content = open(smali_file, 'rb').read()
        
        file_changed = False
        
        data_array_count = len(data_array)
        i = 0
        while i < data_array_count:
            stub_key = data_array[i][SPECIAL_KEY]
            stub_value = data_array[i][SPECIAL_VALUE]
            
            if smali_file_content.find(stub_key) >= 0:
                log("Replace \"%s\" with \"%s\"" % (stub_key, stub_value))
                smali_file_content = smali_file_content.replace(stub_key, 
                                                                stub_value)
                file_changed = True
                
            i += 1
        
        # write back
        if file_changed:
            log("Changed: %s" % (smali_file))
            smali_file_obj = open(smali_file, 'wb')
            smali_file_obj.write(smali_file_content)
            smali_file_obj.close()
            
    def replace_smali_with_default_data(self, smali_file):
        self.replace_smali_with_data(smali_file, DEFAULT_DATA_MAP)
            
    def replace_smali_with_allapp_data(self, smali_file):
        allapp_data = self.special_app_data["*"]
        self.replace_smali_with_data(smali_file, allapp_data)
            
    def replace_smali_with_special_data(self, smali_file):
        special_data = self.special_app_data[self.package_name]
        self.replace_smali_with_data(smali_file, special_data)
        
    # In smali file, we have some stub value
    # We need to replace them with real value
    def replace_smali_stub_data(self):
        # replace some stub data
        #log(str(self.special_app_data))
        trend_smali_dir = os.path.join(self.decompile_dir, fix_win_path("smali/com/trendmicro/vmi/sso"))
            
        # 1st, if "*" exists, use these value first
        if "*" in self.special_app_data:
            log("Found all app data (*):\n%s" % (str(self.special_app_data["*"])))
            self.android_analyzer.walk_java_package(trend_smali_dir, self.replace_smali_with_allapp_data)
            
        # 2nd, use app special value
        if self.package_name in self.special_app_data:
            log("Found %s special app data:\n%s" % (self.package_name, 
                                                    str(self.special_app_data[self.package_name])))
            self.android_analyzer.walk_java_package(trend_smali_dir, self.replace_smali_with_special_data)
            
        # last, use default value for rest of data
        log("Use default data for rest of data")
        self.android_analyzer.walk_java_package(trend_smali_dir, self.replace_smali_with_default_data)
    
    # return 0, success
    # return -1, no wrapper info found, do nothing
    
    def do_fuckSignatureWrapper(self):
        log("\nFucking Vmi client signature")
        ret = {}
        ret["result"] = 0
        ret["message"] = ""
        try:
            self.android_analyzer.walk_java_package(self.decompile_dir, self.fuckSmaliContainsSignature)
        except Exception as e:
            print e
            ret["result"] = -1
        
        print ret
        return ret
    
    def fuckSmaliContainsSignature(self, smali_file):
        
        smali_file_content = open(smali_file, 'rb').read()
        if smali_file_content.find(VIRDROID_SIGN) >= 0:
            log("Found VMI signature: %s" % (smali_file))
            sign_offset = smali_file_content.index(VIRDROID_SIGN)
            print sign_offset - 1692
            #print smali_file_content[sign_offset - 1692:sign_offset - 1677]
            func_entrance_offset =  smali_file_content[0:sign_offset].rindex('.method public static a(Landroid/content/Context;)Z')
            print 'entrance:'+str(func_entrance_offset)
            fucked_smali_part = smali_file_content[func_entrance_offset:sign_offset].replace('const/4 v0, 0x0','const/4 v0, 0x1')
            fucked_smali_file_content = smali_file_content[0:func_entrance_offset] +fucked_smali_part + smali_file_content[sign_offset:]
            #smali_file_content = smali_file_content.replace(VIRDROID_SIGN, WRAPPER_SIGN)
            smali_file_obj = open(smali_file, 'wb')
            smali_file_obj.write(fucked_smali_file_content)
            smali_file_obj.close()
            
            
    
    
    def do_ssowrapper(self):
        log("\nDo ssowrapper...")
        
        ret = {}
        ret["result"] = 0
        ret["message"] = ""
        
        # read SSO info from prepared json file
        #self.read_sso_info()
        
        self.android_analyzer.parse_control()
        
        log("Find target Activity/Fragment...")
        self.package_name = self.android_analyzer.get_package_name()
        log("Package name: %s" % (self.package_name))
        
        log("Analyse %s ..." % (self.package_name))
        # Auto analyse APK
        self.auto_analyse_sso_info()
        
        log("Add wrapper code...")
        self.wrapper_info = self.get_wrapper_info()
        log(str(self.wrapper_info))
        if len(self.wrapper_info) > 0:
            #self.add_permission()
            self.copy_stub()
            add_code_ret = self.add_code()
            if add_code_ret == False:
                err_msg = "1"
                log("Code inject failed.")
                ret["result"] = -1
                ret["message"] = err_msg
                return ret
            
            self.replace_smali_stub_data()
            
            # magic for virdroid
            if self.package_name == "com.trendmicro.virdroid":
                log("Found VMI Client :>")
                # replace cert
                self.android_analyzer.walk_java_package(self.decompile_dir, self.replace_virdriod_sign)
            
        else:
            err_msg = "2"
            log("No wrapper information found.")
            ret["result"] = -1
            ret["message"] = err_msg
            return ret
        
        log("\nDONE ssowrapper...\n")
        
        return ret
