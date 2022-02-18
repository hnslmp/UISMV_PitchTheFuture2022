## PoseNet Python

This repository contains a pure Python implementation (multi-pose only) of the Google TensorFlow.js Posenet model. For a (slightly faster) PyTorch implementation that followed from this, see (https://github.com/rwightman/posenet-pytorch)

### Install

A suitable Python 3.x environment with a recent version of Tensorflow is required.

Development and testing was done with Conda Python 3.6.8 and Tensorflow 1.12.0 on Linux.

Windows 10 with the latest (as of 2019-01-19) 64-bit Python 3.7 Anaconda installer was also tested.

If you want to use the webcam demo, a pip version of opencv (`pip install opencv-python`) is required instead of the conda version. Anaconda's default opencv does not include ffpmeg/VideoCapture support. Also, you may have to force install version 3.4.x as 4.x has a broken drawKeypoints binding.

A conda environment setup as below should suffice: 
```
conda install tensorflow-gpu scipy pyyaml python=3.6
pip install opencv-python==3.4.5.20

```
