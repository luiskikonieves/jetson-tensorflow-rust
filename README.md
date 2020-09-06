# py-jetson

Repository for playing with a Jetson Nano. 


## Requirements

## Hardware

You will need the following hardware to run this project:

* [Jetson Nano Developer Kit](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
* [5V 4A power supply](https://www.amazon.com/gp/product/B07413Q5Y4/ref=as_li_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=B07413Q5Y4&linkCode=as2&tag=desertbot-20&linkId=785912983fcb0207e5d0940ebfca9423)
* J48 jumper
* [Raspberry Pi Camera Module v2](https://www.digikey.com/catalog/en/partgroup/raspberry-pi-camera-module-v2/63181?utm_adgroup=Programmers%20Dev&utm_source=google&utm_medium=cpc&utm_campaign=Dynamic%20Search_RLSA_Buyers&utm_term=&utm_content=Programmers%20Dev&gclid=Cj0KCQjwhb36BRCfARIsAKcXh6H0b37_zqrGRSlMun8dv3EY0uEGLlyEkfF78_dqaqqi8Fb2kC6oz9IaAtW8EALw_wcB) or equivalent
* Cat 5 or Wi-Fi connection

## Software

You will need the following software to run this project:

* [JetPack SDK for Jetson Nano](https://developer.nvidia.com/embedded/jetpack)
* Python packages listed in `requirements.txt` 

### Installing and Running Application

This program requires some other tools to be installed on the Jetson Nano. All of these can be installed
by running `scripts/provision.sh` on the Jetson Nano. 

This script will also create a systemd service which will automatically start the program upon boot and restart
the program upon crash. The program may be disabled by running `sudo systemctl --user disable camera-nano.service`.


