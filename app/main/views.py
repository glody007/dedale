from flask import render_template
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
    student = Student.query.filter_by(id=num_id).first()
    if student is None:
        abort(404)
    dico = {'Prenom':'alchemist',
            'Nom':'mbutwile',
            'Post-nom':'lubaba',
            'Ecole': 'Monk',
            'Pourcentage': '100%'}
    return render_template('infostudent.html', student=student)
