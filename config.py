import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///example.db"
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = 'SimpleCache'