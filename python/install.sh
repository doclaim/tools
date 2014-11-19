#!/bin/bash
action=$1
name=$2
[ -z $action ] && action=-h
. /etc/rc.d/init.d/functions

function install_py2_7_8()
{
  [ -d /usr/local/python2.7 ] && echo 'python 2.7 has been installed' && exit 1
  #begin install
  cd Python-2.7.8
  ./configure --prefix=/usr/local/python2.7
  make && make install
  [ -d /usr/local/python2.7 -a -e /usr/local/python2.7/bin/python2.7 ] && {
     rm -rf /usr/bin/python
     cp /usr/local/python2.7/bin/python2.7 /usr/bin/python
     /usr/bin/python -V
  }
}

function install_pip()
{
  setuptool='setuptools-7.0'
  rm -rf $setuptool/dist/*
  daemon /usr/bin/python $setuptool/setup.py install && chmod +x $setuptool/dist/*
  /bin/bash $setuptool/dist/*
  cd pip-1.4
  /usr/bin/python setup.py install && {
    which pip
    echo "$pyname pip install finished"
  }
}
install_py2_7_8
install_pip
