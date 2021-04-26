##################################################################################################################################
#                                                       Adarsh , Aadithya                                                               #
##################################################################################################################################

import serial 
import sys
import os

ser = serial.Serial('/dev/rfcomm0',9600) 
ser1 = ser.readline().decode('ascii')
path='/sys/class/backlight/intel_backlight/brightness' 



while(1):
	try:
		#value  = ser.readline().split()
		value  = str(ser.readline())
		#value = value.split()
		print (value) 
		
	except KeyboardInterrupt:
		print('Interrupted')
		break
	#finally:
		#ser.close()
		# Just to take care of initial garbage values

# @ signifies a decorator
@app.route('/')
def index():
    return 'This is home page'

@app.route('/heart')
def heartrate():
    water = serial.Serial("COM4",9600)
    water1 = water.readline().decode('ascii')
    return '<h2>pulse is:</h2> ' + ser1 + '%'




if __name__=="__main__":
    app.run()

############################################################# END ##################################################################
