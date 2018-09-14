import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from datetime import timedelta
import requests

GPIO.setmode(GPIO.BCM)
gpiopin = 23
GPIO.setup(gpiopin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#time format which is sent to server
format = "%Y-%m-%d %H-%M-%S"

apikey = "3cyBp6zUCDtcm2wb"
serveraddress = '127.0.0.1:5000'

blinks = 0
starttime = datetime.now()

#function called when blinked is detected
def my_callback(channel):
	global blinks
	print("blink detected n. ", str(blinks), " input=", GPIO.input(channel))
	blinks += 1

GPIO.add_event_detect(gpiopin, GPIO.RISING, callback=my_callback, bouncetime=400)

#loop
while(True):
	sleep(1)
	difftime = datetime.now() - starttime

	#if interval time passed
	if difftime > timedelta(0,10):
		payload = {'start': starttime.strftime(format), 'end': datetime.now().strftime(format), 'watthour': blinks, 'key': apikey}
		r = requests.post(serveraddress+'/electricityusage', json=payload)
		blinks = 0
		starttime = datetime.now()
		print('response: ', r)

GPIO.cleanup()
