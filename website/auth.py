from flask import Blueprint, render_template,redirect,url_for,request,flash
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from flask import session
from flask import Flask
from flask_mysqldb import MySQL
import MySQLdb
import mysql.connector
from datetime import timedelta

auth = Blueprint('auth', __name__)

app=Flask(__name__)
app.secret_key="0000"
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
    return "<p> Log out </p>"

@auth.route('/sign-up',methods=['GET','POST','DELETE'])
def sign_up():
    return render_template("sign_up.html")

#def signup_post(): 
@auth.route('/adduser',methods=['GET','POST','DELETE'])

def add():
    email=request.form.get("u_email")
    username=request.form.get("username")
    password=request.form.get("u_password")

    cursor=conn.cursor()
    cursor.execute("""INSERT INTO `sign_up` (`Email`,`Username`,`Password`) VALUES ('{}','{}','{}')""".format(email,username,password))
    conn.commit()
    flash('User created successfully!')
    return 'user registered succesfully'


@auth.route("/checkuser",methods=["POST",'GET'])
def check():

    cursor = conn.cursor()
    sql = """SELECT `Username` as username FROM `sign_up` """
    cursor.execute(sql)
    alist = cursor.fetchall()
    [i[0] for i in alist]

    if request.method=='POST':
        session.pop('user_name',None)

        username=request.form.get("username")
        password=request.form.get('password1')
        print(username)
        print(password)

        cursor.execute("""SELECT * FROM `sign_up` WHERE  `Password` LIKE '{}' AND `username` LIKE `username`""".format(password,username))
        users=cursor.fetchall()
        print(users)
    

        if len(users) > 0:
            flash('You were successfully logged in')
            session['user_name']=alist[0]
            return render_template("dashboard.html")

        else:
            flash("INCORRECT USERNAME OR PASSWORD! PLEASE TRY AGAIN!")

            return render_template("login.html")
    

   # user= User.query.filter_by(email=email).first()

    #if user:
     #   return redirect(url_for('auth.login'))    

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

