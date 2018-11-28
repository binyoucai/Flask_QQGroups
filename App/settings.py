import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_uri(dbinifo):
    engine = dbinifo.get('ENGINE') or 'sqlite'
    driver = dbinifo.get('DRIVER') or 'sqlite'
    user = dbinifo.get('USER') or ''
    password = dbinifo.get('PASSWORD') or ''
    host = dbinifo.get('HOST') or ''
    port = dbinifo.get('PORT') or ''
    name = dbinifo.get('NAME') or ''
    return '{}+{}://{}:{}@{}:{}/{}'.format(engine, driver, user, password, host, port, name)


class Config:
    DEBUG = False

    TESTIG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'sfdsfdsfdsf'


class DevelopConfig(Config):
    DEBUG = True

    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'qq8455682',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask_taopiaopiao'
    }

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PROT = 25
    MAIL_USERNAME =  'rongjiawei1204@163.com'
    MAIL_PASSWORD = 'Rock1204'
    MAIL_DEFAULT_SENDER =MAIL_USERNAME


    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    DEBUG = True

    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'qq8455682',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'qq8455682',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'qq8455682',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'flask'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    'develop': DevelopConfig,
    'testing': TestConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig

}