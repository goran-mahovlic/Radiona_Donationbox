
###############################################################
# Radiona Donation box V1.0                                   #
# database for money log sqlite3                              #
# graphics by pygame (SDL) no need for X system               #
# GPIO interrupts for raspberry                               #
# support tu run on beagle bone black                         #
# prepared for windows version                                #
# coud be prepared to run on every linux system               #
#                                                             #
# by Goran Mahovlic                                           #
###############################################################

import sys
import os
import threading
import sqlite3
from datetime import datetime, date

CheckOS = os.uname()[1]

if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5: 
# condi. and
# On NT like Windows versions smpeg video needs windb.
    print "Your system is Windows"
    os.environ['SDL_VIDEODRIVER'] = 'windib'
elif CheckOS.find('beaglebone') == 0:
    print "Your system is Beagle Bone Black"
elif CheckOS.find('raspberry') == 0:
    print "Your system is Raspberry Pi"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)

import time 
import pygame
from time import gmtime, strftime
from pygame.locals import *

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from pygame.compat import unicode_

pygame.init()

time_stamp = time.time()
pulse = 0
money = 0
project = 0
projectChanged = False
pwm = 0

#Checking system version , setting communication, on linux creating database if not exist, creating tables if not exist
if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
    screen = pygame.display.set_mode((800, 600))
    print "No sqlite logging in windows implemented yet"
elif CheckOS.find('beaglebone') == 0 or CheckOS.find('raspberry') == 0:   
    # run on beagle and rasp
    print "Running this part of code on rasp and BBB"
    size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    if os.path.isfile('/home/donationbox/donationboxDatabase.sqlite'):
        conn = sqlite3.connect("/home/donationbox/donationboxDatabase.sqlite",detect_types=sqlite3.PARSE_DECLTYPES) 
        print ("Database exist")
        conn.close()
    else:
        conn = sqlite3.connect("/home/donationbox/donationboxDatabase.sqlite",detect_types=sqlite3.PARSE_DECLTYPES)
        print ("Database created")
        conn.execute("CREATE TABLE money(id INTEGER PRIMARY KEY,date TEXT, time TEXT, inserted INTEGER, project INTEGER)")
        print("Table money for project created")
        conn.close()        
    if CheckOS.find('raspberry') == 0:
        # this shoud run only on raspberry
        # GPIO 17 & 23 & 24 set up as inputs, pulled up to avoid false detection.
        # GPIO 25 set up as output
        # Both ports are wired to connect to GND on button press.
        # So we'll be setting up falling edge detection for all
        print "Run this part code of code only on rasp"
        # Shoud run only on raspberry
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(25, GPIO.OUT) # set GPIO 25 as output
        # Blink LED
        GPIO.output(25,True) ## Turn on GPIO pin 25
        time.sleep(1)
        GPIO.output(25,False) ## Turn on GPIO pin 25
        # LED dimm
        led = GPIO.PWM(25, 100)  # create object led for PWM on port 25 at 100 Hertz 
        led.start(0)             # start led on 0 percent duty cycle (off)  
        # In code just call led.ChangeDutyCycle(pwm) to setup pwm 
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
            global project
            global pwm
            global projectChanged
#            print "falling edge detected on 23"
        # go to next project
            if pwm < 76:
                pwm = pwm + 15
                led.ChangeDutyCycle(pwm)
                print pwm
            if (project < 5):
                project = project + 1
                projectChanged = True
            elif(project == 0):
                project = project + 1
                projectChanged = True
        
        def my_callback3(channel):
            global project
            global pwm
            global projectChanged
#            print "falling edge detected on 24"
            if pwm > 14:
                pwm = pwm - 15
                led.ChangeDutyCycle(pwm)
                print pwm
            if (project > 0):
                project = project - 1
                projectChanged = True
            elif(project == 0):
                project = project + 1
                projectChanged = True

        # when a falling edge is detected on port 17, regardless of whatever 
        # else is happening in the program, the function my_callback will be run
        GPIO.add_event_detect(17, GPIO.FALLING, callback=my_callback, bouncetime=50)
        # when a falling edge is detected on port 23 & 24, regardless of whatever 
        # else is happening in the program, the function my_callback2 will be run
        # 'bouncetime=300' includes the bounce control written into interrupts2a.py
        GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callback2, bouncetime=300)
        GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callback3, bouncetime=300)

    elif CheckOS.find('beaglebone') == 0:
        #Shoud run only on beaglebone
        print "No GPIO on Beagle Bone Black implemented yet"
        
#Setting up pygame, loading pictures, sound, setting fonts
print "Run this part of code on All systems"
pygame.display.set_caption('DonationBox for Radiona projects')
pygame.mouse.set_visible(0)
pygame.mixer.quit()
pygame.mixer.init(44100, -16,2,2048)

projectWelcomeImage = pygame.image.load("/home/donationbox/Pictures/projectWelcomeImage.png") 
projectOneImage = pygame.image.load("/home/donationbox/Pictures/projectOneImage.png")
projectTwoImage = pygame.image.load("/home/donationbox/Pictures/projectTwoImage.png")
projectThreeImage = pygame.image.load("/home/donationbox/Pictures/projectThreeImage.png")
projectFourImage = pygame.image.load("/home/donationbox/Pictures/projectFourImage.png")
projectFiveImage = pygame.image.load("/home/donationbox/Pictures/projectFiveImage.png")

projectWelcomeSound = pygame.mixer.Sound("/home/donationbox/Sound/projectWelcomeSound.wav")
projectOneSound = pygame.mixer.Sound("/home/donationbox/Sound/projectOneSound.wav")
projectTwoSound = pygame.mixer.Sound("/home/donationbox/Sound/projectTwoSound.wav")
projectThreeSound = pygame.mixer.Sound("/home/donationbox/Sound/projectThreeSound.wav")
projectFourSound = pygame.mixer.Sound("/home/donationbox/Sound/projectFourSound.wav")
projectFiveSound = pygame.mixer.Sound("/home/donationbox/Sound/projectFiveSound.wav")

font=pygame.font.SysFont("verdana", 70)

#Setting varibles
font.set_bold(False)
font.set_italic(True)
blackColor = 0,0,0

def getMoneyForProject(money_project):
    if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
        print ("No log on windows")
    elif sys.platform == 'linux2':
        conn = sqlite3.connect("/home/donationbox/donationboxDatabase.sqlite",detect_types=sqlite3.PARSE_DECLTYPES) 
        cursor = conn.cursor() 
        cursor.execute("SELECT sum(inserted) FROM (SELECT id,inserted,project FROM money WHERE project = ('" + str(money_project) + "'))")
        money_in_project = cursor.fetchone()
        conn.close
        print "For project:" + str(money_project) + " we have collected:" + str(money_in_project).strip( ')(,' ) + "kn"
    return str(money_in_project).strip( ')(,' )

# open database insert money for project into database		
def sendToDatabase(ProjectMoney,CurrentProject):
    if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
        print ("No log on windows")
    elif sys.platform == 'linux2':
        conn = sqlite3.connect("/home/donationbox/donationboxDatabase.sqlite",detect_types=sqlite3.PARSE_DECLTYPES) 
        conn.execute("INSERT INTO money(date,time,inserted,project) values(?,?,?,?)", ((time.strftime("%Y-%m-%d")),(time.strftime("%H:%M:%S")),ProjectMoney,CurrentProject))
#        print "Inserting into database: " + time.strftime("%Y-%m-%d"),(time.strftime("%H:%M:%S"),ProjectMoney,CurrentProject 
        conn.commit()
        conn.close()

def sendToText(text):
    text_file = open("/home/donationbox/donationbox.log", "a")
    text_file.write(str(text))
    
def checkKeyboard():
    global projectChanged
    global project
    global money
    for event in pygame.event.get():
        #sendToText(event.type)
        if (event.type == QUIT):
            pygame.quit()
            sys.exit()
            done = True
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                done = True    
            elif (event.key == K_1):
                sendToDatabase(money,project)
            elif (event.key == K_2):
                sendToDatabase(money,project)
            elif (event.key == K_5):
                sendToDatabase(money,project)
            elif (event.key == K_KP_MINUS):
                if (project > 1):
                    project = project - 1
                    projectChanged = True
                elif(project == 0):
                    project = project + 1
                    projectChanged = True
            elif (event.key == K_KP_PLUS):
                if (project < 5):
                    project = project + 1
                    projectChanged = True
                elif(project == 0):
                    project = project + 1
                    projectChanged = True
            else:
                print event.key
             
def checkMoney():
    time_now = time.time()
    global money
    global pulse
    global projectChanged
    if (time_now - time_stamp) >= 0.2:
        if (pulse == 6):
            money = 1
            sendToDatabase(money,project)
            print "Ubacili ste 1kn"
            projectChanged = True
            money = 0
            pulse = 0
        elif (pulse == 7):
            money = 2
            sendToDatabase(money,project)
            print "Ubacili ste 2kn"
            projectChanged = True
            money = 0
            pulse = 0
        elif (pulse == 8):
            money = 5
            sendToDatabase(money,project)
            print "Ubacili ste 5kn"
            projectChanged = True
            money = 0
            pulse = 0
        elif (pulse == 0):
            pulse = 0
                
def checkProject():
    global project
    global projectChanged
    global blackColor
    if (project == 0):
        screen.fill((255,255,255))
        screen.blit(projectWelcomeImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(0)) + "kn",blackColor)
        pygame.display.flip()
        projectWelcomeSound.play()
        time.sleep(1)
        projectWelcomeSound.stop()  
        projectChanged = False        
    elif (project == 1):
        screen.fill((255,255,255))
        screen.blit(projectOneImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(1)) + "kn",blackColor)
        pygame.display.flip()
        projectOneSound.play()
        time.sleep(1)
        projectOneSound.stop()           
        projectChanged = False       
    elif (project == 2):
        screen.fill((255,255,255))
        screen.blit(projectTwoImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(2)) + "kn",blackColor)
        pygame.display.flip()
        projectTwoSound.play()
        time.sleep(1)
        projectTwoSound.stop()           
        projectChanged = False           
    elif (project == 3):
        screen.fill((255,255,255))
        screen.blit(projectThreeImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(3)) + "kn",blackColor)
        pygame.display.flip()
        projectThreeSound.play()
        time.sleep(1)
        projectThreeSound.stop()               
        projectChanged = False       
    elif (project == 4):   
        screen.fill((255,255,255))
        screen.blit(projectFourImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(4)) + "kn",blackColor)
        pygame.display.flip()
        projectFourSound.play()
        time.sleep(1)
        projectFourSound.stop()           
        projectChanged = False
    elif (project == 5):    
        screen.fill((255,255,255))
        screen.blit(projectFiveImage,(0,0))
        text_trenutno("Trenutno: " + str(getMoneyForProject(5)) + "kn",blackColor)
        pygame.display.flip()
        projectFiveSound.play()
        time.sleep(1)
        projectFiveSound.stop()           
        projectChanged = False
        
def text_trenutno(score,fontColor):
   scoretext=font.render(str(score), 1,fontColor)
   screen.blit(scoretext, (10, 10))
   
screen.fill((255,255,255))
screen.blit(projectWelcomeImage,(0,0))
text_trenutno(getMoneyForProject(0),blackColor)
pygame.display.flip()
projectWelcomeSound.play()
time.sleep(1)
projectWelcomeSound.stop()      
   
try:
    while True:
        checkMoney()
        checkKeyboard()
        if (projectChanged):       
            checkProject()

except KeyboardInterrupt:
    if CheckOS.find('raspberry') == 0:
        led.stop()
        GPIO.cleanup()       # clean up GPIO on CTRL+C exit shoud be added only on rasp
      
if CheckOS.find('raspberry') == 0:
    led.stop()
    GPIO.cleanup()           # clean up GPIO on normal exit shoud be added only on rasp
