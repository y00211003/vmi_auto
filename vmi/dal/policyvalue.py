from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PolicyValue(Base):
    __tablename__ = 'policy_policyvalue'
    id = Column(Integer, primary_key=True)
    policy_id = Column(Integer)
    value = Column(Text)
    detail = Column(Text)

    def __init__(self, policy_id):
        self.policy_id = policy_id
