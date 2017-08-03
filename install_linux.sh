#! /bin/bash

# Install everything that is in apt
sudo apt-get install -y git
sudo apt-get install -y python-numpy
sudo apt-get install -y python-scipy
sudo apt-get install -y python-matplotlib
sudo apt-get install -y python-qt4
sudo apt-get install -y python-skimage
sudo apt-get install -y python-vtk

# Install everything that is in pip
sudo pip install fipy
sudo pip install solidpython
sudo pip install numpy-stl
sudo pip install wget

# Clone PyFRAP and install
sudo python setup.py install --gmsh --fiji

 


