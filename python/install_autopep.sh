#!/bin/bash

[ -e /usr/local/python2.7/bin/autopep8 ] && echo "autopep8 has installed already" && exit 1
pip install autopep8
echo "example: find . -type f -name "*.py" | xargs autopep8 -i --aggressive"
