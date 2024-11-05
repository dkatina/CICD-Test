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
    pass