from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField,\
                    RadioField, ValidationError
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length

class AddStudentForm(Form):
    first_name = StringField('Nom', validators=[Required(), Length(1, 15)])
    last_name = StringField('Post-nom', validators=[Required(), Length(1, 15)])
    forename = StringField('Forename', validators=[Required(), Length(1, 15)])
    birth = DateField('Date de naissance')
    sex = RadioField('Sex', choices=[('F', 'Female'), ('M', 'Male')], validators=[Required()])
    submit = SubmitField('Envoyer')

def registered_student(form):
    from ..models import Student
    registered = Student.query.filter_by(first_name=form.first_name.data).\
                               filter_by(last_name=form.last_name.data).\
                               filter_by(forename=form.forename.data).\
                               first()
    if registered:
        return True
    else:
        return False

class AddSchoolForm(Form):
    name  = StringField('Nom', validators=[Required(), Length(1, 20)])
    state = StringField('Pays', validators=[Required(), Length(1, 20)])
    city  = StringField('Ville', validators=[Required(), Length(1, 20)])
    street_name = StringField('Avenue', validators=[Required(), Length(1, 20)])
    email = StringField('Email', validators=[Required()])
    submit = SubmitField('Envoyer')
