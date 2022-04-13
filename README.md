# Yoga Pose Classification App
COSC 490 Final Project due 11 April 2022

Authors:
    Veronica Jack
    Edouard Eltherington
    Logan Parker
    Khai Luong

## Table of Contents
* [General Information](#general-information)
* [Language and Modules](#language-and-modules)
* [Setup](#setup)
* [Additional Information](#additional-information)
* [Citations](#citations)

## General Information

Please view our [report](https://github.com/edouarde1/Yoga-Pose-Classification/blob/main/documentation/Project-Report.pdf) to learn more about how our app was developed

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
1. Before you get started, please ensure you have Python 3.7, PIP, and the modules listed above installed.

2. Download and Prepare OpenPose 
    - For Window User:
        1. Download [openpose-1.7.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases/tag/v1.7.0) (portable version of OpenPose)
        2. Extract the folder `openpose` and move it into the `Yoga-Pose-Classification` app (*note: put inside not on the same level*).
        3. Double click on `openpose/models/getBaseModels.bat` to download the required models for image rendering
    - For Mac User:
        1. Download [openpose-1.7.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases/tag/v1.7.0) (portable version of OpenPose)
        2. Extract the folder `openpose` and move it into the `Yoga-Pose-Classification` app (*note: put inside not on the same level*).
        3. Download the caffemodel from this [link](https://www.kaggle.com/datasets/changethetuneman/openpose-model?select=pose_iter_584000.caffemodel) and put it inside this path "openpose/models/pose/body_25"


3. Run the application, which will open your web browser.

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


# Yoga Pose Classification App
COSC 490 Final Project

Authors:
- Veronica Jack
- Edouard Eltherington
- Logan Parker
- Khai Hung Luong

# Source Citation
OpenPose models are taken from CMU-Perceptual-Computing-Lab/OpenPose for study purpose, link to the source repository: https://github.com/CMU-Perceptual-Computing-Lab/openpose

## Additional Information
TODO

## Citations
TODO
