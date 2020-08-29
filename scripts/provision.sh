#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "You must login as root to execute this script."
   exit 1
fi

echo 'Upgrading device.'

sudo apt-get update

sudo apt full-upgrade -y

echo 'Downloading packages.'

sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran

sudo apt-get install python3-pip

sudo pip3 install -U pip

sudo pip3 install -U pip testresources setuptools numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11

# TF-2.x
$ sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow==2.2.0+nv20.7
