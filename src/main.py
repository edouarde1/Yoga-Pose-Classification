import streamlit as st
import numpy as np
import tensorflow as tf
import keras
import urllib.request
from PIL import Image

def get_md_as_string(path):
    url = "https://raw.githubusercontent.com/edouarde1/Yoga-Pose-Classification/main/documentation/" + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = keras.models.load_model("../models/" + model_name, compile=False)
    return model

def classify_pose(img):
    # Process Image
    test_img = Image.open(img)
    test_img = tf.image.resize(test_img, size=[224,224], preserve_aspect_ratio=True)
    test_img = keras.preprocessing.image.img_to_array(test_img)
    test_img = test_img / 255.0
    test_img = np.expand_dims(test_img, axis=0)
    
    # Load Model and Predict
    model = load_model("cat_dog_model.h5") # TODO: Update model name
    results = model.predict(test_img)
    
    return results

# TODO: Update after determining model and result format
def display_results(results):
    # If showing original image and processed image, use columns
    #left_col, right_col = st.columns(2)
    #left_col.image(img, caption="Original Image")
    #right_col.image(proc_img, caption="Processed Image")
    #right_col.write("Probability of correct pose: " + result_prob)
    
    # If only showing original with written results:
    st.image(picture)
    st.write("Probability of being a dog: " + str(results[0][0]))

# Main Page Info
st.title('Yoga Pose Classification App')
st.write(" ------ ")

# SIDEBAR
st.sidebar.title("Yoga Pose Classification App")
st.sidebar.write(" ------ ")

sidebar_menu = ['Project Info', 'Practice Yoga', 'About Us']
sidebar_choice = st.sidebar.selectbox('Menu', sidebar_menu)

st.sidebar.write(" ------ ")
st.sidebar.write("Last updated: 30 March 2022") #TODO: update

# MENU = PROJECT INFO
if sidebar_choice == sidebar_menu[0]:
    #st.markdown("Our project's purpose...  \n"
    #        +"Our goal...  \n"
    #        +"\n"
    #        +":point_left: How to use the web app...")
    #st.markdown("View our [code on Github](https://github.com/edouarde1/Yoga-Pose-Classification)")
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
    pose_choice = st.radio('Select the pose you want to practice', pose)
    
    # Load images for each pose
    if pose_choice == pose[0]:
        st.text('Try to do '+ pose[0])
        #st.image(pose_file0)
    elif pose_choice == pose[1]:
        st.text('Try to do '+ pose[1])
        #st.image(pose_file1)
    elif pose_choice == pose[2]:
        st.text('Try to do '+ pose[2])
        #st.image(pose_file2)
    elif pose_choice == pose[3]:
        st.text('Try to do '+ pose[3])
        #st.image(pose_file3)
    else:
        st.text('Try to do '+ pose[4])
        #st.image(pose_file4)
    
    # Update page subheader and text
    st.subheader('Your Turn')
    
    st.info("Privacy Info: Uploaded images are never saved or stored. "
        +"They are held temporarily in memory for processing "
        +"and are discarded after the results are displayed. ")
    st.warning("For best results, please upload an image of one (1) person "
               +"doing the Yoga pose in the center of the frame.")

    # Give option to upload or take a picture
    src = ['Upload Image', 'Take a picture']
    src_choice = st.radio('Source', src)
    
    if src_choice == src[0]:
        picture = st.file_uploader(src[0], type=['jpg', 'png', 'jpeg'])
    else:
        picture = st.camera_input(src[1])

    # Display the user's photo
    # TODO: decide if we want to (also) show the processed image with the stick figure on top
    if picture is not None:
        st.success("Image ready for processing.")
        # Process the image with the model
        if st.button("Process"):
            res = classify_pose(picture)
            display_results(res)

# MENU = ABOUT US
if sidebar_choice == sidebar_menu[2]:
    # TODO: write more
    st.write("We are students at the University of British Columbia Okanagan Campus, "
                 +"and this project was created for the course COSC 490: Student-Directed Seminar "
                 +"(Topic: Advanced Machine Learning).")
