#
# Convert jar to smali
# Author: Wayne Sun
# Date: 2014-05-05
#
# To run this, we need:
# dex2jar (d2j-jar2dex)
# baksmali-1.x
# 7z/zip
#
#

import json
import os
import re
import shutil
import sys

from util import *

JAVA_PATH = "/usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java"
JAR2DEX = "tools/dex2jar/d2j-jar2dex.bat"
BAKSMALI = "tools/baksmali-2.0.3.jar"

STUB_JAVA_DIR = "stub_java"
STUB_SMALI_DIR = "stub_smali"
STUB_JAR = "stub.jar"
STUB_DEX_JAR = "stub.dex.jar"
CLASSES_DEX = "classes.dex"

def jar2dex(stub_java_dir_path):
    stub_jar_path = os.path.join(stub_java_dir_path, STUB_JAR)
    stub_dex_jar_path = os.path.join(stub_java_dir_path, STUB_DEX_JAR)
    classes_dex_path = os.path.join(stub_java_dir_path, CLASSES_DEX)
    
    if os.path.exists(stub_dex_jar_path):
        remove_file(stub_dex_jar_path)
        
    if os.path.exists(classes_dex_path):
        remove_file(classes_dex_path)
        
    cmd = "%s \"%s\" -o \"%s\"" % (JAR2DEX, stub_jar_path, stub_dex_jar_path)
    run_cmd(cmd)
    
    if not os.path.exists(stub_dex_jar_path):
        log("jar2dex FAILED!!!")
        return -1
    
    cwd = os.getcwd()
    os.chdir(stub_java_dir_path)
    
    cmd = "7z -tzip e \"%s\" %s" % (stub_dex_jar_path, CLASSES_DEX)
    run_cmd(cmd)
    
    os.chdir(cwd)
    
    if not os.path.exists(classes_dex_path):
        log("jar2dex FAILED!!!")
        return -1
    
    return 0

def baksmali(stub_java_dir_path, stub_smali_dir_path):
    old_stub_smali_dir = os.path.join(stub_smali_dir_path, "com")
    classes_dex_path = os.path.join(stub_java_dir_path, CLASSES_DEX)
    
    if os.path.exists(old_stub_smali_dir):
        remove_dir(old_stub_smali_dir)
    
    cmd = "%s -Xms1024m -jar \"%s\" -o \"%s\" \"%s\"" % (JAVA_PATH, BAKSMALI, stub_smali_dir_path, classes_dex_path)
    run_cmd(cmd)
    

def main():
    global JAR2DEX
    global BAKSMALI
    
    root_path = os.path.abspath(fix_win_path("../"))
    
    JAR2DEX = os.path.join(root_path, fix_win_path(JAR2DEX))
    BAKSMALI = os.path.join(root_path, fix_win_path(BAKSMALI))
    
    stub_java_dir_path = os.path.join(root_path, fix_win_path(STUB_JAVA_DIR))
    stub_smali_dir_path = os.path.join(root_path, fix_win_path(STUB_SMALI_DIR))
    
    if jar2dex(stub_java_dir_path) == -1:
        return
    
    baksmali(stub_java_dir_path, stub_smali_dir_path)
    
    
if __name__ == '__main__':
    main();

