from . import api
from .authentification import auth
from ..models import School

@api.route('/school/<int:id>')
def get_school(id):
    school = School.query.get_or_404(id)
    return jsonify(school.to_json())

@api.route('/schools')
def get_schools():
    schools = School.query.all()
    return jsonify({'schools': [school.to_json() for school in schools]})
