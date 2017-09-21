from app import db, lm
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
import os


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(10), index=True, unique=True)
    password = db.Column(db.String(20))
    folder_list = db.relationship('Folder', backref='owner', lazy='dynamic')
    file_list = db.relationship('File', backref='owner', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    @lm.user_loader
    def load_user(self):
        return User.query.get(self)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(128), index=True)
    inner_link = db.Column(db.String(1024), index=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))

    @staticmethod
    def upload_file(file, folder, user):
        filename = secure_filename(file.filename)
        inner_name = f'{str(folder)}-{str(user)}-{filename}'
        file.save(os.path.join(UPLOAD_FOLDER, inner_name))
        db_file = File(file_name=filename, owner_id=user, folder_id=folder, inner_link=inner_name)
        db.session.add(db_file)
        db.session.commit()
        return inner_name

    @staticmethod
    def move_file(inner_name, new_path):
        file = File.query.filter_by(inner_link=inner_name).first()
        old_path = inner_name
        inner_link = f'{str(new_path)}-{str(user)}-{filename}'
        os.rename(old_path, inner_link)
        db.query(file).update({'folder_id': new_path}, {'inner_link': inner_link})
        db.session.commit()
      #  return True

   # @staticmethod
    #def download_file():
     #   pass

    @staticmethod
    def delete_file(inner_name, user_id):
        file = File.query.filter_by(inner_link=inner_name).first()
        if file.owner_id == user_id:
            db.session.delete(file)
            db.session.commit()
            real_file = os.path.join(UPLOAD_FOLDER, inner_name)
            os.remove(real_file)
            return True
        return False

    def __repr__(self):
        return f'{self.file_path}/{self.file_name}'


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    parent = db.Column(db.String(64))
    url = db.Column(db.String(1024))
    path = db.Column(db.String(1024))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file = db.relationship('File', backref='folder', lazy='dynamic')

    @staticmethod
    def create_default_folder(user_id, user_nickname):
        folder = Folder(name=user_nickname, parent=None,
                        path=f'{user_nickname}', url=f'{user_nickname}',
                        owner_id=user_id)
        db.session.add(folder)
        db.session.commit()

    @staticmethod
    def create_folder(user_id, folder_name, parent):
        check_folder = Folder.query.filter_by(name=folder_name, owner_id=user_id,
                                              parent=parent.id).first()
        if check_folder:
            return check_folder
        folder = Folder(name=folder_name, parent=parent.id,
                        path=f'{parent.path}/{folder_name}',
                        url=f'{parent.url}/{folder_name+str(user_id)}',
                        owner_id=user_id)
        db.session.add(folder)
        db.session.commit()
        return folder

    @staticmethod
    def delete_folder(folder_id):
        folder = Folder.query.filter_by(id=folder_id).first()
        child = Folder.query.filter_by(parent=folder.parent)
        if child:
            Folder.delete_folder(child.id)
        db.session.delete(folder)
        db.session.commit()





