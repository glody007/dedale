from . import db
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,\
                              check_password_hash
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort, current_app, url_for
from .exceptions import ValidationError

class Permission:
    AJOUTER_ETUDIANT = 0x01
    SUPPRIMER_ETUDIANT = 0x02
    MODIFIER_ETUDIANT = 0x04
    AJOUTER_ECOLE = 0x08
    MODIFIER_ECOLE  = 0x10
    SUPPRIMER_ECOLE = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def inserer_roles():
        roles = {
            'Utilisateur': (Permission.AJOUTER_ETUDIANT |
                            Permission.MODIFIER_ETUDIANT),
            'Moderateur': (Permission.AJOUTER_ETUDIANT |
                           Permission.MODIFIER_ETUDIANT |
                           Permission.SUPPRIMER_ETUDIANT),
            'Moine': (Permission.AJOUTER_ETUDIANT |
                      Permission.MODIFIER_ETUDIANT |
                      Permission.AJOUTER_ECOLE |
                      Permission.MODIFIER_ECOLE),
            'Guru': (0xff)
        }
        for r in roles:
            role = Role.query.filter_by(nom=r).first()
            if role is None:
                role = Role(nom=r)
            role.permissions = roles[r]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role {nom}>'.format(nom = self.nom)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    username = db.Column(db.String(32), nullable = True)
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def peut(self, permissions):
        return self.role is not None and\
            (self.role.permissions & permissions) == permissions

    def est_guru(self):
        return self.peut(Permission.SUPPRIMER_ECOLE)

    def est_moine(self):
        return self.peut(Permission.MODIFIER_ECOLE)

    def peut_acceder_ou_403(self, school_id):
        guru = self.est_guru()
        moine = self.est_moine()
        if not guru and not moine and self.school_id != school_id:
            abort(403)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                        expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    @staticmethod
    def generate_fake(count = 100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        school_count = School.query.count()
        for i in range(count):
            randschool = School.query.offset(randint(0, school_count - 1)).first()
            admin = User(email = forgery_py.internet.email_address(),
                                username = forgery_py.internet.user_name(),
                                password_hash = forgery_py.lorem_ipsum.word(),
                                school = randschool)
            db.session.add(admin)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User {email}>'.format(email = self.email)

@login_manager.user_loader
def load_admin(admin_id):
    return User.query.get(int(admin_id))

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
    Departement_id = db.Column(db.Integer, db.ForeignKey('departements.id'))
    Promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))
    pourcentage = db.Column(db.Integer, index = True)

    @staticmethod
    def from_json(json_student):
        first_name = json_student.get('first_name')
        last_name = json_student.get('last_name')
        forename = json_student.get('forename')
        sex = json_student.get('sex')
        birth = json_student.get('birth')
        pourcentage = json_student.get('pourcentage')
        if is_none_or_empty(first_name) or is_none_or_empty(last_name) or\
           is_none_or_empty(forename) or is_none_or_empty(sex) or\
           is_none_or_empty(pourcentage):
           raise ValidationError('one field is empty')
        return Student(first_name=first_name, last_name=last_name,
                        forename=forename, sex=sex, birth=birth,
                        pourcentage=pourcentage)

    def to_json(self):
        school_url = ""
        if self.school_id is not None:
            school_url = url_for('api.get_school', id=school_id, _external=True)

        json_student = {
            'url': url_for('api.get_student', id=self.id, _external=True),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'forename': self.forename,
            'sex': self.sex,
            'birth': self.birth,
            'pourcentage': self.pourcentage,
            'school': school_url
        }
        return json_student

    def update_student(self, new_student):
        self.first_name = new_student.first_name
        self.last_name = new_student.last_name
        self.forename = new_student.forename
        self.sex = new_student.sex
        self.birth = new_student.birth
        self.pourcentage = new_student.pourcentage
        db.session.add(self)
        db.session.commit()

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

class Departement(db.Model):
    __tablename__ = 'departements'
    id = db.Column(db.Integer, primary_key = True)
    nom = db.Column(db.String(64), unique = True, index = True)
    students = db.relationship('Student', backref = 'departement', lazy = 'dynamic')

    def __repr__(self):
        return '<Departement {nom}>'.format(classe = self.nom)

class Promotion(db.Model):
    __tablename__ = 'promotions'
    id = db.Column(db.Integer, primary_key = True)
    niveau = db.Column(db.Integer, unique = True, index = True)
    students = db.relationship('Student', backref = 'promotion', lazy = 'dynamic')

    def __repr__(self):
        return '<Promotion {niveau}>'.format(classe = self.niveau)

class School(db.Model):
    __tablename__ = 'schools'
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    name = db.Column(db.String(20), index = True)
    state = db.Column(db.String(20), index = True)
    city = db.Column(db.String(20), index = True)
    street_name = db.Column(db.String(20), index = True)
    students = db.relationship('Student', backref = 'school', lazy = 'dynamic')
    admins = db.relationship('User', backref = 'school', lazy = 'dynamic')

    @staticmethod
    def from_json(json_school):
        name = json_school.get('name')
        email = json_school.get('email')
        state = json_school.get('state')
        city = json_school.get('city')
        street_name = json_school.get('street_name')
        if is_none_or_empty(name) or is_none_or_empty(email) or\
           is_none_or_empty(state) or is_none_or_empty(city) or\
           is_none_or_empty(street_name):
           raise ValidationError('one field is empty')
        return School(name=name, email=email, state=state,
                      city=city, street_name=street_name)

    def to_json(self):
        json_school = {
            'url': url_for('api.get_school', id=self.id, _external=True),
            'name': self.name,
            'email': self.email,
            'state': self.state,
            'city': self.city,
            'street_name': self.street_name,
            'students': url_for('api.get_school_students', id=self.id, _external=True)
        }
        return json_school

    def update_school(self, new_school):
        self.name = new_school.name
        self.email = new_school.email
        self.state = new_school.state
        self.city = new_school.city
        self.street_name = new_school.street_name
        db.session.add(self)
        db.session.commit()

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
def add_students_to_school_from_dicos(students_datas, school_id):
    from sqlalchemy.exc import IntegrityError

    students = []
    for student_datas in students_datas:
        student = Student(first_name=student_datas['first_name'],
                          last_name=student_datas['last_name'],
                          forename=student_datas['forename'],
                          school_id=school_id,
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

def is_none_or_empty(string):
    if string is None or string == '':
        return True
    return False
