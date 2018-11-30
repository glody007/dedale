from flask import render_template, flash, redirect, url_for
from . import auth
from .forms import AddStudentForm, registered_student

@auth.route('/admin/schools')
def admin_schools():
    from ..models import School

@auth.route('/admin/students', methods=['GET', 'POST'])
def admin_students():
    from ..models import Student, School
    from .. import db
    form = AddStudentForm()
    registered = registered_student(form)

    if form.validate_on_submit() and not registered:
        school = School.query.first()
        student = Student(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          forename=form.forename.data,
                          birth=form.birth.data,
                          school_id=1,
                          sex=form.sex.data)
        db.session.add(student)
        db.session.commit()

        flash('New user added.')
        return redirect(url_for('auth.admin_students'))

    students = Student.query.all()
    return render_template('students.html', students=students, form=form)

@auth.route('/admin/students/delete/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    from ..models import Student
    from .. import db

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('auth.admin_students'))

@auth.route('/admin/students/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    from ..models import Student
    from .. import db

    student = Student.query.get_or_404(id)
    form = AddStudentForm()
    registered = registered_student(form)

    if form.validate_on_submit() and not registered:
        student.first_name = form.first_name.data
        student.last_name  = form.last_name.data
        student.forename   = form.forename.data
        student.sex        = form.sex.data
        student.birth      = form.birth.data

        db.session.add(student)
        db.session.commit()
        return redirect(url_for('auth.admin_students'))

    form.first_name.data = student.first_name
    form.last_name.data  = student.last_name
    form.forename.data   = student.forename
    form.sex.data        = student.sex
    form.birth           = student.birth
    return render_template('update_student.html', form=form)


@auth.route('/admin/download')
def admin_download():
    from ..models import Student
    students = Student.query.all()

    return render_template('download.html', students=students)
