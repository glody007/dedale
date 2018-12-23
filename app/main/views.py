from flask import render_template, abort
from . import main

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/student/<id>')
def student(id):
    from ..models import Student
    from ..url_map import num_from_string
    num_id = int(num_from_string(id))
    num_id -= 12345
    student = Student.query.filter_by(id=id).first()
    if student is None:
        abort(404)

    return render_template('infostudent.html', student=student)
