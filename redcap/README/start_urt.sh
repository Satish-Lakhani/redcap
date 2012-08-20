#!/bin/bash
killall -u XXXXXXXX -r ioUrTded #replace XXXXXXXX with your user name
screen -wipe
screen -A -m -d -S XXXXXXXX ./ioUrTded.i386 +set fs_game "q3ut4" +set dedicated 2 +set net_port 27960 +set com_hunkmegs 512 +set com_zonemegs 128 +exec server.cfg +map ut4_casa
if ps -ef | grep [R]edcap_110
then
exit 0
echo "RedCap Killed"
else
cd q3ut4/RC11/ #replace q3ut4/RC10/ with true path to S_prestart.sh file
./S_prestart.sh
fi