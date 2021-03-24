from flask import Blueprint, render_template,redirect,url_for,request,flash
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html",text="testing")

@auth.route('/logout')
def logout():
    return "<p> Log out </p>"

@auth.route('/sign-up')
def sign_up():
    return render_template("sign_up.html")

@auth.route('/signup',methods=['post'])
def signup_post():
    email=request.form.get('email')
    username=request.form.get('name')
    password=request.form.get('password')

    user= User.query.filter_by(email=email).first()

    if user:
        return redirect(url_for('auth'.login))    

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
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('stress.html', prediction_text='Your Stress Level is {}'.format(output))

@auth.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    redirect(url_for('auth'.home))
    return jsonify(output)

