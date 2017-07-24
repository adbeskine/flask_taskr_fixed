# users.forms

from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email



class RegisterForm(Form):
	email = StringField('email', validators=[DataRequired(), Length(min=6, max=25), Email()])
	username = StringField('username', validators=[DataRequired(), Length(min=6, max=25)])
	password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])