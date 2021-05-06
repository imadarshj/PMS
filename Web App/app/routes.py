import os
from datetime import datetime, timedelta
from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
import numpy as np

model = pickle.load(open(
    'C:\\Users\\Tushar\\Downloads\\TARP-main\\TARP-main\\Web App\\app\\model.pkl', 'rb'))


def datetime_range(start, end, delta):
    current = start
    i = 0
    while i < end:
        yield current
        current += delta
        i += 1


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms = RegistrationForm()
    if forms.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            forms.password.data).decode('utf-8')
        user = User(username=forms.username.data,
                    email=forms.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account created for {forms.username.data}! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=forms)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    forms = LoginForm()
    if forms.validate_on_submit():
        user = User.query.filter_by(email=forms.email.data).first()
        if(user and bcrypt.check_password_hash(user.password, forms.password.data)):
            login_user(user, remember=forms.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', title='Login', form=forms)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/dashboard")
@login_required
def dashboard():
    # text = request.args.get('jsdata')
    f = open(
        'C:\\Users\\Tushar\\Downloads\\TARP-main\\TARP-main\\Web App\\app\\input.txt', 'r')
    data = []
    bpm = []
    temperature = []
    time = []

    while(1):
        try:
            # ser = serial.Serial('/dev/rfcomm1',9600)
            # input_list.append(str(ser.readline()))
            for line in f:
                data.append(line.strip())
            data = [i for i in data if i != '']
            for item in data:
                temp = item.split(' ')
                bpm.append(temp[1])
                temperature.append(temp[3])
            time = [dt.strftime('%Y-%m-%dT%H:%M') for dt in datetime_range(
                datetime.now(), len(data), timedelta(minutes=15))]
            return render_template('dashboard.html', title='Dashboard', bpm=bpm, temperature=temperature, time=time)
        except:
            break


@app.route('/predict')
def predict():
    check = pd.DataFrame({'age': [67],	'sex': [1],	'cp': [2],	'trestbps': [152],	'chol': [212],	'fbs': [
                         0],	'restecg': [0], 'thalach': [150],	'exang': [0],	'oldpeak': [0.8],	'slope': [1],	'ca': [0],	'thal': [3]})
    scaler = StandardScaler()
    check = scaler.fit_transform(check)
    output = model.predict(check)
    return render_template('predict.html', prediction_text='the output is {}'.format(output[0]), title='predict')
