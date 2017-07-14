import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://dev:Obelixbdf0428!@localhost:5432/tips"
    DEBUG = True
    SECRET_KEY = os.environ.get("TIPICAL_SECRET_KEY", os.urandom(12))

# class TestingConfig(object):
#     DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/posts-test"
#     DEBUG = True
