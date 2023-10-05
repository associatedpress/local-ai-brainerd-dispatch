class Config(object):
    DEBUG = False
    TESTING = False

    DATABASE_NAME = 'DATABASE_NAME'
    DB_USERNAME = 'DB_USERNAME'
    DB_PASSWORD = 'DB_PASSWORD'
    DB_CONFIG = 'AMAZON_AWS_RDS_URI'

class ProductionConfig(Config):
    pass



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

