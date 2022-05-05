from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    otch = StringField('Отчество', validators=[DataRequired()])
    age = StringField('Возраст', validators=[DataRequired()])
    speciality = StringField('Должность', validators=[DataRequired()])
    education = StringField('Образование', validators=[DataRequired()])
    em = PasswordField('Подтверждение регистрации руководителем студии', validators=[DataRequired()])
    submit = SubmitField('Применить')