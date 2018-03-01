from . import db
from flask_login import UserMixin

class AdminSchool(UserMixin, db.Model):
    __tablename__ = 'AdminSchools'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    username = db.Column(db.String(32), nullable = True)
    password_hash = db.Column(db.String(128))
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    def __repr__(self):
        return '<AdminSchool {email}>'.format(email = self.email)

class Student(db.Model):
    __tablename__ = 'students'
    __table_args__ = tuple(UniqueConstraint('first_name', 'last_name', 'forename',
                           'sex', 'birth', 'school_id', name='student_unique_constraint'))
                           
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(15), index = True)
    last_name = db.Column(db.String(15), index = True)
    forename = db.Column(db.String(15), index = True)
    sex = db.Column(db.String(1), index = True)
    birth = db.Column(db.Date)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'))

    def __repr__(self):
        return '<Eleve {first_name} {last_name} {forename}>'.format(first_name = self.first_name,
                last_name = self.last_name,forename = self.forename)

class School(db.Model):
    __tablename__ = 'schools'
    id  = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    name = db.Column(db.String(20), index = True)
    country = db.Column(db.String(20), index = True)
    town = db.Column(db.String(20), index = True)
    street = db.Column(db.String(20), index = True)
    #number = db.Column(db.Integer)
    students = db.relationship('Student', backref = 'school', lazy = 'dynamic')
    admins = db.relationship('AdminSchool', backref = 'school', lazy = 'dynamic')

    def __repr__(self):
        return '<School {name}>'.format(name = self.name)
