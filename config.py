import os


basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'jopasruchkoi'


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


UPLOAD_FOLDER = os.path.join(basedir, 'storage')
MAX_CONTENT_LENGTH = 64*1024*1024

#EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'gif', 'zip']
#ALLOWED_EXTENSIONS = set(EXTENSIONS)



