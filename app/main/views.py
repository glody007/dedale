from flask import render_template
from . import main

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/student/<id>')
def student(id):
    from ..models import Student
    student = Student.query.filter_by(id=int(id)).first()
    if student is None:
        abort(404)
    return render_template('infostudent.html', name=student.first_name)
