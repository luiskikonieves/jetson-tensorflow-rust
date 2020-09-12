#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "You must login as root to execute this script."
   exit 1
fi

echo 'Upgrading device.'

sudo apt-get update

sudo apt full-upgrade -y

echo 'Downloading packages.'

# Required packages for TensorFlow:
sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran -y

# Install pip3
sudo apt-get install python3-pip -y
yes | sudo pip3 install -U pip testresources setuptools

# Python package dependencies
yes | sudo pip3 install -U pip testresources setuptools numpy==1.16.1 future==0.17.1 mock==3.0.5 h5py==2.9.0 keras_preprocessing==1.0.5 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11
# $ sudo pip3 install -U numpy==1.16.1 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11

# TF-2.2
yes | sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v44 tensorflow==2.2.0+nv20.7

# Install program's requirements
yes | sudo pip3 install -r ../requirements.txt

# Remove deprecated packages
sudo apt auto-remove -y

# Create the service
echo 'Creating systemd service.'

{
  echo '[Unit]'
  echo 'Description=Object detection service that streams on the network'
  echo ''
  echo '[Service]'
  echo 'ExecStart=/usr/bin/camera_nano.py'
  echo 'Restart=on-failure'
  echo 'RestartSec=5'
  echo 'User=jetson'
  echo ''
  echo '[Install]'
  echo 'WantedBy=default.target'
} | sudo tee /lib/systemd/system/camera-nano.service

sudo chown root:root /lib/systemd/system/camera-nano.service
sudo chmod 644 /lib/systemd/system/camera-nano.service
sudo systemctl --user enable camera-nano.service

sync

echo
echo 'Updates complete. Please reboot.'
echo
