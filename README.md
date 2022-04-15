# Yoga Pose Classification App
COSC 490 Final Project due 11 April 2022

Authors: Edouard Eltherington, Veronica Jack, Logan Parker, and Khai Hung Luong

## Table of Contents
* [General Information](#general-information)
* [Language and Modules](#language-and-modules)
* [Setup](#setup)
* [Walkthrough](#walkthrough)
* [Citations](#citations)

## General Information

Please view our [project proposal](https://github.com/edouarde1/Yoga-Pose-Classification/blob/main/documentation/Project%20Proposal.pdf) and [final report](https://github.com/edouarde1/Yoga-Pose-Classification/blob/main/documentation/Project-Report.pdf) to learn more about our application's development.

## Language and Modules
This application was created with the following language and module versions:

- Python 3.9.7
- streamlit 1.8.1
- tensorflow 2.7.0
- keras 2.7.0
- numpy 1.21.3
- opencv-python 4.5.5.64
- scikit-image 0.19.2
- urllib3 1.26.7

## Setup

#### Important: This version is compatible both on Windows and MacOS systems. Please note that this version has reduced performance due to Openpose integration on MacOS computers. If you are using a Windows computer is it highly recommended that you download this repo from the ‘window-only’ branch.

1. Before you get started, please ensure you have Python 3.7, PIP, and the modules listed above installed.

2. Download and Prepare OpenPose
    1. Download [openpose-1.7.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases/tag/v1.7.0) (portable version of OpenPose)
    2. Extract the folder `openpose` and move it into the `Yoga-Pose-Classification` app (*note: put inside not on the same level*).
    3. Download the [caffemodel](http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/body_25/) and place the file in "openpose/models/pose/body_25/"

3. Run the application, which will open the app your default web browser.

    ```
    cd src
    streamlit run main.py
    ```

## Walkthrough 

1. Home Screen 

![home-screen](https://user-images.githubusercontent.com/75917131/163100015-35d6bfe7-4d0b-443d-b740-39c9afaf1ba1.jpeg)

2. Select a pose 

![select-pose ](https://user-images.githubusercontent.com/75917131/163100029-277f4a50-3f4c-44c1-99b0-8bd19f8b3e1d.jpeg)

3. Attempt yoga pose, take a photo, and process image 

![user-upload-results ](https://user-images.githubusercontent.com/75917131/163100119-5f553a4f-d219-4367-a3b1-18b1da2c636f.jpeg)

# Citations
OpenPose models are taken from CMU-Perceptual-Computing-Lab/OpenPose for study purpose, link to the source repository: https://github.com/CMU-Perceptual-Computing-Lab/openpose
