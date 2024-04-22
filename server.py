import os

from flask_login import current_user, login_required, logout_user, LoginManager, login_user, UserMixin
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from data.user import RegisterForm
from data.users import User
from data.login import LoginForm
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose, form
from flask_admin.contrib.sqla import ModelView
from api import dops_api
from flask import Flask, render_template, url_for, make_response, jsonify, redirect
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_puper_secret_key_you_will_not_get_it'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/sc1357_db_.sqlite'
db = SQLAlchemy(app)
file_path = 'C:/Users/Максим/PycharmProjects/sch_project/static/events'
# def main():
db_session.global_init("db/sc1357_db_.sqlite")
app.register_blueprint(dops_api.blueprint)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class Table(db.Model, SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'events'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    event = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)


admin = Admin(app, name='admin', template_mode='bootstrap4')

db_sess = db_session.create_session()


class MyView(ModelView):
    form_extra_fields = {
        'image': form.ImageUploadField('Image',
                                       base_path=file_path)
    }

    # def is_accessible(self):
    #     return current_user.is_authenticated
    #
    # def not_auth(self):
    #     return make_response(jsonify({'ERROR': 'Forbidden'}), 403)


admin.add_view(MyView(name='Hello', session=db_sess, model=Table, url='/add-data'))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'ERROR': 'Bad Request'}), 400)


@app.route('/')
@app.route('/index')
def start():
    return render_template("index.html", title='Школа 1357')


# @app.route('/admin')
# def admin_1():
#     return render_template("admin/index.html", title='Школа 1357')


@app.route('/events')
def events():
    db_sess = db_session.create_session()
    db_ = db_sess.query(Table).all()
    items = [item.to_dict(only=('event', 'description')) for item in db_]
    print(items)
    images = db_sess.query(Table.image).all()
    images = [f"events/{image[0]}" for image in images]
    return render_template("events.html", title='Мероприятия', items=items, images=images,
                           zip=zip)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # db_sess = db_session.create_session()
        # user = db_sess.query(User).filter(User.name == form.username.data).first()
        # if user and user.check_password(form.password.data):
        #     login_user(user, remember=form.remember_me.data)
        return redirect('/admin')
        # return render_template('login.html',
        #                        message="Неправильный логин или пароль",
        #                        form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/кружки')
def show_1():
    return render_template('кружки.html', title='Школа 1357')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    # main()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port)
