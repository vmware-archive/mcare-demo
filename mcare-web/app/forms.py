from flask.ext.wtf import Form
from flask import request, session
from wtforms import StringField, SubmitField, DateTimeField, TextField, TextAreaField
from wtforms import PasswordField, HiddenField, SelectField
from wtforms.validators import Length, required
from wtforms.csrf.session import SessionCSRF
from config import config

class BaseForm(Form):
    class Meta:
        csrf = False  # Enable CSRF
        csrf_class = SessionCSRF  # Set the CSRF implementation
        csrf_secret = config['development'].SECRET_KEY
        # Any other CSRF settings here.

        @property
        def csrf_context(self):
            return session

class NameForm(BaseForm):
    #name = StringField('', validators=[Required()])
    submit = SubmitField('Load Database')


class UserForm(BaseForm):
     uname = TextField('UserName', [required()]) 
     password = PasswordField('UserPassword', [required()]) 
     firstname = TextField('FirstName') 
     lastname = TextField('LastName') 
     email = TextField('Email', [required()]) 
     phone = TextField('Phone') 
     kinveyuser = TextField('KinveyUser') 
     kinveypassword = PasswordField('KinveyPassword') 


class CustomerForm(BaseForm):
     
    cname = TextField('Company Name', [required()])
    firstname = TextField('Contact First Name') 
    lastname = TextField('Contact Last Name') 
    email = TextField('Email')
    street = TextField('Street')
    city  = TextField('City')
    state  = SelectField('State', [Length(max=2)])
    postal  = TextField('Postal')
    

class TicketForm(BaseForm):

    ttype = SelectField('Type')
    body = TextAreaField('Description')
    firstname  = TextField('Contact First Name')
    lastname  = TextField('Contact Last Name')
    phone  = TextField('Contact phone')
    cemail  = TextField('Contact email')
    tstate = SelectField(u'Ticket State', choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')])
    tpriority = SelectField('Priority', coerce=int)

class CommentForm(BaseForm):
     
    body = TextAreaField('Description', [required()])
    email = TextField('Contact Email')


class SearchForm(BaseForm):
    key  = TextField('Key')


class LoginForm(BaseForm):
    """Render HTML input for user login form.

    Authentication (i.e. password verification) happens in the view function.
    """
    username = TextField('Username', [required()])
    password = PasswordField('Password', [required()])
   
