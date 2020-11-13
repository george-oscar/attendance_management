#!/bin/bash
# Raspberry Pi OS with desktop 2020-08-20

# install apt package
apt_get_install(){
	sudo apt update
	sudo apt upgrade -y
	sudo apt install -y build-essential cmake pkg-config
	sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng-dev
	sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
	sudo apt install -y libxvidcore-dev libx264-dev
	sudo apt install -y libatlas-base-dev gfortran
	sudo apt install -y libhdf5-dev libhdf5-serial-dev libhdf5-103
	sudo apt install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
	sudo apt install -y python3-dev
	sudo apt clean
}

# install Open CV
install_opencv(){
	sudo -E python3 -m pip install -upgrade pip
	sudo -E pip3 install -U setuptools
	sudo -E pip3 --default-timeout=1000 install opencv-python==4.0.1.24
	sudo -E pip3 install opencv-contrib-python==4.0.1.24
}

install_dlib(){
	sudo sed -i -e "s/^CONF_SWAPSIZE=.*/CONF_SWAPSIZE=1024/g" /etc/dphys-swapfile
	cat /etc/dphys-swapfile | grep CONF_SWAPSIZE
	sudo service dphys-swapfile restart
	mkdir -p dlib
	git clone -b 'v19.6' --single-branch https://github.com/davisking/dlib.git dlib/
	cd ./dlib
	sudo python3 setup.py install --compiler-flags "-mfpu=neon"
	sudo -E pip3 install face_recognition
	sudo service dphys-seapfile stop
	sudo sed -i -e "s/CONF_SWAPSIZE=1024/CONF_SWAPSIZE=128/g" /etc/dphys-swapfile
	cat /etc/dphys-swapfile | grep CONF_SWAPSIZE
	sudo service dphys-swapfile restart
}


START_TIME=`date +%s`

# change directory here
cd `dirname $0`

apt_get_install
install_opencv
install_dlib

END_TIME=`date +%s`

SS=`expr ${END_TIME} - ${START_TIME}`
HH=`expr ${SS} / 3600`
SS=`expr ${SS} % 3600`
MM=`expr ${SS} / 60`
SS=`expr ${SS} % 60`

echo "Total Time(Setup OpenCV): ${HH}:${MM}:${SS} (h:m:s)"
