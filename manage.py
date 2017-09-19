import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(10), index=True, unique=True)
    password = db.Column(db.String(20))
    folder_list = db.relationship('Folder', backref='owner', lazy='dynamic')
    file_list = db.relationship('File', backref='owner', lazy='dynamic')


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(128), index=True)
    inner_link = db.Column(db.String(1024), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    parent = db.Column(db.String(64))
    url = db.Column(db.String(1024))
    path = db.Column(db.String(1024))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file = db.relationship('File', backref='folder', lazy='dynamic')


if __name__ == '__main__':
    manager.run()
