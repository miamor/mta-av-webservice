import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mtaav:mtaav@123@localhost:3306/mtaav?charset=utf8'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://noinh:noi123456@14.225.16.247:3306/mtaav'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Noi12345@@localhost:3306/buysharing_new'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
