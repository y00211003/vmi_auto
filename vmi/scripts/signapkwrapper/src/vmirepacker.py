#!/usr/bin/python
# Auto Repacker for VMI
# Author: Wayne Sun
# Date: 2014-04-15
#
# To run this, we need:
# java
# jarsigner
# apktool
# smali-1.x
# axml
# 7z/zip
#
#

import os
import re
import shutil
import sys
import time

from util import *
from androidutil import *
from ssowrapper import VMISSOWrapper
from debugwrapper import VMIDebugWrapper

JAVA_PATH = "java"
JARSIGNER_PATH = "jarsigner"
KEYTOOL_PATH = "keytool"

APKTOOL = "tools/apktool.jar"
SMALI = "tools/smali-2.0.3.jar"
AXML = "tools/axml.jar"

KEYSTORE_FILE = "keystore/com.trendmicro.wrapper"
KEYSTORE_NAME = "com.trendmicro.wrapper"
KEYSTORE_SIGNATURE = "X.509, CN=TrendMicro Wrapper, OU=com.trendmicro.wrapper, O=com.trendmicro, L=NJ, ST=JS, C=86"
KEYSTORE_MD5 = "C4:FA:88:40:1C:E8:B6:68:8F:EC:38:BA:9C:5C:42:84"

class VMIRepacker(object):
    def __init__(self, apk_source, working_dir = ""):
        # the source apk file (full name)
        self.apk_source = apk_source
        # the apk file name (without .apk extension)
        self.apk_file_name = ""
        # repacked apk path (without signature, hope to be full path)
        self.apk_repacked_path = ""
        # repacked apk path (signed, hope to be full path)
        self.apk_repacked_signed_path = ""
        # working directory (hope to be full path)
        if not working_dir == "":
            self.working_dir = working_dir
        else:
            self.working_dir = "E:\\temp\\sso_working"
        # decompiled files directory
        self.decompile_dir = ""
        # old cwd
        self.old_cwd_path = ""
        # full paths
        self.root_path = os.path.abspath(fix_win_path("../"))
        
        self.java_path = fix_win_path(JAVA_PATH)
        self.jarsigner_path = fix_win_path(JARSIGNER_PATH)
        self.keytool_path = fix_win_path(KEYTOOL_PATH)
        
        self.apktool_path = os.path.join(self.root_path, fix_win_path(APKTOOL))
        self.smali_path = os.path.join(self.root_path, fix_win_path(SMALI))
        self.axml_path = os.path.join(self.root_path, fix_win_path(AXML))
        
        self.keystore_path = os.path.join(self.root_path, fix_win_path(KEYSTORE_FILE))
    
    def prepare(self):
        log("\nPrepare...")
        log("ROOT path:\n%s" % self.root_path)
        
        self.apk_file_name = os.path.basename(self.apk_source)
        ext_name = self.apk_file_name.split('.')
        ext_name = ext_name[len(ext_name) - 1]
        if not ext_name == "apk":
            log("Not an apk?")
            return -1
        if (not os.path.exists(self.apk_source)) or (
            not os.path.isfile(self.apk_source)):
            log("No file found at \"%s\"." % (self.apk_source))
            return -1
        
        log("Let's hack \"%s\"" % (self.apk_source))
        
        self.apk_file_name = self.apk_file_name[:-4] # remove .apk
        self.apk_repacked_path = "%s.rep.apk" % (self.apk_file_name)
        
        sign_apk = "%s.sign.apk" % (self.apk_file_name)
        sign_apk = os.path.join(self.working_dir, sign_apk)
        self.apk_repacked_signed_path = sign_apk
        if os.path.exists(self.apk_repacked_signed_path):
            remove_file(self.apk_repacked_signed_path)
        
        # copy to working dir
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
            
        self.apk_repacked_path = os.path.join(self.working_dir, self.apk_repacked_path)
        self.apk_repacked_path = os.path.abspath(self.apk_repacked_path)
        if os.path.exists(self.apk_repacked_path):
            remove_file(self.apk_repacked_path)
        copy_file(self.apk_source, self.apk_repacked_path);
        return 0
    
    def decompile(self):
        log("\nDecompile...")
        
        self.decompile_dir = os.path.join(self.working_dir, self.apk_file_name)
        if os.path.exists(self.decompile_dir):
            remove_dir(self.decompile_dir)
            
        # use apktool to decompile
        cmd = "%s -jar \"%s\" d \"%s\" -o \"%s\"" % (self.java_path, self.apktool_path, self.apk_repacked_path, self.decompile_dir)
        run_cmd(cmd)
        
        # unzip original META-INF out
        if is_windows_sys():
            meta_info_dir = os.path.join(self.decompile_dir, "META-INF")
            os.mkdir(meta_info_dir)
            os.chdir(meta_info_dir)
        else:
            os.chdir(self.decompile_dir)
            
        zip_extract_file(self.apk_repacked_path, "META-INF/*")
        os.chdir(self.working_dir)
        
    def change_manifest_version(self, android_analyzer):
        log("\nChange versionName..")
        
        axml_dir = os.path.join(self.decompile_dir, "amxl")
        if not os.path.exists(axml_dir):
            os.mkdir(axml_dir)
        
        os.chdir(axml_dir)
        
        zip_extract_file(self.apk_repacked_path, "AndroidManifest.xml")
        
        manifest_extract = os.path.join(axml_dir, "AndroidManifest.xml")
        manifest_plain = os.path.join(axml_dir, "AndroidManifest.p.xml")
        manifest_binary = os.path.join(axml_dir, "AndroidManifest.b.xml")
        manifest_binary_new = os.path.join(axml_dir, "AndroidManifest.xml")
        
        os.rename(manifest_extract, manifest_binary)
        
        # decompile xml
        cmd = "%s -jar \"%s\" b2x \"%s\" \"%s\"" % (self.java_path, self.axml_path, manifest_binary, manifest_plain)
        run_cmd(cmd)
        
        # change versionName
        manifest_content = open(manifest_plain, 'rb').read()
        version_name = re.search(r'versionName=\"([^"]*)\"', manifest_content)
        if version_name:
            log("\n")
            
            version_name = version_name.group(1)
            version_name = version_name.strip()
            
            log("versionName: %s" % (version_name))
            
            new_version_name = version_name
            
            if version_name.startswith("@"):
                log("versionName is an id, let's get real value.")
                new_version_name = android_analyzer.get_string_by_id(version_name)
                log("versionName: %s => %s." % (version_name, new_version_name))
                
            new_version_name = "3.0.9999"
            
            #manifest_content = manifest_content.replace("versionName=\"%s\"" % (version_name),
            #                                            "versionName=\"%s\"" % (new_version_name))
            
            manifest_file = open(manifest_plain, 'wb')
            manifest_file.write(manifest_content)
            manifest_file.close()
            
            log("\n")
        
        # compile xml
        cmd = "%s -jar \"%s\" x2b \"%s\" \"%s\"" % (self.java_path, self.axml_path, manifest_plain, manifest_binary_new)
        run_cmd(cmd)
        
        # replace zip
        zip_delete_file(self.apk_repacked_path, "AndroidManifest.xml")
        zip_add_file(self.apk_repacked_path, "AndroidManifest.xml")
        
        os.chdir(self.working_dir)
        
    def recompile(self):
        log("\nRecompile...")
        
        newdex_path = os.path.join(self.decompile_dir, "classes.dex")
        smali_path = os.path.join(self.decompile_dir, "smali")
        cmd = "%s -Xms1024m -jar \"%s\" -o \"%s\" \"%s\"" % (self.java_path, self.smali_path, newdex_path, smali_path)
        run_cmd(cmd)
        
    def repack(self, android_analyzer):
        log("\nRepack...")
        
        # change AndroidManifest
        self.change_manifest_version(android_analyzer)
        
        # delete old dex and signature
        zip_delete_file(self.apk_repacked_path, "classes.dex")
        zip_delete_file(self.apk_repacked_path, "META-INF/*")
        
        # add new dex
        # to keep classes.dex in zip root, chdir to self.decompile_dir,
        # then come back.
        os.chdir(self.decompile_dir)
        zip_add_file(self.apk_repacked_path, "classes.dex")
        os.chdir(self.working_dir)
        
    def signapk(self):
        log("\nSign apk...")
        
        cmd = "%s -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore" % (self.jarsigner_path)
        cmd = "%s \"%s\"" % (cmd, self.keystore_path)
        cmd = "%s -signedjar" % (cmd)
        
        cmd = "%s \"%s\" \"%s\" %s" % (cmd, 
                                       self.apk_repacked_signed_path, 
                                       self.apk_repacked_path,
                                       KEYSTORE_NAME)
        run_cmd_with_stdio(cmd, "trendmicro")
        
    # Check if this apk is wrapped by VMIRepacker
    # by checking if file is signed by our keystore.
    def check_wrapped_cert_by_signature(self, apk_path):
        cmd = "%s -verify -verbose -certs \"%s\"" % (self.jarsigner_path, apk_path)
        verify_result = run_cmd_with_stdio(cmd, "")
        
        if verify_result.find(KEYSTORE_SIGNATURE) >= 0:
            return True
        
        return False
    
    def find_package_rsa(self):
        meta_info_dir = os.path.join(self.decompile_dir, "META-INF")
        if not os.path.exists(meta_info_dir):
            return ""
        
        files = os.listdir(meta_info_dir)
        for file in files:
            if get_file_ext_name(file).lower() == "rsa":
                return os.path.join(meta_info_dir, file)
        
        return ""
    
    # Check if this apk is wrapped by VMIRepacker
    # by checking RSA signature MD5.
    def check_wrapped_cert_by_rsa(self, rsa_path):
        if rsa_path == "":
            return False
        
        rsa_data = open(rsa_path, 'rb').read()
        
        cmd = "%s -printcert" % (self.keytool_path)
        verify_result = run_cmd_with_stdio(cmd, rsa_data)
        
        #log(verify_result)
        
        if verify_result.find(KEYSTORE_MD5) >= 0:
            return True
        
        return False
        
    def check_result(self):
        if os.path.exists(self.apk_repacked_signed_path):
            log("\nRepack succeed!\nFOUND: %s" % (self.apk_repacked_signed_path))
            return 0
        else:
            log("\nRepack failed!\nNOT FOUND: %s" % (self.apk_repacked_signed_path))
            return -1
        
    def return_result_and_cleanup(self, ret, message):
        # clean up
        remove_dir(self.decompile_dir)
        remove_file(self.apk_repacked_path)
        
        # return result to stderr
        result_json = "{\"code\":%s,\"detail\":%s}" % (ret, escape_json_string(message))
        log_err(result_json)

    def go(self):
        ret = self.prepare()
        if ret == -1:
            self.return_result_and_cleanup(-1, "4")
            return
        
        # cd to working directory
        self.old_cwd_path = os.getcwd()
        os.chdir(self.working_dir)
        
        self.decompile()
        
        package_rsa_path = self.find_package_rsa()
        #log(package_rsa_path)
        
        if self.check_wrapped_cert_by_rsa(package_rsa_path):
            log("Already wrapped!")
            self.return_result_and_cleanup(-1, "7")
        else:
            # let's do real work
            android_analyzer = AndroidAnalyzer(self.root_path, self.decompile_dir)
            
            wrapper = VMISSOWrapper(self.root_path, self.decompile_dir, android_analyzer)
            ret = wrapper.do_fuckSignatureWrapper()
            #print ret
            
            #wrapper = VMIDebugWrapper(self.root_path, self.decompile_dir)
            #ret = wrapper.do_debugwrapper()
            
            if ret["result"] == -1:
                log("NO wrapper work need to do, exit!")
                self.return_result_and_cleanup(-1, ret["message"])
            else:
                log("Ready to recompile!")
                #time.sleep(10)
                
                self.recompile()
                
                self.repack(android_analyzer)
                
                self.signapk()
                
                ret = self.check_result()
                if ret == 0:
                    # successed
                    self.return_result_and_cleanup(0, self.apk_repacked_signed_path)
                else:
                    self.return_result_and_cleanup(-1, "3")
            
        # go back
        os.chdir(self.old_cwd_path)
     
def main():
    apk_path = ""
    working_dir = ""
    
    if len(sys.argv) < 2:
        print "Useage: python vmirepacker.py xxx.apk [outputdir]"
        quit()
    elif len(sys.argv) == 2:
        apk_path = sys.argv[1]
    elif len(sys.argv) == 3:
        apk_path = sys.argv[1]
        working_dir = sys.argv[2]
    
    repacker = VMIRepacker(apk_path, working_dir)
    
    repacker.go()
    
if __name__ == '__main__':
    main();
