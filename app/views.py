from flask import render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.models import User
from app.forms import RegistrationForm, LoginForm, PhotoUploadForm, ChangeLoginPasswordForm
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', title='Головна', current_user=current_user)
    else:
        return render_template('index.html', title='Головна')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    login_error = False  

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Успішний вхід!', 'success')
            return redirect(url_for('index'))
        else:
            login_error = True
            flash("Неправильне ім'я користувача або пароль.", 'error')

    return render_template('login.html', title='Вхід', form=form, login_error=login_error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

UPLOAD_FOLDER = 'profiles_photos'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    changedata = False
    form = PhotoUploadForm()
    change_login_password_form = ChangeLoginPasswordForm()
    new_status = request.form.get('status') 

    if form.validate_on_submit():
        photo = form.photo.data
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)

            current_user.status = new_status
            current_user.photo_path = filepath
            db.session.commit()

            flash('Фотографію завантажено!', 'success')

    if change_login_password_form.validate_on_submit():
        new_login = change_login_password_form.new_login.data
        new_password = change_login_password_form.new_password.data

        if new_login != current_user.username:
            existing_user = User.query.filter_by(username=new_login).first()
            if existing_user:
                changedata = True
                flash("Користувач з таким логіном вже існує. Виберіть інший логін.", 'error')
            else:
                current_user.username = new_login

        if new_password:
            current_user.set_password(new_password)

        if changedata == False:
            db.session.commit()
            flash('Дані оновлено!', 'success')

    return render_template(
        'account.html',
        title='Обліковий запис',
        form=form,
        user=current_user,
        changedata=changedata,
        upload_folder=app.config['UPLOAD_FOLDER'],
        change_login_password_form=change_login_password_form,
        os=os
    )

@app.route('/change_login_password', methods=['POST'])
@login_required
def change_login_password():
    form = ChangeLoginPasswordForm()

    if form.validate_on_submit():
        new_username = form.new_login.data
        new_password = form.new_password.data

        existing_user = User.query.filter_by(username=new_username).first()

        if existing_user and existing_user.id != current_user.id:
            flash("Користувач з таким логіном вже існує. Виберіть інший логін.", 'error')
        else:
            current_user.username = new_username
            current_user.set_password(new_password)
            db.session.commit()

            flash('Логін та пароль успішно змінено!', 'success')

    return redirect(url_for('account'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    registration_error = None

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            registration_error = "Користувач з таким ім'ям вже існує."
            flash(registration_error, 'error')
        else:
            user = User(username=username)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            flash('Обліковий запис успішно створено. Тепер ви можете увійти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Реєстрація', form=form, registration_error=registration_error)

