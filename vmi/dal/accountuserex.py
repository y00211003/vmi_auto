from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountUserex(Base):

    __tablename__ = 'account_userex'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    policy_id = Column(Integer)
    guid= Column(String)
    phone = Column(String)
    timestamp = Column(DateTime)
    login_time = Column(DateTime)
    need_change_password = Column(SmallInteger)
    total_online_time = Column(Integer)
    idle_expired_time = Column(DateTime)
    dn = Column(Text)

    last_modified_time = Column(DateTime)
    begin_apply_policy_time = Column(DateTime)
    last_apply_policy_time = Column(DateTime)
    is_visible = Column(SmallInteger)
    status = Column(Integer)
    
    def __init__(self, user_id, guid):
        self.user_id = user_id
        self.guid = guid
        
