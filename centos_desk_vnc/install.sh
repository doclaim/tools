#!/bin/bash

err="install failure"
exists=`yum grouplist|grep Desktop &>/dev/null;echo $?`
[ $exists -eq 0 ] && echo "Desktop has installed already" && exit 1

echo "--------begin install desktop-----------"
yum groupinstall -y   "Desktop"   "Desktop Platform"   "Desktop Platform Development"　 "Fonts" 　"General Purpose Desktop"　 "Graphical Administration Tools"　 "Graphics Creation Tools" 　"Input Methods" 　"X Window System" 　"Chinese Support [zh]"　"Internet Browser"


[ $? -ne 0 ] && echo $err && exit 1

sed -i 's/id:[0-9]/id:5/g' /etc/inittab
tail -n 1 /etc/inittab

[ $? -ne 0 ] && echo $err && exit 1

echo "--------begin stall vnc-----------"
yum install -y *vnc*
[ ! -e /root/.vnc/xstartup ] && echo "vnc server not exists"
rm -rf /root/.vnc/xstartup && cp xstartup /root/.vnc/

vncserver -kill :1
vncserver :1

ps -aux|grep vnc



