##################################################################################################################################
#                                                       Adarsh , Aadithya                                                               #
##################################################################################################################################

import serial 
import sys
import os

from flask import Flask
app = Flask(__name__)


#ser = serial.Serial('/dev/rfcomm0',9600) 
#ser1 = ser.readline().decode('ascii')
path='/sys/class/backlight/intel_backlight/brightness' 


# @ signifies a decorator
@app.route('/')
def index():
    return 'This is home page'

@app.route('/heart')
def heartrate():
	while(1):
		try:
			ser = serial.Serial('/dev/rfcomm8',9600) 
			value  = str(ser.readline())
			print (value)
			return '<h2>pulse is:</h2> ' + value
		except KeyboardInterrupt:
			print('Interrupted')
			break

if __name__=="__main__":
    app.run()

############################################################# END ##################################################################
