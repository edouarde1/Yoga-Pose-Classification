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
    model = tf.keras.models.load_model("../models/" + model_name, compile=False) # removed compile=False
    return model


def run_app(original_img):
    with st.spinner("Processing image..."):
        # Convert user image to rendered image
        render_img()
        # give the system time to save the rendered image
        time.sleep(2)
        # Process rendered img for model
        rendered_img = Image.open(PROC_IMG)
        display_pictures(original_img, rendered_img)
        processed_image = np.array(rendered_img).astype('float32')/255
        processed_image = transform.resize(processed_image, (256, 256, 3))
        processed_image = tf.expand_dims(processed_image, axis=0)
        
    # Load Model
    model = load_model("efficientnet_pretrain1_openpose")  # TODO: Update model name

    # Classify pose
    predictedvalues = model.predict(processed_image)
    predicted = np.argmax(predictedvalues, axis=1)

    # Define labels
    labels = ['Cow-Face1','Extended-Hand-to-Big-Toe-Pose','Half-Lord-of-the-Fishes-Pose',
    'Half-Moon-Pose','Warrior-I-Pose','dancer','extended-triangle','firelog','goddess',
    'lotus','revolved-side-angle','tree-pose','upward-salute','warrior2']
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
        st.write("First, choose a pose that you want to practice.")
        st.write("Second, take a picture or upload an image of yourself doing that pose.")
        st.write("Finally, click `Process` to run our model.")

    # Add pose options
    st.subheader("Choose a Yoga Pose")
    pose = ['Pose 1', 'Pose 2', 'Pose 3', 'Pose 4', 'Pose 5']
    pose_choice = st.selectbox('Select the pose you want to practice', pose)

    # Load images for each pose
    if pose_choice == pose[0]:
        st.text('Try to do ' + pose[0])
        # st.image(pose_file0)
    elif pose_choice == pose[1]:
        st.text('Try to do ' + pose[1])
        # st.image(pose_file1)
    elif pose_choice == pose[2]:
        st.text('Try to do ' + pose[2])
        # st.image(pose_file2)
    elif pose_choice == pose[3]:
        st.text('Try to do ' + pose[3])
        # st.image(pose_file3)
    else:
        st.text('Try to do ' + pose[4])
        # st.image(pose_file4)

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
