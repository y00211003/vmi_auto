'''
Created on Jul 30, 2012

@author: xiang_wang@trendmicro.com.cn
'''

from vmi.singleton import Singleton
import ConfigParser, os, threading
from vmi.utility.logger import Logger

log = Logger(__file__)

class INIParser (dict):
    '''
    Ini file parser
    '''
    def __init__(self, configfile = None):
        self.config = ConfigParser.SafeConfigParser()
        
        if configfile == None:

            self._config_path =  os.path.join(os.path.dirname(__file__),'config.ini')
        else:
            self._config_path = configfile
        self.config.read(self._config_path)
        
    @property
    def config_path(self):
        return self._config_path

    @config_path.setter
    def config_path(self, c_path):
        self._config_path = c_path
        log.debug('Reloading config from ' + c_path + '...')
        self.reload()

    def get(self, section, key):
        if not self.config is None:
            return self.config.get(section, key)
        else:
            raise Exception("Un-initialized Instance")

    def set(self, section, key, value):
        self.config.set(section ,key, value)       

    def reload(self):
        self.config.read(self._config_path)

    def write(self):
        #save to file
        cfgfile = open(self._config_path,'w')
        self.config.write(cfgfile)
        cfgfile.close()

    def __dict__(self):
        dict.clear(self)
        dictionary = {}
        for section in self.config.sections():
            for option in self.config.options(section):
                dictionary[section][option] = self.config.get(section, option)
        return dictionary

    def __getitem__(self, section):
        result = dict()
        for option in self.config.options(section):
            result[option] = self.config.get(section,option)
        return result

    def __setitem__ (self, section , values):
        print 'test'
        if not type(values) == 'dict':
            raise TypeError
        else:
            for key in values.keys():
                self.config.set(section, key, values[key])
        self.write()


@Singleton
class Configure(INIParser):

    def __init__(self):
        configfile = None
        #for py2exe to find the config.ini path
        if os.path.exists(os.path.join(os.path.dirname(__file__),'..','..','config.ini')):
            configfile = os.path.join(os.path.dirname(__file__), '..','..','config.ini')           
        else:
            configfile  =  os.path.join(os.path.dirname(__file__),'config.ini')
        if not os.path.exists(configfile):
            
            raise IOError("No configuration file found")
        log.debug(configfile)
        INIParser.__init__(self, configfile)
