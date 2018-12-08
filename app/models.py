from . import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash,\
                              check_password_hash
from . import login_manager

class AdminSchool(UserMixin, db.Model):
    __tablename__ = 'AdminSchools'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    username = db.Column(db.String(32), nullable = True)
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count = 100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        school_count = School.query.count()
        for i in range(count):
            randschool = School.query.offset(randint(0, school_count - 1)).first()
            admin = AdminSchool(email = forgery_py.internet.email_address(),
                                username = forgery_py.internet.user_name(),
                                password_hash = forgery_py.lorem_ipsum.word(),
                                school = randschool)
            db.session.add(admin)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<AdminSchool {email}>'.format(email = self.email)

@login_manager.user_loader
def load_admin(admin_id):
    return AdminSchool.query.get(int(admin_id))

class Student(db.Model):
    __tablename__ = 'students'
    #composite UniqueConstraint de first_name last_name forename sex birth school_id
    __table_args__ = tuple(UniqueConstraint('first_name', 'last_name', 'forename',
                           'sex', 'birth', 'school_id', name='student_unique_constraint'))

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(15), index = True)
    last_name = db.Column(db.String(15), index = True)
    forename = db.Column(db.String(15), index = True)
    sex = db.Column(db.String(1), index = True)
    birth = db.Column(db.Date)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    @staticmethod
    def generate_fake(count = 1000):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        school_count = School.query.count()
        for i in range(count):
            randschool = School.query.offset(randint(0, school_count - 1)).first()
            student = Student(first_name = forgery_py.name.first_name(),
                              last_name = forgery_py.name.last_name(),
                              forename = forgery_py.name.first_name(),
                              sex = forgery_py.personal.abbreviated_gender(),
                              birth = forgery_py.date.date(past = True, min_delta = 1000, max_delta = 7300),
                              school = randschool)
            db.session.add(student)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<Eleve {first_name} {last_name} {forename}>'.format(first_name = self.first_name,
                last_name = self.last_name,forename = self.forename)

class School(db.Model):
    __tablename__ = 'schools'
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    name = db.Column(db.String(20), index = True)
    state = db.Column(db.String(20), index = True)
    city = db.Column(db.String(20), index = True)
    street_name = db.Column(db.String(20), index = True)
    #number = db.Column(db.Integer)
    students = db.relationship('Student', backref = 'school', lazy = 'dynamic')
    admins = db.relationship('AdminSchool', backref = 'school', lazy = 'dynamic')

    @staticmethod
    def generate_fake(count = 100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            school = School(email = forgery_py.internet.email_address(),
                            name = forgery_py.name.company_name(),
                            state = forgery_py.address.state(),
                            city = forgery_py.address.city(),
                            street_name = forgery_py.address.street_name())
            db.session.add(school)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<School {name}>'.format(name = self.name)

'''take list that contain dictionaries of student's datas
   add students to database'''
def add_students_from_dicos(students_datas):
    from sqlalchemy.exc import IntegrityError

    students = []
    for student_datas in students_datas:
        student = Student(first_name=students_datas['first_name'],
                          last_name=student_datas['last_name'],
                          forename=student_datas['forename'],
                          school_id=student_datas['school_id'],
                          sex=student_datas['sex'])
        students.append(student)

    db.session.add_all(students)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

'''take list of students and generate list of
   dictionaries containing datas of students'''
def from_students_of_school_to_dicos(school_id):

    school = School.query.get(school_id)
    students = school.students
    students_datas = []
    for student in students:
        students_datas.append({'first_name' : student.first_name,
                              'last_name' : student.last_name,
                              'forename' : student.forename,
                              'sex' : student.sex})
    return students_datas
