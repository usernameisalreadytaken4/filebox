from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class CreateFolder(FlaskForm):
    folder_name = StringField('folder_name', validators=[DataRequired()])


class UploadFile(FlaskForm):
    file = FileField(validators=[DataRequired()])


class MoveFile(FlaskForm):
    new_path = StringField('new_path', validators=[DataRequired()])