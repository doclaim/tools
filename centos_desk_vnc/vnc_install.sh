#!/bin/bash

sed -i 's/id:[0-9]/id:5/g' /etc/inittab
tail -n 1 /etc/inittab

echo "--------begin stall vnc-----------"
yum install -y *vnc*
[ ! -e /root/.vnc/xstartup ] && echo "vnc server not exists"
rm -rf /root/.vnc/xstartup && cp xstartup /root/.vnc/

vncserver -kill :1
vncserver :1

ps -aux|grep vnc
