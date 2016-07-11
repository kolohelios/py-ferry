class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/py-ferry"
    DEBUG = True

class TestingConfig(object):
    DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/py-ferry-test"
    DEBUG = False
