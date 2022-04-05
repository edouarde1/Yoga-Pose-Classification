import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
import urllib.request
from openpose_functions import open_pose_to_image

labels = ['Cow-Face-Pose', 'Crescent-Moon-Pose', 'Eagle-Pose', 'Extended-Hand-to-Big-Toe-Pose', 'Half-Lord-of-the-Fishes-Pose', 'Half-Moon-Pose', 'Warrior-I-Pose', 'chair', 'cow-face', 'dancer', 'extended-side-angle', 'extended-triangle', 'firelog', 'goddess', 'hero', 'lotus', 'revolved-side-angle', 'tree-pose', 'upward-salute', 'warrior2']

def get_md_as_string(path):
    url = "https://raw.githubusercontent.com/edouarde1/Yoga-Pose-Classification/main/documentation/" + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = tf.keras.models.load_model("../models/" + model_name, compile=False) # removed compile=False
    return model

def run_app(original_img):
    # Process image using OpenPose
    with st.spinner("Processing image..."):
        processed_img = open_pose_to_image(original_img.getvalue())
        display_pictures(original_img, processed_img)
    
    # Load Model
    model = load_model("efficientnet_openpose")  # TODO: Update model name
    
    # Prepare processed image for prediction
    image = tf.convert_to_tensor(processed_img)
    image = tf.image.resize(image, [256, 256], preserve_aspect_ratio=True) # TODO: adjust size if needed
    image = tf.expand_dims(image, axis=0)  # the shape would be (1, 180, 180, 3)
    
    # Classify pose
    predictedvalues = model.predict(image)
    predicted = np.argmax(predictedvalues, axis=1)
    
    # See terminal for debugging
    print("SHAPE: " + str(predictedvalues.shape))
    print("VALS: " + str(predictedvalues))
    print("PRED: " + str(predicted))
    print("LABEL: " + str(labels[predicted[0]]))

    display_results(labels[predicted[0]])

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
            res = run_app(picture)

# MENU = ABOUT US
if sidebar_choice == sidebar_menu[2]:
    # TODO: write more
    st.write("We are students at the University of British Columbia Okanagan Campus, "
             + "and this project was created for the course COSC 490: Student-Directed Seminar "
             + "(Topic: Advanced Machine Learning).")
