from flask import Blueprint, render_template,redirect,url_for,request,flash
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask import session
from flask import Flask
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb
import mysql.connector
from datetime import timedelta
import bcrypt
from bcrypt import checkpw
from flask_bcrypt import Bcrypt
from hashlib import md5

auth = Blueprint('auth', __name__)

bcrypt1=Bcrypt()
app=Flask(__name__)
mysql1=MySQL(app)
app.secret_key="0000"
app.config['MySQL_HOST']= 'localhost'

conn=mysql.connector.connect(host="localhost",user="root",password="",db="fit fact")

if(conn):
    print("connection succesful")
cursor=conn.cursor()


output=0

    


@auth.route('/login',methods=['POST','GET','DELETE'])
def login():
    return render_template("login.html",text="testing")

@auth.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')
    return "<p> Log out </p>"

@auth.route('/sign-up',methods=['GET','POST','DELETE'])
def sign_up():
    return render_template("sign_up.html")

#def signup_post(): 
@auth.route('/adduser',methods=['GET','POST','DELETE'])

def add():
    email=request.form.get("u_email")
    username=request.form.get("username")
    password=request.form.get("u_password").encode('utf-8')
    hashpwd=bcrypt.hashpw(password,bcrypt.gensalt())

    cursor=conn.cursor()
    cursor.execute("INSERT INTO sign_up (Email,Username,Password) VALUES (%s, %s, %s)",(email,username,password,))
    conn.commit()
    session['name']= username
    session['email']= email

    flash('User created successfully!')
    return render_template('login.html')

@app.before_request
def before_request():
   g.username = None
   if 'username' in session:
       g.username = session['username']


@auth.route("/checkuser",methods=["POST",'GET'])
def check():

    if request.method=="POST":
        username=request.form['username']
        password=request.form['password1'].encode('utf-8')
        hashed=bcrypt.hashpw(password,bcrypt.gensalt())

        cur=conn.cursor(dictionary=True, buffered=True)
        cur.execute("SELECT * FROM sign_up WHERE Email =%s", [username])

        if cur is not None:
            data = cur.fetchone()
            try:
                password1 = data['Password']
            except Exception:
                error = 'Invalid Username or Password'
                flash(" ")
                return render_template('login.html', error=error)


            if bcrypt.checkpw(password1.encode('utf-8'),hashed):
                app.logger.info('Password Matched')
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                cur.close()
                return render_template('dashboard.html')
        

        else:
            error = 'Invalid Username or Password'
            return render_template('login.html', error=error)
 
        



@auth.route('/about')
def about():
    return render_template("about.html")


@auth.route('/predict')
def home():
    model = pickle.load(open('model.pkl', 'rb'))

    return render_template('stress.html')

@auth.route('/predicted',methods=['POST'])
def predict():
    model = pickle.load(open('model.pkl', 'rb'))
    int_features = [int(x) for x in request.form.values()]
    for x in request.form.keys():
        session[x] =  request.form.get(x)
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    redirect(url_for('auth.exposition'))
    session['my_var'] = output

    return render_template('stress.html', prediction_text='Your Stress Level is {}'.format(output))

@auth.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    redirect(url_for('auth'.home))
    return jsonify(output)


@auth.route('/exposition',methods=['GET','POST'])
def exposition():
    value = session.get('my_var', None)
    Mood = session.get('Mood', None)
    Sleep = session.get('Hours of Sleep', None)
    return render_template('report.html', value=int(value), mood = int(Mood), sleep = int(Sleep))

@auth.route('/analyze', methods=['GET','POST'])
def analyze():
    return render_template('analyze.html')