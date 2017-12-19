from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class App(Base):
    __tablename__ = 'app_app'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    icon = Column(String)
    rating = Column(Float)
    version = Column(String)
    file = Column(String)
    size = Column(Integer)
    package = Column(String)
    schema = Column(String)
    type = Column(Integer)
    launch_number = Column(Integer)

    def __init__(self, name, description):
        self.name = name
        self.description = description
