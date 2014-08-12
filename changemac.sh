#!/bin/bash

echo -e "Enter new MAC address: \c"
read mac
/etc/init.d/networking stop
ifconfig wlan0 down
ifconfig wlan0 hw ether $mac
ifconfig wlan0 up
/etc/init.d/networking start
ifconfig wlan0
