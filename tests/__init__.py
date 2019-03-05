import unittest
from app import create_app, db
from app.models import User, Role

class FlaskBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.inserer_roles()
        self.client = self.app.test_client(use_cookies=True)
        self.default_user_data = {'email' : 'nagato@dedale.xyz',
                                  'password' : '12345678',
                                  'role_name' : 'Guru'}
        self.add_user_to_db(self.default_user_data)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_user_to_db(self, user_data):
        user = User(email=user_data['email'])
        user.password = user_data['password']
        role = Role.query.filter_by(nom=user_data['role_name']).first()
        user.role = role
        db.session.add(user)
        db.session.commit()
