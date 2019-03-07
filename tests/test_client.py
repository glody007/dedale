from app import create_app, db
from app.models import User, School
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

        #user not logged in
        reponse_main = self.client.get(url_for('main.index'))
        self.assertFalse('Admin' in reponse_main.get_data(as_text=True))

        #login
        reponse_login = self.login(email=self.user_datas['email'],
                                   password=self.user_datas['password'])
        self.assertTrue('Admin' in reponse_login.get_data(as_text=True))

        #logout
        reponse_logout = self.client.get(url_for('auth.logout'))
        self.assertFalse('Admin' in reponse_logout.get_data(as_text=True))

    def test_shools_administration(self):
        self.login(email=self.user_datas['email'],
                   password=self.user_datas['password'])

        #get school administration page
        reponse = self.client.get(url_for('auth.admin_schools'))
        self.assertTrue('Add school' in reponse.get_data(as_text=True))

        '''check if school's name changes after request to edit_school page
           with edited school datas'''
        edited_school_datas = self.datas['edited_school']
        self.client.post(url_for('auth.edit_school', id=self.datas['school_id']),
                         data=edited_school_datas,
                         follow_redirects=True)
        edited_school = School.\
                        query.\
                        filter_by(name=edited_school_datas['name']).first()
        self.assertTrue(edited_school.name == edited_school_datas['name'])

        '''check if school doesn't exist after request to delete_school page'''
        self.client.get(url_for('auth.delete_school', id=self.datas['school_id']),
                        follow_redirects=True)
        school = School.\
                 query.\
                 filter_by(id=self.datas['school_id']).first()
        self.assertTrue(school == None)
