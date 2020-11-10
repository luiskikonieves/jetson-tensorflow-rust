#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "You must login as root to execute this script."
   exit 1
fi

# Create a user to run the service
USERNAME=jetson
echo 'Username: '$USERNAME

echo 'Updating device.'
sudo apt-get update
sudo apt full-upgrade -y

echo 'Downloading packages.'
sudo apt-get install git cmake -y
sudo apt-get install libpython3-dev python3-numpy python3-pip -y
# Install pip3
yes | sudo pip3 install -U pip testresources setuptools
# Install program's requirements
yes | sudo pip3 install -r ../requirements.txt

# Install PyTorch
echo 'Installing PyTorch.'
wget https://nvidia.box.com/shared/static/wa34qwrwtk9njtyarwt5nvo6imenfy26.whl -O torch-1.7.0-cp36-cp36m-linux_aarch64.whl
pip3 install Cython
sudo apt install libjpeg-dev libfreetype6-dev libpng-dev libopenblas-base libopenmpi-dev
pip3 install numpy torch-1.7.0-cp36-cp36m-linux_aarch64.whl

git clone --branch v0.8.1 https://github.com/pytorch/vision torchvision
cd torchvision
export BUILD_VERSION=0.8.1
sudo python3 setup.py install
# ??? Why do the nvidia instructions need this????
# cd ../

cd /home/$USERNAME/python-envs/env/lib/python3.6/site-packages

if id -u $USERNAME > /dev/null 2>&1;
then
    echo "User exists: $USERNAME"
else
    echo "Adding user $USERNAME"

    sudo useradd -s /bin/bash -m -U $USERNAME
    sudo addgroup $USERNAME sudo > /dev/null 2>&1
fi

# Create the service
echo 'Creating systemd service.'

{
  echo '[Unit]'
  echo 'Description=Object detection service that streams on the network'
  echo ''
  echo '[Service]'
  echo 'ExecStart='$PWD'/camera_nano.py'
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

# Remove deprecated packages
echo 'Cleaning up.'
sudo apt auto-remove -y

echo
echo 'Updates complete. Rebooting'
sudo reboot
