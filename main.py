from flask_login import LoginManager
from flask import Flask
from flask import render_template
from flask import redirect, request, abort
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime
from data import db_session
from forms.user import RegisterForm
from data.users import User
from data.loginform import LoginForm
from data.dosts import Dosts
from forms.dosts import DostsForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session.global_init("db/teachers.db")
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    return render_template("glav.html")


@app.route('/dost')
def dost():
    db_session.global_init('db/teachers.db')
    db_sess = db_session.create_session()
    dosts = db_sess.query(Dosts)
    return render_template("dost.html", dosts=dosts)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init('db/teachers.db')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user1 = db_sess.query(User).filter(User.speciality == 'Руководитель студии').first()
        if not user1.check_password(form.em.data):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Неверное подтверждение регистрации руководителем студии")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            otch=form.otch.data,
            email=form.email.data,
            age=form.age.data,
            education=form.education.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init('db/teachers.db')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/dost")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/napr')
def napr():
    return render_template("napr.html")


@app.route('/ped')
def ped():
    return render_template("ped.html")


@app.route('/kont')
def kont():
    return render_template("kont.html")


@app.route('/new_dost', methods=['GET', 'POST'])
@login_required
def new_dost():
    form = DostsForm()
    db_session.global_init('db/teachers.db')
    if request.method == 'GET':
        return render_template("dosts.html", form=form)
    elif request.method == 'POST':
        db_sess = db_session.create_session()
        dosts = Dosts()
        dosts.title = form.title.data
        dosts.content = form.content.data
        current_user.dosts.append(dosts)
        db_sess.merge(current_user)
        db_sess.commit()
        user = db_sess.query(Dosts).filter(Dosts.content == form.content.data).first()
        i = user.id
        file = request.files['file']
        file.save(f"static/img/photo{i}.jpg")
        return redirect('/dost')
    return render_template("dosts.html", form=form)


@app.route('/dosts/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dosts(id):
    form = DostsForm()
    if request.method == "GET":
        db_session.global_init('db/teachers.db')
        db_sess = db_session.create_session()
        dosts = db_sess.query(Dosts).filter(Dosts.id == id).first()
        if dosts:
            form.title.data = dosts.title
            form.content.data = dosts.content
        else:
            abort(404)
    if form.validate_on_submit():
        db_session.global_init('db/teachers.db')
        db_sess = db_session.create_session()
        dosts = db_sess.query(Dosts).filter(Dosts.id == id).first()
        if dosts:
            dosts.title = form.title.data
            dosts.content = form.content.data
            db_sess.commit()
            return redirect('/dost')
        else:
            abort(404)
    return render_template('edit.html',
                           form=form
                           )


@app.route('/dosts_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_session.global_init('db/teachers.db')
    db_sess = db_session.create_session()
    dosts = db_sess.query(Dosts).filter(Dosts.id == id).first()
    if dosts:
        db_sess.delete(dosts)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/dost')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/dost")


@app.route('/edit_prof', methods=['GET', 'POST'])
@login_required
def edit_prof():
    form = RegisterForm()
    if request.method == "GET":
        db_session.global_init('db/teachers.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.otch.data = user.otch
            form.email.data = user.email
            form.education.data = user.education
            form.age.data = user.age
            form.speciality.data = user.speciality
        else:
            abort(404)
    else:
        db_session.global_init('db/teachers.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.otch = form.otch.data
            user.email = form.email.data
            user.education = form.education.data
            user.age = form.age.data
            user.speciality = form.speciality.data
            db_sess.commit()
            return redirect('/dost')
        else:
            abort(404)
        return redirect('/login')
    return render_template('edit_prof.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
