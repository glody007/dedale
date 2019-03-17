from .authentification import auth
from .decorateurs import permission_requise
from ..models import Student, Permission
from flask import url_for, jsonify, request
from .. import db
from . import api

@api.route('/student/<int:id>')
@auth.login_required
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_json())

@api.route('/students/')
@auth.login_required
@permission_requise(Permission.AJOUTER_ETUDIANT)
def get_students():
    students = Student.query.all()
    return jsonify({'students': [student.to_json() for student in students]})

@api.route('/students/', methods=['POST'])
@auth.login_required
@permission_requise(Permission.AJOUTER_ETUDIANT)
def new_student():
    student = Student.from_json(request.json)
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_json()), 201,\
           {'Location': url_for('api.get_student', id=student.id, _external=True)}

@api.route('/students/<int:id>', methods=['PUT'])
@auth.login_required
@permission_requise(Permission.MODIFIER_ETUDIANT)
def edit_student(id):
    student = Student.query.get_or_404(id)
    new_student = Student.from_json(request.json)
    student.update_student(new_student)
    return jsonify(student.to_json()), 201,\
           {'Location': url_for('api.get_student', id=student.id, _external=True)}
