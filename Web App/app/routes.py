import os
import serial
import sys
from twilio.rest import Client
from datetime import datetime, timedelta
from app import app, db, bcrypt, mail
from flask_mail import Message
from flask import render_template, url_for, flash, redirect, request
from app.forms import RegistrationForm, LoginForm
from app.models import User, Report
from flask_login import login_user, current_user, logout_user, login_required

from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
import numpy as np

dirname, filename = os.path.split(os.path.abspath(__file__))
# print(dirname)

model = pickle.load(open(dirname+'/model.pkl', 'rb'))


def most_frequent(bpm):
    return max(set(bpm), key=bpm.count)


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
                    email=forms.email.data, password=hashed_password, phone=forms.phone.data)
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


input_list = []
maximum_heart_rate = 0


def most_frequent(List):
    return max(set(List), key=List.count)


@app.route("/dashboard")
@login_required
def dashboard():
    # text = request.args.get('jsdata')
    f = open(dirname+'/input.txt', 'r')
    data = []
    bpm = []
    temperature = []
    time = []
    count = 0
    ser = serial.Serial('/dev/rfcomm3',9600)

    while(1):
        try:
            # Making -> b'BPM: 90 Temp: 99.70\r\n'  ==> as BPM: 90 Temp: 99.70
            # print("Hi")
            # print("Hi 3")
            x = str(ser.readline())
            #print(x)
            # print("Hi 1")
            x = x[2:]
            x = x[:len(x)-5]
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
            count = count+1
            # break
            if count == 100:
                count = 0
                break
        except:
            print("Exception")
            break
    # print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for line in f:
        data.append(line.strip())
    data = [i for i in data if i != '']
    # print(input_list)
    # print(data)
    # Use data instead of input_list if no hardware
    for item in data:
        temp = item.split(' ')
        bpm.append(temp[1])
        temperature.append(temp[3])
    # Sending Emails Part
    file1 = open('myfile.txt', 'r')
    s=file1.read()
    print("----------------The sent. is "+s+"  - ")
    print(type(s))
    if(int(s)==0):
	    most_frequent_bpm = most_frequent(bpm)
	    print("Equal")
	    msg = f'Hi {current_user.username} Your Heartrate is: {most_frequent_bpm}'
	    email = current_user.email
	    subject = 'HeartRate Alert'
	    message = Message(subject, sender="dummy768.mail@gmail.com", recipients=[email])
	    message.body = msg
	    mail.send(message)
	    
	    account_sid="ACd3e473fa31ae435131e9294621b7d251"
	    auth_token="4fddb8493a9a346d045bcad21ea922b9"
	    client = Client(account_sid,auth_token)
	    client.messages.create(
	    	to="+918479047961",
	    	from_="+19045745588",
	    	body=msg
	    )
	    
	    	
    file1.close()
    file1 = open('myfile.txt', 'w')
    file1.write("1")
    file1.close()
    #####################
    # Calculating the most frequent heart rate
    global maximum_heart_rate
    maximum_heart_rate = most_frequent(bpm)
    # print(var_list)
    # print(maximum_heart_rate)
    symptoms1 = ""
    symptoms2 = ""
    if(int(maximum_heart_rate) > 150):
        symptoms1 = "Your heart rate is " + \
            str(maximum_heart_rate) + \
            " .You may have symptoms of Supraventricular Tachycardia"
    elif(int(maximum_heart_rate) < 60):
        symptoms2 = "Your heart rate is " + \
            str(maximum_heart_rate) + " .You may have symptoms of Bradycardia."
    else:
        symptoms1 = "Your heart rate is " + \
            str(maximum_heart_rate) + " which is normal."

    time = [dt.strftime('%Y-%m-%dT%H:%M')
            for dt in datetime_range(datetime.now(), len(data), timedelta(minutes=15))]
    input_list.clear()
    return render_template('dashboard.html', title='Dashboard', bpm=bpm, temperature=temperature, time=time, symptoms1=symptoms1, symptoms2=symptoms2)


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
            'thalach': [maximum_heart_rate]
        })
        # print(maximum_heart_rate)
        output = model.predict(check)
        result = ''
        if(int(output[0]) == 0):
            flash(f'You do not have any Symptoms of Heart Disease.', 'success')
            result = 'You didnt have any sypmtoms of Heart Disease'
        else:
            flash(
                f'You do have symptoms of Heart Disease. Please consult a doctor.', 'danger')
            result = 'You did have symptoms of Heart Disease'
        report = Report(age=values[0], sex=values[1], cp=values[2], trestbps=values[3], chol=values[4], fbs=values[5], restecg=str('remove'),
                        thalach=maximum_heart_rate, exang=str('remove'), oldpeak=str('remove'), slope=str('remove'), ca=str('remove'), thal=str('remove'), result=result, patient=current_user)
        db.session.add(report)
        db.session.commit()
        return render_template('predict.html', title='Predict')
    else:
        return render_template('predict.html', title='Predict', maximum_heart_rate=maximum_heart_rate)


@ app.route('/reports', methods=['GET', 'POST'])
@ login_required
def reports():
    user = User.query.filter_by(username=current_user.username).first()
    reports = user.reports
    return render_template('reports.html', title='Report', reports=reports)
