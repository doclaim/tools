#!/bin/bash

path=$PWD
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
     echo "export PATH=$PATH:/usr/local/python2.7/bin/" >>/etc/profile
     /usr/bin/python -V
  }
}


function install_pip()
{
  cd $path
  [ -d setuptools-7.0 ] && rm -rf setuptools-7.0
  [ -d pip-1.4 ] && rm -rf pip-1.4
  tar -xzvf setuptools-7.0.tar.gz
  tar -xzvf pip-1.4.tar.gz
  setuptool='setuptools-7.0'
  /usr/bin/python $setuptool/setup.py install && chmod +x $setuptool/dist/*
  /bin/bash $setuptool/dist/*
  cd pip-1.4
  /usr/bin/python setup.py install && {
    [ -e /usr/bin/pip ] && rm -rf /usr/bin/pip
    ln -s /usr/local/python2.7/bin/pip /usr/bin/pip
    which pip
    echo "$pyname pip install finished"
  }
}

#install_py2_7_8
install_pip
