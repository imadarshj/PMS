import os
import serial 
import sys
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

dirname, filename = os.path.split(os.path.abspath(__file__))
#print(dirname)

model = pickle.load(open(dirname+'/model.pkl', 'rb'))


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

input_list=[]

@app.route("/dashboard")
@login_required
def dashboard():
    # text = request.args.get('jsdata')
    f = open(dirname+'/input.txt', 'r')
    data = []
    bpm = []
    temperature = []
    time = []
    count=0
    ser = serial.Serial('/dev/rfcomm1',9600)

    while(1):
        try:
            # Making -> b'BPM: 90 Temp: 99.70\r\n'  ==> as BPM: 90 Temp: 99.70
            #print("Hi")
            #print("Hi 3")
            x=str(ser.readline())
            #print("Hi 1")
            x=x[2:]
            x=x[:len(x)-5]
            input_list.append(x)
            
            print("********************8"+x+"8**********************")
            '''for line in f:
                data.append(line.strip())
                print(line)
            data = [i for i in data if i != '']
            print(input_list)
            print(data)
            for item in data:
                temp = item.split(' ')
                bpm.append(temp[1])
                temperature.append(temp[3])
            time = [dt.strftime('%Y-%m-%dT%H:%M') for dt in datetime_range(datetime.now(), len(data), timedelta(minutes=15))]'''
            count=count+1
            #break
            if count==100:
                count=0
                break
        except:
            print("Exception")
            break
    print(input_list)
    #print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for line in f:
        data.append(line.strip())
        print(line)
    data = [i for i in data if i != '']
    #print(input_list)
    #print(data)
    # Use data instead of input_list if no hardware
    for item in input_list:
        temp = item.split(' ')
        bpm.append(temp[1])
        temperature.append(temp[3])
    time = [dt.strftime('%Y-%m-%dT%H:%M') for dt in datetime_range(datetime.now(), len(data), timedelta(minutes=15))]
    input_list.clear()
    return render_template('dashboard.html', title='Dashboard', bpm=bpm, temperature=temperature, time=time)


@app.route('/symptom-checker', methods=['GET', 'POST'])
@login_required
def predict():
    if(request.method == 'POST'):
        result = request.form
        values = []
        for key, value in result.items():
            values.append(value)
        check = pd.DataFrame({
            'age': [values[0]],
            'sex': [values[1]],
            'cp': [values[2]],
            'trestbps': [values[3]],
            'chol': [values[4]],
            'fbs': [values[5]],
            'restecg': [values[6]],
            'thalach': [values[7]],
            'exang': [values[8]],
            'oldpeak': [values[9]],
            'slope': [values[10]],
            'ca': [values[11]],
            'thal': [values[12]]
        })

        output = model.predict(check)
        if(int(output[0]) == 0):
            flash(f'You do not have any Symptoms of Heart Disease.', 'success')
        else:
            flash(
                f'You do have symptoms of Heart Disease. Please consult a doctor.', 'danger')
        return render_template('predict.html', title='predict')
    else:
        return render_template('predict.html', title='predict')
