#!/bin/bash

echo -e "Enter new MAC address: \c"
read mac
/etc/init.d/networking stop
ifconfig wlan1 down
ifconfig wlan1 hw ether $mac
ifconfig wlan1 up
/etc/init.d/networking start
ifconfig wlan1
