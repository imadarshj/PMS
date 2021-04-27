import serial 
import sys
import os
import time

from flask import Flask, render_template, request
app = Flask(__name__,template_folder='template')
#ser = serial.Serial('/dev/rfcomm0',9600) 
#ser1 = ser.readline().decode('ascii')
path='/sys/class/backlight/intel_backlight/brightness' 

file1 = open('input.txt', 'r')
# @ signifies a decorator
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heart')
def heartrate():
	text = request.args.get('jsdata')
	input_list = []
	while(1):
		try:
			input_list.append(str(file1.readline()))
			return render_template('input.html', input=input_list)
		except KeyboardInterrupt:
			print('Interrupted')
			break

if __name__=="__main__":
    app.run()