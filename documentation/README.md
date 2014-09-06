#Simple Raspberry Pi Open/Close Door Sensor With Email Software Written in Python or RPOC for short.

##Preview
<a href="http://imgur.com/oEBoSvk"><img src="http://i.imgur.com/oEBoSvk.png" title="Hosted by imgur.com" height="360px" /></a>

##Why I made it ?
I made RPOC because I leave the house and always wonder if I left the front door open or not. To combat that fear; I turned to what I knew best, technology. Using a raspberry pi and python code; I wrote a simple bot script that will send an email or a text to remind me that the door was indeed closed.




##Project Requirements
* <a href="http://www.amazon.com/RASPBERRY-MODEL-756-8308-Raspberry-Pi/dp/B009SQQF9C">Raspberry Pi </a>(Amazon aPrime)

*
<a href="http://www.adafruit.com/product/375">Door        Contact Switches
</a>


Total Cost : Less than  $50


##Raspberry Pi Instructions
connect the contact switch to pin 23 use the guides below to help you.

<img src="http://elinux.org/images/2/2a/GPIOs.png">

<img src="https://learn.adafruit.com/system/assets/assets/000/003/929/medium800/learn_raspberry_pi_breadboard.png?1396803957">



##Simple terminal instructions
```bash
# 1) Clone git

git clone https://github.com/davidholmesnyc/doorSensor.git

# 2) Go to folder
cd doorSensor

# 3) Edit Config

sudo nano config.json

# 4) Start Server

python doorSever.py
```


#Config Example
```Javascript
{

	"GMAIL-USERNAME":"myGMailAccount@gmail.com",
	"GMAIL-PASSWORD":"myGMailPassword",
	"TO":"SEND_TO_SOMEONE@thierEmailAddress.com",
	"RASPBERRY_PI_PIN":"23"

}
```

#Bonus

If you happen to know your cell phone email address  you could get MMS notifications when ever your door opens or closes
