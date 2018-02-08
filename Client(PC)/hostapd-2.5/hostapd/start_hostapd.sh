#!/bin/bash
#sudo restart networking
#sudo nmcli nm wifi off
#sudo rfkill unblock wlan

ifconfig wlan0 down
ifconfig wlan0 10.10.0.1/24 up
sleep 1

service isc-dhcp-server restart
./hostapd ./hostapd.conf
