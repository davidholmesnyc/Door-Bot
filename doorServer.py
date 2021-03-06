#!/usr/bin/python 
import time
import smtplib
import threading
import datetime
import json
import sys
from pprint import pprint
import sys, os


# THESE VARIBLES HELPS MAKE SURE WE DONT KEEP SENDING EMAILS  

sent_close_email_already = 0
sent_open_email_already = 0
door_pin = True 


#START OF GET CONFIG 
pathname = os.path.dirname(sys.argv[0])
json_data=open(os.path.abspath(pathname)+'/config.json')
config = json.load(json_data)
print("Config\n")
pprint(config)
json_data.close()

# END OF GET CONFIG 

# RASPBERRY PI STUFF 

try:
	
	if len(sys.argv) < 2:
			import RPi.GPIO as io  
			io.setmode(io.BCM)
			io.setup( config['RASPBERRY_PI_PIN'] , io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp
			door_pin = io.input( config['RASPBERRY_PI_PIN'] )
except ImportError:
		raise ImportError("not running from a raspberry pi if you want to test this program please edit the config and then run 'python doorServer.py test' to run in test mode ")



# END OF RASPBERRY PI STUFF 


# FUNCTIONS -- PATTERN STYLE DECROTIVE 
def action(action):

	global sent_close_email_already
	global sent_open_email_already
	
	if(action == 'closed'):
		if sent_close_email_already != 1 :
			print('Door '+action)
			sent_open_email_already = 0
			sent_close_email_already = 1
			send_email(action)
			print('Sent Closed Email')
	
	if(action == 'opened'):
		if sent_open_email_already != 1 :
			print('Door '+action)
			sent_close_email_already = 0
			sent_open_email_already = 1
			send_email(action)
			print('Sent Open Email')
	return

## SEND EMAIL FUNCTON  -- ACCEPTED ACTION STATES('open','closed')
def send_email(action):
	try:
		fromaddr = config["GMAIL-USERNAME"]
		toaddrs  = config["TO"]
		msg = "\n The Door was "+action+" on " + datetime.datetime.now().strftime("%A, %B %d %Y %I:%M%p") # The /n separates the message from the headers
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(config["GMAIL-USERNAME"],config["GMAIL-PASSWORD"])
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
		print(msg)
	except:
		print("ERROR CONNECTING TO MAIL SERVER")
		

# init AKA DO THIS RIGHT NOW 
def __init__():
	while True:
		try:
			door_pin = io.input( config['RASPBERRY_PI_PIN'] )
		except:
			door_pin = door_pin

		if door_pin:
			action('opened')
		else:
			action('closed')
			#send_email('closed')
		time.sleep(0.5)
	return 
# END OF init

# TEST SUITE -- JUST RUN the TEST Parameter AND IT WILL RANDOMLY ACT LIKE THE DOOR IS OPENING OR CLOSING EVERY 5 SECONDS 
#print sys.argv[1]
if len(sys.argv) > 2:
	if sys.argv[1] == 'test':
		def testServer():
			print('Starting Test Mode --- EVERY 5 SECONDS THE DOOR WILL OPEN OR CLOSE')
			def set_interval(func, sec):
				def func_wrapper():
					set_interval(func, sec)
				func()
				t = threading.Timer(sec, func_wrapper)
				t.start()
				return t

			def randomDoorInput():
				time.sleep(5)
				global door_pin
				if door_pin == True :
					door_pin = False
				else:
					door_pin = True
				return door_pin

			return set_interval(randomDoorInput,5)
		testServer()
#END OF TEST SUITE 


# START UP FUNCTIONS 
__init__()

#END OF START UP FUNCTIONS 
















