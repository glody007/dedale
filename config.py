import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(os.path.dirname(__file__))
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SECRET_KEY = "mysecretkey"
    UPLOAD_FOLDER = '/tmp'
    ALLOWED_EXTENSIONS = set(['xlsx'])

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.db')
    DEBUG = True

class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
