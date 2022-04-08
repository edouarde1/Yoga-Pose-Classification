import os
import time

import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
import urllib.request
from PIL import Image
from skimage import transform
from proc import save_img, render_img

# TODO: Use Python tempfile instead
USER_IMG = "images/temp.jpg"
PROC_IMG = "images/temp_rendered.png"


def get_md_as_string(path):
    url = "https://raw.githubusercontent.com/edouarde1/Yoga-Pose-Classification/main/documentation/" + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = tf.keras.models.load_model("../models/" + model_name, compile=False)  # removed compile=False
    return model


def run_app(original_img):
    with st.spinner("Processing image..."):
        # Convert user image to rendered image
        render_img()
        # check if openpose has finished rendering the image
        while not os.path.exists(PROC_IMG) and os.path.exists(USER_IMG):
            time.sleep(1)

        # Process rendered img for model
        rendered_img = Image.open(PROC_IMG)
        display_pictures(original_img, rendered_img)
        processed_image = np.array(rendered_img).astype('float32') / 255
        processed_image = transform.resize(processed_image, (256, 256, 3))
        processed_image = tf.expand_dims(processed_image, axis=0)

    # Load Model
    model = load_model("efficientnet_pretrain1_openpose")  # TODO: Update model name

    # Classify pose
    predictedvalues = model.predict(processed_image)
    predicted = np.argmax(predictedvalues, axis=1)

    # Define labels
    labels = ['Cow-Face', 'Extended-Hand-to-Big-Toe-Pose', 'Half-Lord-of-the-Fishes-Pose',
              'Half-Moon-Pose', 'Warrior-I-', 'Dancer', 'Extended-Triangle', 'Fire-Log', 'Goddess',
              'Lotus', 'Revolved-Side-Angle', 'Tree-Pose', 'Upward-Salute', 'Warrior-II']
    # See terminal for debugging
    print("SHAPE: " + str(predictedvalues.shape))
    print("VALS: " + str(predictedvalues))
    print("PRED: " + str(predicted))
    print("LABEL: " + str(labels[predicted[0]]))

    display_results(labels[predicted[0]])

    # TODO: Use Python tempfile instead to ensure user image is ALWAYS deleted
    os.remove(USER_IMG)
    os.remove(PROC_IMG)


# Show original vs. processed images
def display_pictures(original, processed):
    left_col, right_col = st.columns(2)
    left_col.image(original, caption="Original Image")
    right_col.image(processed, caption="Processed Image")


# TODO: determine how we want to display results
def display_results(results):
    st.write("Your pose was classified as: " + str(results))
    if pose_choice == 'Choose a pose':
        st.write("You have not chose any model pose. Please pick one from the select box above.")
    elif pose_choice == str(results):
        st.write("Congratulation! You have correctly done the pose")
    else:
        st.write("Your pose is not correct. Please try again.")


# Main Page Info
st.title('Yoga Pose Classification App')
st.write(" ------ ")

# SIDEBAR
st.sidebar.title("Yoga Pose Classification App")
st.sidebar.write(" ------ ")

sidebar_menu = ['Project Info', 'Practice Yoga', 'About Us']
sidebar_choice = st.sidebar.selectbox('Menu', sidebar_menu)

st.sidebar.write(" ------ ")
st.sidebar.write("Last updated: 30 March 2022")  # TODO: update

# MENU = PROJECT INFO
if sidebar_choice == sidebar_menu[0]:
    st.write(get_md_as_string("project-info.md"))

# MENU = PRACTICE YOGA
if sidebar_choice == sidebar_menu[1]:

    # Provide users more instructions
    with st.expander("Instructions"):
        st.write("First, choose a pose that you want to practice for example image of that pose.")
        st.write("Second, take a picture or upload an image of yourself doing that pose.")
        st.write("Finally, click `Process` to run our model.")
        st.write("*Tip: For pose that have facing direction (left or right), you can do in either direction.")

    # Add pose options
    st.subheader("Choose a Yoga Pose")
    poses = ['Choose a pose', 'Cow-Face', 'Extended-Hand-to-Big-Toe', 'Half-Lord-of-the-Fishes',
             'Half-Moon', 'Warrior-I', 'Dancer', 'Extended-Triangle', 'Fire-Log', 'Goddess',
             'Lotus', 'Revolved-Side-Angle', 'Tree', 'Upward-Salute', 'Warrior-II']
    pose_choice = st.selectbox('Select the pose you want to practice', poses)

    for pose in poses:
        if pose_choice == 'Choose a pose':
            pass
        else:
            if pose_choice == pose:
                st.text('Example model for ' + pose + ':')
                st.image('./example_poses/' + pose + '.png')

    # Update page subheader and text
    st.subheader('Your Turn')

    st.info("Privacy Info: Uploaded images are never saved or stored. "
            + "They are held temporarily in memory for processing "
            + "and are discarded after the results are displayed. ")
    st.warning("For best results, please upload an image of one (1) person "
               + "doing the Yoga pose in the center of the frame.")

    # Give option to upload or take a picture
    src = ['Upload Image', 'Take a picture']
    src_choice = st.radio('Source', src)

    if src_choice == src[0]:
        picture = st.file_uploader(src[0], type=['jpg', 'png', 'jpeg'])
    else:
        picture = st.camera_input(src[1])

    # If image provided, show process button to run app
    if picture is not None:
        st.success("Image ready for processing.")
        if st.button("Process"):
            # Save the image into a temporary location for processing
            save_img(picture, USER_IMG)
            run_app(picture)

# MENU = ABOUT US
if sidebar_choice == sidebar_menu[2]:
    # TODO: write more
    st.write("We are students at the University of British Columbia Okanagan Campus, "
             + "and this project was created for the course COSC 490: Student-Directed Seminar "
             + "(Topic: Advanced Machine Learning).")
