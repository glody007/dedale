from app import create_app, db
from app.models import User, Role
from flask import url_for
from . import FlaskBaseTestCase

class FlaskClientTestCase(FlaskBaseTestCase):

    def setUp(self):
        FlaskBaseTestCase.setUp(self)

    def login(self, email='', password=''):
        reponse = self.client.post(url_for('auth.login'), data={
            'email': email,
            'password': password
        }, follow_redirects=True)
        return reponse

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('solution' in response.get_data(as_text=True))

    def test_login_logout(self):
        user_data = self.default_user_data

        #user not logged in
        reponse = self.client.get(url_for('main.index'))
        self.assertFalse('Admin' in reponse.get_data(as_text=True))

        #login
        reponse = self.login(email=user_data['email'],
                             password=user_data['password'])
        self.assertTrue('Admin' in reponse.get_data(as_text=True))

        #logout
        reponse = self.client.get(url_for('auth.logout'))
        self.assertFalse('Admin' in reponse.get_data(as_text=True))

    def test_shools_administration(self):
        self.default_user_data['role_name'] = 'Guru'
        self.login(email=self.default_user_data['email'],
                   password=self.default_user_data['password'])

        reponse = self.client.get(url_for('auth.admin_schools'))
        self.assertTrue('Add school' in reponse.get_data(as_text=True))
