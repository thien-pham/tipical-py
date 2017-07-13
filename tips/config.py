import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://dev:Obelixbdf0428!@localhost:5432/tips"
    DEBUG = True

# class TestingConfig(object):
#     DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/posts-test"
#     DEBUG = True
