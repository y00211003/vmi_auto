#
# Utility
# Author: Wayne Sun
# Date: 2014-04-29
#
#

import json
import os
import platform
import shlex
import shutil
import sys

from subprocess import Popen, PIPE, STDOUT

# Log to stdout
def log(message):
    print "%s" % (message)
    
# Log to stderr
def log_err(message):
    print >> sys.stderr, message
    
def run_cmd(cmd):
    log("Run: \n%s" % (cmd))
    os.system(cmd)

def run_cmd_with_stdio(cmd, input_data):
    log("Run: \n%s" % (cmd))
    p = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    return p.communicate(input = input_data)[0]

def run_cmd_with_stderr(cmd):
    log("Run: \n%s" % (cmd))
    p = Popen(shlex.split(cmd), stdout=PIPE, stdin=PIPE, stderr=PIPE)
    
    stdout_text, stderr_text = p.communicate()
    
    return stderr_text
    
def is_windows_sys():
    return (platform.system() == "Windows")

def fix_win_path(path):
    if is_windows_sys():
        return path.replace("/", "\\")
    else:
        return path
    
def find_strings_in_string(strings, in_string):
    for str_itr in strings:
        if in_string.find(str_itr) >= 0:
            return True
        
    return False

def copy_file(source, dest):
    shutil.copyfile(source, dest);

def copy_dir(source, dest):
    for filename in os.listdir(source):
        src_file = os.path.join(source, filename)
        dst_file = os.path.join(dest, filename)
        if os.path.isdir(src_file):
            if not os.path.exists(dst_file):
                os.mkdir(dst_file)
            copy_dir(src_file, dst_file)
        
        if os.path.isfile(src_file):
            copy_file(src_file, dst_file);

def remove_file(path):
    if os.path.exists(path):
        os.remove(path)            

def remove_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    
def get_file_ext_name(filename):
    ext_name = filename.split('.')
    ext_name = ext_name[len(ext_name) - 1]
    return ext_name

def escape_json_string(input_str):
    return json.dumps(input_str)

def zip_extract_file_win(zip_file, extract_file_pattern):
    cmd = "7z -tzip e \"%s\" \"%s\"" % (zip_file, extract_file_pattern)
    run_cmd(cmd)
    
def zip_extract_file_unix(zip_file, extract_file_pattern):
    cmd = "unzip \"%s\" \"%s\"" % (zip_file, extract_file_pattern)
    run_cmd(cmd)

def zip_extract_file(zip_file, extract_file_pattern):
    if is_windows_sys():
        zip_extract_file_win(zip_file, extract_file_pattern)
    else:
        zip_extract_file_unix(zip_file, extract_file_pattern)

def zip_add_file_win(zip_file, add_file):
    cmd = "7z -tzip a \"%s\" \"%s\"" % (zip_file, add_file)
    run_cmd(cmd)
    
def zip_add_file_unix(zip_file, add_file):
    cmd = "zip \"%s\" \"%s\"" % (zip_file, add_file)
    run_cmd(cmd)

def zip_add_file(zip_file, add_file):
    if is_windows_sys():
        zip_add_file_win(zip_file, add_file)
    else:
        zip_add_file_unix(zip_file, add_file)

def zip_delete_file_win(zip_file, delete_file_pattern):
    cmd = "7z -tzip d \"%s\" \"%s\"" % (zip_file, delete_file_pattern)
    run_cmd(cmd)
    
def zip_delete_file_unix(zip_file, delete_file_pattern):
    cmd = "zip -d \"%s\" \"%s\"" % (zip_file, delete_file_pattern)
    run_cmd(cmd)

def zip_delete_file(zip_file, delete_file_pattern):
    if is_windows_sys():
        zip_delete_file_win(zip_file, delete_file_pattern)
    else:
        zip_delete_file_unix(zip_file, delete_file_pattern)

