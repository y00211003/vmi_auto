# -*- coding: utf-8 -*-
'''
Author      :  xiang_wang@trendmicro.com.cn
Description :  Data Access Level
'''

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from vmi.utility.logger import Logger
from vmi.singleton import Singleton
from authuser import AuthUser
from accountuserex import AccountUserex
from app import App
from policyvalue import PolicyValue
from vmi.configure import Configure

log = Logger(__name__)

#@Singleton
class DalService(object):

    def __init__(self):
        self.config = Configure.Instance()
        config = self.config

        db_host = config.get('DataBase','host')
        db_uri = 'mysql://vmi:vmi4trend@'+ db_host +'/vmi'
        db_engine = create_engine(db_uri)
        Session = sessionmaker(bind=db_engine)
        self.session = Session()
                                        
    def disable_change_password(self, user_name):
        res = self.session.query(AuthUser).filter(AuthUser.username==user_name).first()
        user_id = res.id
        account = self.session.query(AccountUserex).get(user_id)
        account.need_change_password = 0
        self.session.commit()
        
    def get_app_attr_by_id(self, app_id, attr):

        app = self.session.query(App).filter(App.id == app_id).first()
        
        if hasattr(app, attr):
            return getattr(app, attr)
        else:
            raise ValueError('Invalid Attribute Information')

    def get_wallpaper_path_by_id(self, w_id):
        policy = self.session.query(PolicyValue).filter(PolicyValue.id == w_id).first()
        value = policy.value
        path = value.split('/')[-1]
        return path
    
    def get_policy_assign_durance_by_name(self, user_name):

        user = self.session.query(AuthUser).filter(AuthUser.username == user_name).first()

        account = self.session.query(AccountUserex).filter(AccountUserex.user_id == user.id).first()

        begin_apply_policy_time = account.begin_apply_policy_time
        last_apply_policy_time = account.last_apply_policy_time

        #print begin_apply_policy_time, last_apply_policy_time

        if begin_apply_policy_time > last_apply_policy_time:
            return None
        else :
            return  begin_apply_policy_time, last_apply_policy_time, last_apply_policy_time - begin_apply_policy_time
