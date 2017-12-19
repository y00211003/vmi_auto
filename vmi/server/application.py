# -*- coding: utf-8 -*-
'''
Author      :  xiang _wang@trendmicro.com.cn
Description :  Unia Server
'''
import os

class Application(object):
    def __init__(self, file_path= None):
        self.info = None
        self._app_data_path = os.path.join( os.path.dirname(__file__), '..','data','applications')
        if not file_path is None and os.path.exists( os.path.join(self._app_data_path , file_path) ):
            self.local_file_path =  os.path.join(self._app_data_path , file_path) 
            self.file_name = os.path.basename(file_path)
        else:
            self.local_file_path = None
        
    def dump_data(self):

        if not self.local_file_path is None:
            body = open(self.local_file_path , 'rb').read()
            return body
        else:
            return None
   
class Paper(object):
    def __init__(self, file_path= None):
        self.info = None
        self._paper_data_path = os.path.join( os.path.dirname(__file__), '..','data','wallpapers')
        if not file_path is None and os.path.exists( os.path.join(self._paper_data_path , file_path) ):
            self.local_file_path =  os.path.join(self._paper_data_path , file_path)
            self.file_name = os.path.basename(file_path)
            self.detail = os.path.basename(file_path)
        else:
            self.local_file_path = None

    def dump_data(self):

        if not self.local_file_path is None:
            body = open(self.local_file_path , 'rb').read()
            #body.name = self.detail
            return body
        else:
            return None

class TXT(object):
    def __init__(self, file_path= None):
        self.info = None
        self._txt_data_path = os.path.join( os.path.dirname(__file__), '..','data','docs')
        if not file_path is None and os.path.exists( os.path.join(self._txt_data_path , file_path) ):
            self.local_file_path =  os.path.join(self._txt_data_path , file_path)
            self.file_name = os.path.basename(file_path)
        else:
            self.local_file_path = None

    def dump_data(self):

        if not self.local_file_path is None:
            body = open(self.local_file_path , 'rb').read()
            #body.name = self.detail
            return body
        else:
            return None
 
