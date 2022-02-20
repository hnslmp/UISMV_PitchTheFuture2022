# Arjuna Team - Shell Pitch the Future
![alt text](https://github.com/hnslmp/UISMV_PitchTheFuture2022/blob/main/Docs/UISMV%20Logo.png)   
## University of Indonesia

## I.Introduction
This Repository contain 2 major program for Universitas Indonesia Arjuna Team Pitch The Future 2022 idea;
1. Drowsiness Detection - to detect drowsinesss and give command to chair to recline accordingly
2. Chair Curvature - to configure chair curvature automatically based on basic human feature

Both of these program requires a camera to be connected to the Computer. Make sure you set the Camera ID correctly so the program can run.

You can download our written report [here](https://github.com/hnslmp/UISMV_PitchTheFuture2022/blob/main/Docs/Written%20Report.pdf)

## II.Major Features
- **Drowsiness Detection**: This program detect the left eye and right eye using camera to measure drowsiness. If the driver is considered drowsy, the seat will adjust itself so that the passenger can rest
- **Chair Curvature Detection**: This program detect the posture and size of the passenger's body and adjust the passenger seat to be comfortable according to ergonomic standards

## III. Requirements
- Tensorflow
- Pygame
- OpenCV (Contrib Version)
- Scipy
- Pyyaml
- pySerial

## IV.Installation

## Prepare Environment
Create a conda virtual environment with tensorflow and activate it.
```
conda create -n arjunaptf python=3.6.13 tensorflow-gpu 
conda activate arjunaptf
```

## Install Drowsiness Detection Requirements
This Repository contain custom configured drowsiness detection based on [Data FLair Driver Drowsiness Detection System](https://data-flair.training/blogs/python-project-driver-drowsiness-detection-system/).

A suitable Python 3.x environment with a recent version of Tensorflow is required.
Development and testing was done with Conda Python 3.6.13 and Tensorflow 1.12.0 on Windows.

Install the following packages :
```
pip install opencv-contrib-python
pip install tensorflow (if you didnt create the environment with tensorflow)
pip install pygame (to play warning sound)
pip install pillow
```
Then run the program by running :
```
drowsiness_detection.py
```
Youtube Demo link : https://www.youtube.com/watch?v=S5CbaeaB6aM

## Install PoseNet Python - Chair Curvature Program

This repository contains a pure Python implementation (multi-pose only) of the Google TensorFlow.js Posenet model. For a (slightly faster) PyTorch implementation that followed from this, see [posenet here](https://github.com/rwightman/posenet-pytorch)

Install the following packages:
```
pip install scipy
pip install pyyaml
pip install opencv-contrib-python
pip install pySerial
```
Then Print the aruco marker and place it near your desired target (seatbelt for example). The aruco file is in the aruco folder and .pdf with name:
```
ArucoMarker.pdf
```
Note that the marker had to be exactly 5 Centimeter x 5 Centimeter (or by printing it without scaling).

Then run the program by running :
```
webcam_demo.py
```
Youtube Demo link : https://youtu.be/xjfZCjrtiTw

Development and testing was done with Conda Python 3.6.13 and Tensorflow 1.12.0 on Windows with Anaconda.

If you want to use the webcam demo, a pip contrib version of opencv (`pip install opencv-contrib-python`) is required instead of the conda version. Anaconda's default opencv does not include ffpmeg/VideoCapture support.


## Proteus (For Simulation)
This Program can simulate the serial protocol communication between the running script and the microcontroller used to control the chair parameter, to simulate this, you should have :
```
Proteus 8 Provessional V 8.9 
Arduino UNO Library by TheEngineeringProject (https://www.theengineeringprojects.com/2015/12/arduino-library-proteus-simulation.html)
Virtual COM PORT (we used Eltima https://www.eltima.com/products/vspdxp/)
```
After opening the project, you have to set the HEX accordingly. Right Click the arduino -> Edit Properties -> edit program -> choose the *.standard.hex file
