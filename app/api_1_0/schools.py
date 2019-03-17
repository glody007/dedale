from .authentification import auth
from .decorateurs import permission_requise
from ..models import School, Permission
from flask import url_for, jsonify, request
from .. import db
from . import api

@api.route('/school/<int:id>')
@auth.login_required
def get_school(id):
    school = School.query.get_or_404(id)
    return jsonify(school.to_json())

@api.route('/schools/')
@auth.login_required
@permission_requise(Permission.AJOUTER_ECOLE)
def get_schools():
    schools = School.query.all()
    return jsonify({'schools': [school.to_json() for school in schools]})

@api.route('/school_studtents/<int:id>')
@auth.login_required
@permission_requise(Permission.AJOUTER_ECOLE)
def get_school_students(id):
    students = School.query.get_or_404(id).students
    return jsonify({'students': [student.to_json() for student in students]})

@api.route('/schools/', methods=['POST'])
@auth.login_required
@permission_requise(Permission.AJOUTER_ECOLE)
def new_school():
    school = School.from_json(request.json)
    db.session.add(school)
    db.session.commit()
    return jsonify(school.to_json()), 201,\
           {'Location': url_for('api.get_school', id=school.id, _external=True)}

@api.route('/schools/<int:id>', methods=['PUT'])
@auth.login_required
@permission_requise(Permission.MODIFIER_ECOLE)
def edit_school(id):
    school = School.query.get_or_404(id)
    new_school = School.from_json(request.json)
    school.update_school(new_school)
    return jsonify(school.to_json()), 201,\
           {'Location': url_for('api.get_school', id=school.id, _external=True)}
