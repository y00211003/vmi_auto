from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuthUser(Base):
        __tablename__ = 'auth_user'
        id = Column(Integer, primary_key=True)
        password = Column(String)
        is_superuser = Column(SmallInteger)
        username = Column(String)
        first_name = Column(String)
        last_name = Column(String)
        email = Column(String)
        is_staff = Column(SmallInteger)
        is_active = Column(SmallInteger)
        date_joined = Column(DateTime)

        def __init__(self, user_name, password):
            self.username = user_name
            self.password = password
