from flask import Flask, flash, g, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from flask_wtf import Form
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from pyecharts.charts import Bar
from web import config

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

users = [{'username': 'jaqen', 'password': generate_password_hash('hghar')}]


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddBookForm(Form):
    name = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    catalogue = StringField('Catalogue', validators=[DataRequired()])
    code = StringField('ISBN code', validators=[DataRequired()])
    submit = SubmitField('Add')


class Book(db.Model):
    __tablename__ = 'BookList'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), index=True)
    author = Column(String(80))
    catalogue = Column(String(80))
    code = Column(String(80), unique=True)

    def __init__(self, name=None, author=None, catalogue=None, code=None):
        self.name = name
        self.author = author
        self.code = code
        self.catalogue = catalogue

    def __repr__(self):
        return "<Book %r>" % (self.name)


@auth.verify_password
def verify_password(username, password):
    for user in users:
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                return True
    return False


## @auth.login_required
## def login_required():
##    if not g.user:
##        return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
@app.route('/login')
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_password(username, password):
            g.user = username
            return redirect('/booklist')
        else:
            flash('Username or password is wrong!')
    Form = LoginForm()
    return render_template('login.html', form=Form)


@auth.login_required
@app.route('/booklist', methods=['GET', 'POST'])
def booklist():
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        catalogue = request.form['catalogue']
        code = request.form['code']
        NewBook = Book(name, author, catalogue, code)
        db.session.add(NewBook)
        db.session.commit()
        return redirect('/booklist')
    db.create_all()
    books = Book.query.all()
    form = AddBookForm()
    return render_template('booklist.html', books=books, form=form)


@app.route('/bookreport')
def bookreport():
    bar = Bar()
    bar.add_xaxis(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    bar.add_yaxis('Borrowed Book', [12, 15, 20, 10, 5, 8, 10])
    bar.add_yaxis('Returned Book', [10, 18, 10, 7, 6, 6, 4])
    return render_template('report.html', myechart=bar.render_embed())


if __name__ == "__main__":
    app.run(debug=True)
