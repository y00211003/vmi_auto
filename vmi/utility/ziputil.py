'''
Created on Jul 30, 2012

@author: xiang_wang@trendmicro.com.cn
'''
import sys, zipfile, os, os.path
import shutil
from mdm.utility.logger import Logger

log = Logger("Zip Package")
class ZipPackage(object):
    '''

    '''
    def __init__(self, zip_file):
        super(ZipPackage, self).__init__()
        self.zip_file = zip_file


    def unzip_to_folder(self, folder):
        for root, dirs, files in os.walk(folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        try:            
            if not os.path.exists(folder):
                os.makedirs(folder)

            zfobj = zipfile.ZipFile(self.zip_file)
            for name in zfobj.namelist():
                if name.endswith('/')  or name.endswith('\\'):
                    os.mkdir(os.path.join(folder, name))
                else:
                    outfile = open(os.path.join(folder, name), 'wb')
                    outfile.write(zfobj.read(name))
                    outfile.close()

        except IOError:
            print "ZipFileUtil error"
