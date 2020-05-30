#!/bin/bash
sleep 5
echo "\n"
echo "imap-smtp interface monitor started"
echo "\n"
sleep 20
while true; do
sleep 30
res=$(ps -aux|grep "python3 /home/pi/sentinair/imap-smtp-interface.py" -i|grep -v grep)
#echo "$res"
if [ "$res" = "" ]; then
sleep 10
python3 /home/pi/sentinair/imap-smtp-interface.py restart
fi
done
