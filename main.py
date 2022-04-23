from flask import Flask, render_template, url_for, redirect
from data import db_session
from data.users import User
from data.reps import Reports
from data.machine import Machine
from data.bucket import Bucket
from forms.user import RegisterForm
from flask_login import LoginManager
from forms.login import LoginForm
from flask_login import login_required, login_user, logout_user


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/bk.db")
    app.add_url_rule('/', 'index', index)
    app.run()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Reports).filter(Reports.is_private != True)
    return render_template("index.html", news=news)

@app.route("/factory")
def factory():
    db_sess = db_session.create_session()
    news = db_sess.query(Reports).filter(Reports.is_private != True)
    return render_template("factory.html", news=news)

@app.route("/gallery")
def gallery():
    db_sess = db_session.create_session()
    news = db_sess.query(Reports).filter(Reports.is_private != True)
    return render_template("gallery.html", news=news)


@app.route("/about")
def about():
    return render_template("about.html",title="Ковши от Жени")

@app.route("/products")
def prod():
    #формируем список техники
    db_sess = db_session.create_session()
    machine_list = db_sess.query(Machine)
    new_list=[]
    for item in machine_list:
        new_list.append(item)
        new_list[-1].main_pic = url_for('static', filename=item.main_pic)
        new_list[-1].id = "prods\\"+str(item.id)

    return render_template("prod.html",title="Ковши от Жени",machine_list=new_list)

@app.route('/prods/<int:mach_id>')
def prods(mach_id):
    # формируем список техники
    db_sess = db_session.create_session()
    buckets_list = db_sess.query(Bucket).filter(Bucket.machine_id == mach_id)
    new_list = []
    for item in buckets_list:
        new_list.append(item)
        new_list[-1].main_pic = '/static/buckets/'+item.pic_url
        new_list[-1].url = new_list[-1].id = "buckets\\"+str(item.id)

    return render_template("buckets.html", title="Ковши от Жени", buckets_list=new_list)

@app.route('/prods/buckets/<int:bucket_id>')
def buckets(bucket_id):
    # формируем список техники
    db_sess = db_session.create_session()
    buckets_list = db_sess.query(Bucket).filter(Bucket.id == bucket_id).first()
    return render_template("bucket_desc.html", bucket=buckets_list)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

if __name__ == '__main__':
    main()