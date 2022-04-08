import time
import os
import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
import urllib.request
from PIL import Image
from skimage import transform
import proc

# files & directory
DIR_IMG = "../temp/"
USER_IMG = DIR_IMG + "temp.jpg"
PROC_IMG = DIR_IMG + "temp_rendered.png"

poses = ['Cow-Face', 'Extended-Hand-to-Big-Toe-Pose', 'Half-Lord-of-the-Fishes-Pose',
                'Half-Moon-Pose', 'Warrior-I-', 'Dancer', 'Extended-Triangle', 'Fire-Log', 'Goddess',
                'Lotus', 'Revolved-Side-Angle', 'Tree-Pose', 'Upward-Salute', 'Warrior-II']

def get_md_as_string(path):
    url = "https://raw.githubusercontent.com/edouarde1/Yoga-Pose-Classification/main/documentation/" + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = tf.keras.models.load_model("../models/" + model_name, compile=False)  # removed compile=False
    return model

def run_app(original_img):
    try:
        with st.spinner("Processing image..."):
            # Save the image into a temporary location for processing
            print("Creating temp user file")
            proc.save_img(original_img, USER_IMG)
            proc.waitUntilExists(USER_IMG)
            
            # Convert user image to rendered image
            print("Creating rendered image with OpenPose...")
            proc.render_img()
            proc.waitUntilExists(PROC_IMG)
            
            # Display user img vs rendered img
            print("Displaying images...")
            rendered_img = Image.open(PROC_IMG)
            display_pictures(original_img, rendered_img)
            
            # Convert rendered img to tensor for model prediction
            processed_image = np.array(rendered_img).astype('float32') / 255
            processed_image = transform.resize(processed_image, (256, 256, 3))
            processed_image = tf.expand_dims(processed_image, axis=0)

        # Load Model
        model = load_model("efficientnet_pretrain1_openpose")  # TODO: Update model name

        # Classify pose
        predictedvalues = model.predict(processed_image)
        predicted = np.argmax(predictedvalues, axis=1)

        # Info in terminal (not shown in app)
        print("SHAPE: " + str(predictedvalues.shape))
        print("VALS: " + str(predictedvalues))
        print("PRED: " + str(predicted))
        print("LABEL: " + str(poses[predicted[0]]))

        # Display verdict
        display_results(poses[predicted[0]])
        
    except:
        st.write("We're sorry. Something went wrong. Please try again or contact the developers.")

    finally:
        # give time for rendered image to be created in case exception occurred during openpose process
        time.sleep(5)
        # iterate through temp directory and delete all files
        for file in os.listdir(DIR_IMG):
            os.remove(os.path.join(DIR_IMG, file))

# Show original vs. processed images
def display_pictures(original, processed):
    left_col, right_col = st.columns(2)
    left_col.image(original, caption="Original Image")
    right_col.image(processed, caption="Processed Image")

# TODO: determine how we want to display results
def display_results(results):
    st.write("Your pose was classified as: " + str(results))
    if pose_choice == 'Choose a pose':
        st.write("You have not chosen a model pose. Please select one from the dropdown above.")
    elif pose_choice == str(results):
        st.balloons()
        st.write("Congratulations! You have correctly done the pose")
    else:
        st.write("Your pose is not correct. Please try again.")

# Main Page Info
st.title('Yoga Pose Classification App')
st.write(" ------ ")

# SIDEBAR
st.sidebar.title("Yoga Pose Classification App")
st.sidebar.write(" ------ ")

sidebar_menu = ['Practice Yoga', 'About']
sidebar_choice = st.sidebar.selectbox('Menu', sidebar_menu)

st.sidebar.write(" ------ ")
st.sidebar.write("Last updated: 08 April 2022")  # TODO: update

# MENU = PRACTICE YOGA
if sidebar_choice == sidebar_menu[0]:

    # Provide users more instructions
    with st.expander("Instructions"):
        st.write("First, choose a pose that you want to practice for example image of that pose.")
        st.write("Second, take a picture or upload an image of yourself doing that pose.")
        st.write("Finally, click `Process` to run our model.")
        st.write("*Tip: For pose that have facing direction (left or right), you can do in either direction.")

    st.subheader("Choose a Yoga Pose")
    # take pose list and add "choose a pose" option so that a pose isn't already selected
    pose_choice = st.selectbox('Select the pose you want to practice', (["Choose a pose"] + poses))

    for pose in poses:
        if pose_choice == 'Choose a pose':
            pass
        else:
            if pose_choice == pose:
                st.write('Example model for ' + pose + ':')
                st.image('./example_poses/' + pose + '.png')
                st.write("All images are provided by the publicly available dataset...") #TODO: finish reference

    # Update page subheader and text
    st.subheader('Your Turn')

    st.info("Privacy Info: Uploaded images are temporarily saved on the "
            + "local device and are immediately discarded after the results "
            + "are displayed. ")
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
            run_app(picture)

# MENU = ABOUT
# TODO: edit, remove, add info
if sidebar_choice == sidebar_menu[1]:
    st.write(get_md_as_string("project-info.md"))
    st.write("We are students at the University of British Columbia Okanagan Campus, "
             + "and this project was created for the course COSC 490: Student-Directed Seminar "
             + "(Topic: Advanced Machine Learning).")
