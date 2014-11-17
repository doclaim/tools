#!/bin/bash

err="install failure"
exists=`yum grouplist|grep Desktop &>/dev/null;echo $?`
[ $exists -eq 0 ] && echo "Desktop has installed already" && exit 1

echo "--------begin install desktop-----------"
yum groupinstall -y   "Desktop"   "Desktop Platform"   "Desktop Platform Development"　 "Fonts" 　"General Purpose Desktop"　 "Graphical Administration Tools"　 "Graphics Creation Tools" 　"Input Methods" 　"X Window System" 　"Chinese Support [zh]"　"Internet Browser"


[ $? -ne 0 ] && echo $err && "echo ----------success install desktop" && exit 0




