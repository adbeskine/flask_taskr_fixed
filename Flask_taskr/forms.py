from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class AddTaskForm(Form):
	task_id = IntegerField()
	name = StringField('Task Name', validators=[DataRequired()])
	due_date = DateField('Date Due (mm/dd/yy)', validators=[DataRequired()], format='%m/%d/%y')
	priority = SelectField(
		'Priority', validators=[DataRequired()],
		choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')])
	status = IntegerField('Status')

class RegisterForm(Form):
	email = StringField('email', validators=[DataRequired(), Length(min=6, max=25), Email()])
	username = StringField('username', validators=[DataRequired(), Length(min=6, max=25)])
	password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])