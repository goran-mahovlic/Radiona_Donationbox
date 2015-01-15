# Radiona_Donationbox
DonationBox for Radiona

DonationBox shoud be something like phisical crowd founding.

On donationbox we have computer(rasp or beaglebone) display (small or big) and two buttons.

Small lcd
http://www.ebay.com/itm/3-5-Inch-TFT-LCD-Display-2-CH-Video-Input-Monitor-New-Car-Rear-View-DVD-Monitor-/171452888466?pt=LH_DefaultDomain_0&hash=item27eb637592
You can change font size on this small lcd so you can see text
http://www.raspberrypi-spy.co.uk/2012/11/cheap-miniature-lcd-screen/

On button press, project on screen change, and user can add money to selected project.

You will need to add pictures, and sounds for this project.

Movies could be added in future versions.

You will need to program your coin selector to accept your coins
https://www.sparkfun.com/products/11719
Do not connect coin selector directly on rasp, con selector on pulse pin has 5V output, rasp can only handle 3.3V
Schematics for lowering voltage will be available soon...

donationbox.py saves money in sqlite database, update money shoud be added to update money on remote myssql database so data could be available from internet.

Currently only working on raspberry, support for beaglebone will be added soon.

In examples folder will be simple python programs that are used in creation of donationbox (press button, show picture, play movie, write to sqlite database ...)
