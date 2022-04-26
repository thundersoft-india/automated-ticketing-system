from flask import Flask, session, render_template, request, redirect, url_for, flash
# from flask import Flask,request,g,jsonify,Response,session,redirect,url_for,escape,render_template,flash
from flask_pymongo import PyMongo
# import os
import bcrypt

app = Flask(__name__)
app.secret_key = "testing"

# Mongo DB Connection
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/test_db")
db = mongodb_client.db
records = db.register


@app.route("/")
@app.route("/main")
def main():
    return render_template('index_alt.html')


@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        signup_user = records.find_one({'username': request.form['username']})

        if signup:
            flash(request.form['username'] + ' username is already exist')
        return redirect(url_for('signup_alt'))

        hashed = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt(14))
        records.insert({'username': request.form['username'], 'password': hashed, 'email': request.form['email']})
        return redirect(url_for('signin_alt'))

    return render_template('signup_alt.html')


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index_alt.html', username=session['username'])

    return render_template('index_alt.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        signin_user = records.find_one({'username': request.form['username']})

        if signin_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), signin_user['password'].encode('utf-8')) == \
                    signin_user['password'].encode('utf-8'):
                session['username'] = request.form['username']
                return redirect(url_for('index_alt'))

        flash('Username and password combination is wrong')
        return render_template('signin_alt.html')

    return render_template('signin_alt.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index_alt'))


if __name__ == '__main__':
    app.run(debug=True)
