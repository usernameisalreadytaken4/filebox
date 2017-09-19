from app import app, db
from flask import render_template, redirect, g, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user, login_user, logout_user
from .forms import LoginForm, CreateFolder, UploadFile
from .models import User, File, Folder
from config import UPLOAD_FOLDER


@app.route('/<address>/<filename>')
@login_required
def get_file(address, filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/del/<address>/<filename>')
@login_required
def delete_file(address, filename):
    File.delete_file(filename, g.user.id)
    return redirect(url_for('user', address=address))


@app.route('/')
@login_required
def index():
    base_folder = Folder.query.filter_by(url=g.user.nickname).first()
    return redirect(url_for('user', address=base_folder.url))


@app.route('/<path:address>', methods=['GET', 'POST'])
@login_required
def user(address):
    print('--'*10, 'address: ', address)
    current_folder = Folder.query.filter_by(url=address).first()
    form_create_folder = CreateFolder()
    form_upload_file = UploadFile()
    # пытаемся создать папку
    if form_create_folder.validate_on_submit():
        folder = Folder.create_folder(g.user.id, form_create_folder.folder_name.data, current_folder)
        print(folder.url)
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
                           form_create_folder=form_create_folder, form_upload_file=form_upload_file)


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            default_folder = Folder(
                name=form.nickname.data,
                parent=None,
                url=f'{form.nickname.data}',
                path=f'{form.nickname.data}',
                owner_id=user.id
            )
            db.session.add(default_folder)
            db.session.commit()
        if user and form.password.data == user.password:
            login_user(user)
            address = Folder.query.filter_by(owner_id=user.id).first()
            return redirect(url_for('user', address=address.url))
    return render_template('login.html',
                           title='введите логин и пароль',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.before_request
def before_request():
    g.user = current_user

