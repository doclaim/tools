#!/bin/bash

[ -e /usr/bin/psdash ] && echo "psdash has installed already" && exit 1

pip install psdash

echo "expmle: psdash --log /var/log/psdash.log --log /var/log/mydb.log"
echo "visit: http://192.168.2.99:5000/"
