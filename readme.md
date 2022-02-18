# Arjuna Team - Shell Pitch the Future
## University of Indonesia

This Repository contain 2 major program ;
1. Drowsiness Detection - to detect drowsinesss and give command to chair to recline accordingly
2. Chair Curvature - to configure chair curvature automatically based on basic human feature

Both of these program requires a camera to be connected to the Computer. Make sure you set the Camera ID correctly so the program can run.

## Drowsiness Detection
This Repository contain custom configured drowsiness detection based on https://data-flair.training/blogs/python-project-driver-drowsiness-detection-system/.
This program detect the left eye and right eye using camera to measure drowsiness.

### Install
A suitable Python 3.x environment with a recent version of Tensorflow is required.
Development and testing was done with Conda Python 3.6.13 and Tensorflow 1.12.0 on Windows.

A conda environment setup is :
```
pip install opencv-contrib-python
pip install tensorflow
pip install pygame (to play warning sound)
```


## PoseNet Python - Chair Curvature Program

This repository contains a pure Python implementation (multi-pose only) of the Google TensorFlow.js Posenet model. For a (slightly faster) PyTorch implementation that followed from this, see (https://github.com/rwightman/posenet-pytorch)

### Install

A suitable Python 3.x environment with a recent version of Tensorflow is required.

Development and testing was done with Conda Python 3.6.13 and Tensorflow 1.12.0 on Windows with Anaconda.

If you want to use the webcam demo, a pip contrib version of opencv (`pip install opencv-contrib-python`) is required instead of the conda version. Anaconda's default opencv does not include ffpmeg/VideoCapture support.

A conda environment setup as below should suffice: 
```
conda install tensorflow-gpu scipy pyyaml python=3.6
pip install opencv-contrib-python
pip install pySerial

```

### Proteus

This Program can simulate the serial protocol communication between the running script and the microcontroller used to control the chair parameter, to simulate this, you should have :
```
Proteus 8 Provessional V 8.9 
Arduino UNO Library by TheEngineeringProject (https://www.theengineeringprojects.com/2015/12/arduino-library-proteus-simulation.html)
Virtual COM PORT (we used Eltima https://www.eltima.com/products/vspdxp/)
```
After opening the project, you have to set the HEX accordingly. Right Click the arduino -> Edit Properties -> edit program -> choose the *.standard.hex file
