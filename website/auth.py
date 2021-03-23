from flask import Blueprint, render_template,redirect,url_for,request,flash

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
