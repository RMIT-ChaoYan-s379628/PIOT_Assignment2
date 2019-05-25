import os
from flask import Flask, flash, g, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from flask_wtf import Form
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
from sqlalchemy import Column, Integer, String
import pyecharts
from pyecharts.charts import Bar
import config

app = Flask(__name__)
app.config.from_object(config)
bootstrap = Bootstrap(app)
auth = HTTPBasicAuth()
users = [{'username': 'jaqen', 'password': generate_password_hash('hghar')}]


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


def connect_to_database():
    # conn = pymysql.connect(host='127.0.0.1',
    #                        user='root',
    #                        password='65390057y',
    #                        db='library')
    # return conn
    conn = pymysql.connect(host='35.244.109.255',
                                 user='root',
                                 password='65390057y',
                                 db='LMS')
    return conn

class DeleteForm(Form):
    id = StringField('Book ID', validators=[DataRequired()])
    submit = SubmitField('Delete')


class AddBookForm(Form):
    name = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    code = StringField('ISBN code', validators=[DataRequired()])
    submit = SubmitField('Add')


@auth.verify_password
def verify_password(username, password):
    for user in users:
        if user['username'] == username:
            if check_password_hash(user['password'], password):
                return True
    return False
    

@app.route('/', methods=['POST', 'GET'])
@app.route ('/login')
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
    conn = connect_to_database()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        author = request.form['author']
        code = request.form['code']
        sql = "insert into Book (Title, Author, PublishedDate) values ('%s', '%s', '%s')" % (name, author, code)
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        conn.commit()
        return redirect('/booklist')
    sql = "select * from Book"
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
    res = cursor.fetchall()
    books = []
    for item in res:
        book = dict()
        book['id'] = item[0]
        book['title'] = item[1]
        book['author'] = item[2]
        book['PublishedDate'] = item[3]
        books.append(book)
    form = AddBookForm()
    form2 = DeleteForm()
    return render_template('booklist.html', books=books, form=form, form2=form2)


@app.route('/deletebook', methods=['POST'])
def deletebook():
    conn = connect_to_database()
    cursor = conn.cursor()
    id = request.form['id']
    sql = "delete from Book where BookID=%s" % id
    try:
        cursor.execute(sql)
    except Exception as e:
        print(e)
    conn.commit()
    return redirect('/booklist')


@app.route('/bookreport')
def bookreport():
    bar = Bar()
    bar.add_xaxis(['Last Day', 'Last 7 days', 'Last 30 days'])
    conn = connect_to_database()
    borrowedBookNums = []
    returnedNums = []
    days = [1, 7, 30]
    for day in days:
        sql = "select count(*) from BookBorrowed where (CURRENT_DATE  - BorrowedDate) <= %s" % day
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        conn.commit()
        res = cursor.fetchone()
        borrowedBookNums.append(res[0])

        sql = "select count(*) from BookBorrowed where (CURRENT_DATE  - ReturnedDate) <= %s" % day
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)
        conn.commit()
        res = cursor.fetchone()
        returnedNums.append(res[0])
    bar.add_yaxis('Borrowed Book', borrowedBookNums)
    bar.add_yaxis('Returned Book', returnedNums)
    return render_template('report.html', myechart=bar.render_embed())


if __name__ == "__main__":
    # app.run()
    host = os.popen('hostname -I').read()
    app.run(host=host, port=80, debug=False)
