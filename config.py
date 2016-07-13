import os


basedir = os.path.abspath(os.path.dirname(__file__))

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p
        )
    )

class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_PRODUCTION_DATABASE_URI'
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + mkpath('../myapp.db')
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     'APP_DEVELOPMENT_DATABASE_URI'
    # )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'APP_TESTING_DATABASE_URI'
    )


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
