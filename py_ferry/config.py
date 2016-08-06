import os

class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/py-ferry"
    DEBUG = True
    SECRET_KEY = os.environ.get('BLOGFUL_SECRET_KEY', os.urandom(12))
    JWT_AUTH_URL_RULE = '/api/auth'

class TestingConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/py-ferry-test"
    DEBUG = False
    SECRET_KEY = 'Not secret'
    JWT_AUTH_URL_RULE = '/api/auth'
    
class TravisConfig(object):
    DATABASE_URI = "postgresql://localhost:5432/py-ferry-test"
    DEBUG = False
    SECRET_KEY = 'Not secret'
    JWT_AUTH_URL_RULE = '/api/auth'
