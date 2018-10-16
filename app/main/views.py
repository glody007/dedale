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
    dico = {'Prenom':'alchemist',
            'Nom':'mbutwile',
            'Post-nom':'lubaba',
            'Ecole': 'Monk',
            'Pourcentage': '100%'}
    return render_template('infostudent.html', student=student)
