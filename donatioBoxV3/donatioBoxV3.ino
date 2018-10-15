/*
  _____                    _   _             ____          __      ______
 |  __ \                  | | (_)           |  _ \         \ \    / /___ \
 | |  | | ___  _ __   __ _| |_ _  ___  _ __ | |_) | _____  _\ \  / /  __) |
 | |  | |/ _ \| '_ \ / _` | __| |/ _ \| '_ \|  _ < / _ \ \/ /\ \/ /  |__ <
 | |__| | (_) | | | | (_| | |_| | (_) | | | | |_) | (_) >  <  \  /   ___) |
 |_____/ \___/|_| |_|\__,_|\__|_|\___/|_| |_|____/ \___/_/\_\  \/   |____/

 Description: DonationBoxV3 box for presentation and exibitions - users can donate money or likes
 
 Based on Heltec esp32 wifi-lora-32 board
 
 [x] Left button is to get random project
 [x]Right button is to Like project
 [ ] If you insert money it will be noted  to selected project
 [ ] Sends changes(in money and likes) to TTN network over LoRa
 [ ] sounds, and 
 [ ] game play if money is inserted...

 Version: 1.03 

 License: FreeBSD

 Maintainer: Goran Mahovlić

 by: Radiona.org

*/

#include "inc/includes.h"

//here you define how many project you have
#define NO_PROJECTS 4
     
    void setup() {
      //interrupt every 100ms to check pins
      setupTimers();

      // Setup pins
      setupAllPins();
      
      Serial.begin(115200);
      Serial.println("Started");

      // init LCD
      setupLCD();
      
      // LMIC init
      os_init();
      // setupLoRa
      setupLoRa();

      // Start check for project change - change picture - send serial 
      do_check(&checkjob);
      
      // Start LoRa send job (sending automatically starts OTAA too)
      do_send(&sendjob);

    }
     
    void loop() {
      os_runloop_once();
}

