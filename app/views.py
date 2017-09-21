from app import app, db
from flask import render_template, redirect, g, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user, login_user, logout_user
from .forms import LoginForm, CreateFolder, UploadFile, MoveFile
from .models import User, File, Folder
from config import UPLOAD_FOLDER


@app.route('/')
@login_required
def index():
    print('index', '---' * 10)
    base_folder = Folder.query.filter_by(url=g.user.nickname).first()
    return redirect(url_for('user', address=base_folder.url))


@app.route('/<path:address>', methods=['GET', 'POST'])
@login_required
def user(address):
    print('user', '---' * 10)
    current_folder = Folder.query.filter_by(url=address).first()
    form_create_folder = CreateFolder()
    form_upload_file = UploadFile()
    form_move_file = MoveFile()
    if form_move_file.is_submitted():
        return redirect(url_for('move_file', address=form_move_file.new_path.data, filename=''))
    # пытаемся создать папку
    if form_create_folder.validate_on_submit():
        folder = Folder.create_folder(g.user.id, form_create_folder.folder_name.data, current_folder)
        return redirect(url_for('user', address=folder.url))
    # пытаемся загрузить файл
    if form_upload_file.validate_on_submit():
        File.upload_file(form_upload_file.file.data, current_folder.id, g.user.id)
        return redirect(url_for('user', address=address))
    folder_list = Folder.query.filter_by(parent=current_folder.id).all()
    parent = Folder.query.filter_by(id=current_folder.parent).first()
    file_list = File.query.filter_by(folder_id=current_folder.id).all()
    return render_template('folders.html', folder=current_folder,
                           folder_list=folder_list, file_list=file_list, parent=parent,
                           form_create_folder=form_create_folder, form_upload_file=form_upload_file,
                           form_move_file=form_move_file)


@app.route('/get/<path:address>/<filename>', methods=['GET'])
@login_required
def get_file(address, filename):
    print('getfile', '---'*10)
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/del/<path:address>/<filename>')
@login_required
def delete_file(address, filename):
    print('deletefile', '---' * 10)
    File.delete_file(filename, g.user.id)
    return redirect(url_for('user', address=address))


@app.route('/move/<path:new_address>/<filename>')
@login_required
def move_file(new_address, filename):
    print('move_file', '---' * 10)
    File.move_file(filename, new_address)
    return redirect(url_for('user', address=new_address))


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login', '---' * 10)
    if g.user is not None and g.user.is_authenticated:
        default_folder = Folder.query.filter_by(owner_id=g.user.id).first()
        if default_folder is None:
            Folder.create_default_folder(g.user.id, g.user.nickname)
        return redirect(url_for('user', address=default_folder.url))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.nickname.data).first()
        if form.nickname.data is None or form.nickname.data == '':
            return redirect(url_for('login'))
        if form.password.data is None or form.password.data == '':
            return redirect(url_for('login'))
        if user and form.password.data != user.password:
            flash('пароль неправильный')
            return redirect(url_for('login'))
        if user is None:
            user = User(
                nickname=form.nickname.data,
                password=form.password.data
            )
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(nickname=form.nickname.data).first()
            Folder.create_default_folder(user.id, user.nickname)
        if user and form.password.data == user.password:
            login_user(user)
            address = Folder.query.filter_by(owner_id=user.id).first()
            return redirect(url_for('user', address=address.url))
    return render_template('login.html',
                           title='введите логин и пароль',
                           form=form)


@app.route('/logout')
def logout():
    print('logout', '---' * 10)
    logout_user()
    return redirect(url_for('login'))


@app.before_request
def before_request():
    print('before request', '---' * 10)
    g.user = current_user

