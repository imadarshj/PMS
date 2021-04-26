##################################################################################################################################
#                                                       Adarsh , Aadithya                                                               #
##################################################################################################################################

import serial 
import sys
import os

ser = serial.Serial('/dev/rfcomm8',9600) 

path='/sys/class/backlight/intel_backlight/brightness' 



while(1):
	try:
		#value  = ser.readline().split()
		value  = str(ser.readline())
		#value = value.split()
		print (value+"\n\n") 
		
	except KeyboardInterrupt:
		print('Interrupted')
		break
	#finally:
		#ser.close()
		# Just to take care of initial garbage values

		
############################################################# END ##################################################################
