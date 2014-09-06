import time
import smtplib
import threading
import datetime
import json
import sys
from pprint import pprint

#START OF GET CONFIG 
json_data=open('config.json')
config = json.load(json_data)
print("Config\n")
pprint(config)
json_data.close()

# END OF GET CONFIG 

# THESE VARIBLES HELPS MAKE SURE WE DONT KEEP SENDING EMAILS  

sent_close_email_already = 0
sent_open_email_already = 0
door_pin = True 


try:
	if sys.argv[1] != 'test':
	    import RPi.GPIO as io  
	    door_pin = io.input( config['RASPBERRY_PI_PIN'] )
	    io.setmode(io.BCM)
	    io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

except ImportError:
	print("not running from a raspberry pi if you want to test this program please edit the config and then run 'python doorServer.py test' to run in test mode ")



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
	fromaddr = config["GMAIL-USERNAME"]
	toaddrs  = config["TO"]
	msg = "\n The Door was "+action+" @ " + datetime.datetime.now().strftime("%A, %B %d %Y %I:%M%p") # The /n separates the message from the headers
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(config["GMAIL-USERNAME"],config["GMAIL-PASSWORD"])
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	print(msg)
	

# init AKA DO THIS RIGHT NOW 
def __init__():
	while True:
		if door_pin:
			action('opened')
		else:
			action('closed')
			#send_email('closed')
		time.sleep(0.5)
	return 
# END OF init

# TEST SUITE -- JUST RUN TEST AND IT WILL RANDOMLY ACT LIKE THE DOOR IS OPENING OR CLOSING EVERY 5 SECONDS 
print sys.argv[1]
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
















