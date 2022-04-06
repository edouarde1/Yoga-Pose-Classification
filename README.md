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

## General Information

Purpose of the project (TODO)

Please view our [report]() to learn more about how our app was developed (TODO)

## Language and Modules
This application was created with the following language and module versions:

- Python 3.9.7
- streamlit 1.8.1

<br>

## Setup
1. Before you get started, please ensure you have Python 3.7 and PIP and have the modules installed using the resources below:

    * Streamlit [install instructions](https://docs.streamlit.io/library/get-started/installation)

        ```
        pip install streamlit
        ```

    * OpenPose
        1. Download [openpose-1.7.0](https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases)
        2. Extract the folder `openpose` and move to the same directory as the `Yoga-Pose-Classification` app.
        3. Download [caffemodel](https://www.kaggle.com/datasets/changethetuneman/openpose-model?select=pose_iter_584000.caffemodel)
        4. Move `pose_iter_584000.caffemodel` to `openpose\models\pose\body_25`

3. TODO

4. Run the application

    ```
    cd src
    streamlit run main.py
    ```

## Additional Information
TODO
