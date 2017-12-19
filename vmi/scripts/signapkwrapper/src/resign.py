#
# Resign repack apk
# Author: Wayne Sun
# Date: 2014-05-15
#
#

import os
import shutil
import sys
import time

from util import *

def signapk(apk_path):
    log("\nSign apk...")
    
    apk_file_name = os.path.basename(apk_path)
    apk_dir_path = os.path.dirname(apk_path)
    apk_signed_name = apk_file_name.replace(".apk", ".sign.apk")
    apk_signed_path = os.path.join(apk_dir_path, apk_signed_name)
    
    cmd = "jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore"
    cmd = "%s \"%s\"" % (cmd, "E:\\coding\\apk_wrapper_poc\\keystore\\com.trendmicro.wrapper")
    cmd = "%s -signedjar" % (cmd)

    cmd = "%s \"%s\" \"%s\" com.trendmicro.wrapper" % (cmd, apk_signed_path, apk_path)
    run_cmd_with_stdio(cmd, "trendmicro")

def main():
    if len(sys.argv) < 2:
        print "Useage: python resign.py xxx.apk"
        quit()
    
    apk_path = sys.argv[1]
    
    signapk(apk_path)
    
if __name__ == '__main__':
    main();
