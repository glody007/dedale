from . import FlaskBaseTestCase
from flask import url_for
from base64 import b64encode
import json
from app.utils import dict_contient
from app.models import School
from app import db

class APITestCase(FlaskBaseTestCase):

    def setUp(self):
        FlaskBaseTestCase.setUp(self)
        self.client = self.app.test_client(use_cookies=False)
        db.session.add(self.create_user())
        db.session.commit()

    def get_api_headers(self, username, password):
        return {
                'Authorization':
                'Basic ' + b64encode(
                        (username + ':' + password).encode('utf-8')).decode('utf-8'),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                }

    def test_no_auth(self):
        reponse = self.client.get(url_for('api.get_students'),
                                   content_type='application/json')
        self.assertTrue(reponse.status_code == 401)

    def test_schools(self):
        #add new school
        rep_post_school = self.client.post(
            url_for('api.new_school'),
            data=json.dumps(self.school_datas),
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_post_school.status_code == 201, "doesn't add new school")
        url_new_school = rep_post_school.headers.get('Location')

        #get new school
        rep_get_school = self.client.get(
            url_new_school,
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_get_school.status_code == 200, "doesn't get school")

        json_reponse = json.loads(rep_get_school.data.decode('utf-8'))
        school_datas_in_json_reponse = dict_contient(json_reponse, self.school_datas)
        self.assertTrue(school_datas_in_json_reponse)

        #modify new school
        edited_school_datas = self.datas['edited_school']
        rep_put_school = self.client.put(
            url_for('api.edit_school', id=1),
            data=json.dumps(edited_school_datas),
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_post_school.status_code == 201, "doesn't put school")
        url_edited_school = rep_post_school.headers.get('Location')

        #get edited school
        rep_get_school = self.client.get(
            url_edited_school,
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_get_school.status_code == 200, "doesn't get edited school")

        json_reponse = json.loads(rep_get_school.data.decode('utf-8'))
        edited_school_datas_in_json_reponse = dict_contient(json_reponse,
                                                            edited_school_datas)
        self.assertTrue(edited_school_datas_in_json_reponse)

    def test_students(self):
        #add new student
        rep_post_student = self.client.post(
            url_for('api.new_student'),
            data=json.dumps(self.student_datas),
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_post_student.status_code == 201, "doesn't add new student")
        url_new_student = rep_post_student.headers.get('Location')

        #get new student
        rep_get_student = self.client.get(
            url_new_student,
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_get_student.status_code == 200, "doesn't get student")

        json_reponse = json.loads(rep_get_student.data.decode('utf-8'))
        student_datas_in_json_reponse = dict_contient(json_reponse, self.student_datas)
        self.assertTrue(student_datas_in_json_reponse)

        #modify new student
        edited_student_datas = self.datas['edited_student']
        rep_put_student = self.client.put(
            url_for('api.edit_student', id=1),
            data=json.dumps(edited_student_datas),
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_post_student.status_code == 201, "doesn't put student")
        url_edited_student = rep_post_student.headers.get('Location')

        #get edited student
        rep_get_student = self.client.get(
            url_edited_student,
            headers=self.get_api_headers(self.user_datas['email'],
                                         self.user_datas['password']))
        self.assertTrue(rep_get_student.status_code == 200, "doesn't get edited student")

        json_reponse = json.loads(rep_get_student.data.decode('utf-8'))
        edited_student_datas_in_json_reponse = dict_contient(json_reponse,
                                                            edited_student_datas)
        self.assertTrue(edited_student_datas_in_json_reponse)
