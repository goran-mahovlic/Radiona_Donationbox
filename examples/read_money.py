#!/usr/bin/env python2.7
# script by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
# Modified by Goran Mahovlic January 2015
# GPIO 24 is now pullup to
# GPIO 17 is used to detect pulses from coin acceptor
# COUTION!!!  Output from coin acceptor is 5V You can burn your raspberry
# Added 1 blue LED in serie on pulse wire to lower coin acceptor Voltage
# Do not do this without proper messuring pulse output pin, it shoud not exceed 3.3V 

import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)

# GPIO 17 & 23 & 17 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for all
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#defining global variables
time_stamp = time.time() 
pulse = 0
money = 0

# now we'll define tree threaded callback functions
# these will run in another thread when our events are detected
# first is used to get puses from coin Acceptor
def my_callback(channel):

    global time_stamp
    global pulse
    time_now = time.time()
    pulse = pulse + 1
    time_stamp = time_now

# second we will use later for user interface
def my_callback2(channel):

    print "falling edge detected on 23"

def my_callback3(channel):

    print "falling edge detected on 24"


print "Make sure you have a button connected so that when pressed"
print "it will connect GPIO port 23 (pin 16) to GND (pin 6)\n"
print "You will also need a second button connected so that when pressed"
print "it will connect GPIO port 24 (pin 18) to GND (pin 6)\n"
print "You will also need a third button connected so that when pressed"
print "it will connect GPIO port 17 (pin 11) to GND (pin 14)"
raw_input("Press Enter when ready\n>")
print "Please insert coins to radiona donation box :)"

# when a falling edge is detected on port 17, regardless of whatever 
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=50)
# when a falling edge is detected on port 23 & 24, regardless of whatever 
# else is happening in the program, the function my_callback2 will be run
# 'bouncetime=300' includes the bounce control written into interrupts2a.py
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback3, bouncetime=300)

try:
    while True: 

        time_now = time.time()
        if (time_now - time_stamp) >= 0.2:
            if (pulse == 6):
                money = 1
                print "Inserted 1kn"
                money = 0
                pulse = 0
            elif (pulse == 7):
                money = 2
                print "Inserted 2kn"
                money = 0
                pulse = 0
            elif (pulse == 8):
                money = 5
                print "Inserted 5kn"
                money = 0
                pulse = 0
            elif (pulse == 0):
                pulse = 0

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
