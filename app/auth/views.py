from flask import render_template, flash, redirect, url_for, request, send_file, current_app
from . import auth
from .forms import AddStudentForm, AddSchoolForm, registered_student, LoginForm
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
import os

@auth.route('/login', methods=['GET', 'POST'])
def login():
    from ..models import AdminSchool
    form = LoginForm()
    if form.validate_on_submit():
        admin_school = AdminSchool.query.filter_by(email=form.email.data).first()
        if admin_school is not None and admin_school.verify_password(form.password.data):
            login_user(admin_school, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.admin_schools'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth.route('/schools', methods=['GET', 'POST'])
@login_required
def admin_schools():
    from ..models import School
    from .. import db

    form = AddSchoolForm()

    if form.validate_on_submit():
        school = School(email=form.email.data,
                        name=form.name.data,
                        state=form.state.data,
                        city=form.city.data,
                        street_name=form.street_name.data,)
        db.session.add(school)
        db.session.commit()

    schools = School.query.all()
    return render_template('schools.html', schools=schools,
                            school_id=1, form=form)

@auth.route('/school/delete/<int:id>', methods=['GET'])
@login_required
def delete_school(id):
    from ..models import School
    from .. import db

    school = School.query.get_or_404(id)
    db.session.delete(school)
    db.session.commit()

    return redirect(url_for('auth.admin_schools'))

@auth.route('/school/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_school(id):
    from ..models import School
    from .. import db

    school = School.query.get_or_404(id)
    form = AddSchoolForm()

    if form.validate_on_submit():
        school.email       = form.email.data
        school.name        = form.name.data
        school.state       = form.state.data
        school.city        = form.city.data
        school.street_name = form.street_name.data

        db.session.add(school)
        db.session.commit()
        return redirect(url_for('auth.admin_schools'))

    form.email.data       = school.email
    form.name.data        = school.name
    form.state.data       = school.state
    form.city.data        = school.city
    form.street_name.data = school.street_name
    return render_template('update_school.html', form=form)

@auth.route('/schools/<int:id>', methods=['GET', 'POST'])
@login_required
def school_students(id):
    from ..models import Student, School
    school = School.query.get_or_404(id)
    form = AddStudentForm()

    students =  school.students
    return render_template('students.html', students=students, form=form, school_id=id)

@auth.route('/school/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_students(id):
    from ..models import Student, School
    from .. import db

    school = School.query.get_or_404(id)
    form = AddStudentForm()
    registered = registered_student(form)

    if form.validate_on_submit() and not registered:
        student = Student(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          forename=form.forename.data,
                          birth=form.birth.data,
                          school_id=id,
                          sex=form.sex.data)
        db.session.add(student)
        db.session.commit()

        flash('New user added.')
        return redirect(url_for('auth.admin_students', id=id, _external=True))

    students = school.students
    return render_template('students.html', students=students, form=form, school_id=id)

@auth.route('/students/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_student(id):
    from ..models import Student
    from .. import db

    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()

    return redirect(url_for('auth.admin_students', id=student.school_id, _external=True))

@auth.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('auth.admin_students', id=student.school_id, _external=True))

    form.first_name.data = student.first_name
    form.last_name.data  = student.last_name
    form.forename.data   = student.forename
    form.sex.data        = student.sex
    form.birth           = student.birth
    return render_template('update_student.html', form=form)

@auth.route('/file-download/<int:id>')
@login_required
def download_file(id):
    from ..models import School
    from ..qr_in_pdf import addQrInPdfFromDatas
    from ..url_map import string_from_num
    taille_qr = (100, 100)
    #take all students from given school id
    #create list of custom ids from their database ids
    students = School.query.get_or_404(id).students
    datas = []
    for student in students:
        custom_id = string_from_num(str(student.id))
        main = 'http://www.dedale.xyz/student/' + str(student.id)
        data = {'main' : main, 'info' : student.first_name}
        datas.append(data)
    #create file path from download folder and file name
    #file name is school id concat with .pdf
    download_folder = current_app.config['UPLOAD_FOLDER']
    file_name = str(id) + '.pdf'
    file_path = download_folder + '/' + file_name
    #create pdf file with qrcodes from list of custom id
    addQrInPdfFromDatas(datas, taille_qr, file_path)
    try:
        return send_file(file_path, attachment_filename=file_name)
    except Exception as e:
        return str(e)

def allowed_file(filename):
    allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@auth.route('/file-upload/<int:id>', methods=['POST'])
@login_required
def upload_file(id):
    from ..excel_import import ExcelDataExtractor
    from ..models import Student, add_students_to_school_from_dicos

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(id) + file.filename)
            upload_folder_name = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_folder_name)
            #import students data from file
            #create list of dicos from those datas
            xlsxToList = ExcelDataExtractor(upload_folder_name)
            students_dicos = xlsxToList.getStudents()
            #add students to database from dicos
            add_students_to_school_from_dicos(students_dicos, id)

            return redirect(url_for('auth.admin_students', id=id, _external=True))
