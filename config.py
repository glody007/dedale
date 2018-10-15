import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    print SQLALCHEMY_DATABASE_URI
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
        username     = "glody",
        password     = "dedale118",
        hostname     = "glody.mysql.pythonanywhere-services.com",
        databasename = "glody$school",
    )

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,

    'default' : DevelopmentConfig
}
