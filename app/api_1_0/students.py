from . import api
from .authentification import auth
from ..models import Student

@api.route('/student/<int:id>')
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_json())

@api.route('/students')
def get_schools():
    students = Student.query.all()
    return jsonify({'students': [student.to_json() for student in students]})
