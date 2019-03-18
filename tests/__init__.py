import unittest
from sqlalchemy.exc import IntegrityError
from app import create_app, db
from app.models import User, School, Student, Role
from app.utils import create_object_from_dico

class FlaskBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.inserer_roles()
        self.datas = self.app.config['DATAS']
        self.user_datas = self.datas['user']
        self.school_datas = self.datas['school']
        self.student_datas = self.datas['student']
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def add_test_datas_to_db(self):
        user = self.create_user()
        school = self.create_school()
        student = self.create_student(school)
        db.session.add_all([user, school, student])
        try:
            db.session.commit()
            self.datas['school_id'] = school.id
            self.datas['student_id'] = student.id
        except IntegrityError:
            db.session.rollback()

    def create_user(self):
        user = User(email=self.user_datas['email'])
        user.password = self.user_datas['password']
        role = Role.query.filter_by(nom=self.user_datas['role_name']).first()
        user.role = role
        return user

    def create_school(self):
        school = create_object_from_dico(School, self.school_datas)
        return school

    def create_student(self, school):
        student = Student(first_name=self.student_datas['first_name'],
                          last_name=self.student_datas['last_name'],
                          forename=self.student_datas['forename'],
                          sex=self.student_datas['sex'])
        student.school = school
        return student
