from flask import Flask, render_template, redirect, flash, request
import re
import datetime
from mysqlconnection import MySQLConnector
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'email_validation')
app.secret_key="deEdlEleeDLeLoO"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check',methods=['post'])
def check():
    email = request.form['email']
    if len(email) < 1:
        flash("Email cannot be empty!")
    elif not EMAIL_REGEX.match(email):
        flash("Email is not valid!")
    else:
        flash("The email address you entered (" + email + ") is a VALID email address! Thank you!")
        query = "INSERT INTO emails (email, created_at) VALUES ('" + email + "',NOW());"
        mysql.query_db(query)
        return redirect('/success')
    return redirect('/')

@app.route('/success')
def success():
    query = "SELECT * FROM emails;"
    emails = mysql.query_db(query)
    return render_template('success.html', emails=emails)

app.run(debug = True)
