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
    DATAS = {
            'user' : {'email' : 'nagato@dedale.xyz',
                      'password' : '12345678',
                      'role_name' : 'Guru'},

            'school' : {'name' : 'konoha',
                        'state' : 'mangas',
                        'city' : 'sereitei',
                        'street_name' : 'yamamoto',
                        'email' : 'kushiki@biakuya.com'},

            'edited_school' : {'name' : 'gottam',
                               'state' : 'comics',
                               'city' : 'sereitei',
                               'street_name' : 'yamamoto',
                               'email' : 'kushiki@biakuya.com'},
            'school_id' : None,

            'student_id' : None,

            'student' : {'first_name' : 'lubaba',
                         'last_name' : 'mbutwile',
                         'forename' : 'dyglo',
                         'sex' : 'M'},

            'edited_student' : {'first_name' : 'richard',
                                'last_name' : 'dawkins',
                                'forename' : 'light',
                                'sex' : 'M'}
            }

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
