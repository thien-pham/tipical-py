from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, AnonymousUserMixin, LoginManager
import datetime
from geoalchemy2 import *
from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from tips import app
# from database import Base, engine

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# from .database import Base

class Tip(Base):
    __tablename__ = "tips"

    id = Column(Integer, primary_key=True)
    title = Column(String(128))
    body = Column(String(1024))
    datetime = Column(DateTime, default=datetime.datetime.now)
    author_id = Column(Integer, ForeignKey('users.id'))
    # location = Column(Geography(geometry_type='POINT', srid=4326))
    # TODO: add in location

    # def as_dictionary(self):
    #     tip = {
    #         "id": self.id,
    #         "title": self.title,
    #         "body": self.body
    #         # "location": self.location
    #     }
    #     return tip

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))
    tips = relationship("Tip", backref="author")

# class Anonymous(Base, AnonymousUserMixin):
#   def __init__(self):
#     self.username = 'Guest'
#
# login_manager = LoginManager(app)
# login_manager.anonymous_user = AnonymousUser

Base.metadata.create_all(engine)
