import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from openpose_functions import open_pose_to_image
from image_process import load_img
from skimage import transform

poses = ['Cow-Face', 'Extended-Hand-to-Big-Toe', 'Half-Lord-of-the-Fishes',
         'Half-Moon', 'Warrior-I', 'Dancer', 'Extended-Triangle', 'Fire-Log', 'Goddess',
         'Lotus', 'Revolved-Side-Angle', 'Tree-Pose', 'Upward-Salute', 'Warrior-II']

def md_to_string(filename):
    result = ""
    with open('../documentation/' + filename, 'r') as infile:
        result += infile.read()
    return result

@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = tf.keras.models.load_model("../models/" + model_name, compile=False)
    return model

def run_app(original_img):
    with st.spinner("Processing image..."):
        rendered_image = open_pose_to_image(original_img.getvalue())
        processed_image = np.array(rendered_image).astype('float32') / 255
        processed_image = transform.resize(processed_image, (256, 256, 3))
        processed_image = tf.expand_dims(processed_image, axis=0)
        display_pictures(original_img, rendered_image)

    # Load Model
    model = load_model("efficientnet_pretrain1_openpose")

    # Classify pose
    predictedvalues = model.predict(processed_image)
    predicted = np.argmax(predictedvalues, axis=1)

    # See terminal for debugging
    print("SHAPE: " + str(predictedvalues.shape))
    print("VALS: " + str(predictedvalues))
    print("PRED: " + str(predicted))
    print("LABEL: " + str(poses[predicted[0]]))
    
    # Display results
    display_results(poses[predicted[0]], predictedvalues[0], predicted)
    
    # Explicitly discard user's image after results are displayed
    rendered_image = None
    processed_image = None

# Show original vs. processed images
def display_pictures(original, processed):
    left_col, right_col = st.columns(2)
    left_col.image(original, caption="Original Image")
    right_col.image(processed, caption="Processed Image")

# Tell user how well they did
def display_results(results, probabilities, predicted):
    THRESHOLD = 0.80
    pred_pose = str(results)
    acc = '{0:.2f}'.format(probabilities[predicted[0]]*100) + "%"
    
    if probabilities[predicted[0]] > THRESHOLD:
        if pose_choice == 'Choose a pose':
            st.warning("You did not select a pose to practice. Please select one from the dropdown above.")
            st.success("Your pose was classified as " + pred_pose + " with an accuracy of " + acc + ".")
        elif pose_choice == pred_pose:
            st.balloons()
            st.success("Congratulations! You have correctly done the selected pose: " + pose_choice + " with an accuracy of " + acc + ".")
        elif pose_choice != pred_pose:
            st.error("Your pose does not match the selected pose: " + pose_choice + ".")
            st.warning("If you were trying " + pred_pose + ", please select the pose from the dropdown above and try again.")
    else:
        st.warning("Your pose was classified as " + pred_pose + " with an accuracy of " + acc + ".")
        st.error("This is not high enough to be confident in your pose, please check your form and try again!")

# Main Page Info
st.title('Namaste (At Home)')
st.write('A Yoga pose classification web app for learning Yoga at home.')
st.write(" ------ ")

# SIDEBAR
st.sidebar.title("Namaste (At Home)")
st.sidebar.write('A Yoga pose classification web app for learning Yoga at home.')
st.sidebar.write(" ------ ")

sidebar_menu = ['Practice Yoga', 'About']
sidebar_choice = st.sidebar.selectbox('Menu', sidebar_menu)

st.sidebar.write(" ------ ")
st.sidebar.write("Last updated: 13 April 2022")  # TODO: update

# MENU = PRACTICE YOGA
if sidebar_choice == sidebar_menu[0]:

    # Provide users more instructions
    with st.expander("Instructions"):
        st.write("First, select a pose to practice. A sample image is provided to help you learn.")
        st.write("Next, take a picture or upload an image of yourself doing that pose.")
        st.write("Finally, click `Process` to run the application and wait for your results.")

    st.subheader("Choose a Yoga Pose")
    # take pose list and add "choose a pose" option so that a pose isn't already selected
    pose_choice = st.selectbox('Select the pose you want to practice', (["Choose a pose"] + poses))

    for pose in poses:
        if pose_choice == 'Choose a pose':
            pass
        else:
            if pose_choice == pose:
                st.write('Sample image of ' + pose + ':')
                st.image('./example_poses/' + pose + '.png')
                st.write("All sample images are provided by the publicly available Yoga Pose Image "
                         + "classification dataset.")
                st.write("Please view the 'About' section from the main menu to learn more.")

    # Update page subheader and text
    st.subheader('Your Turn')
    st.write("Now it's your turn to practice the pose!")
    st.warning("For best results, please ensure the image is of one (1) person "
               + "doing the Yoga pose in the center of the frame facing the camera. "
               + "For poses that face left or right, you can perform the pose in either direction.")
    st.info("Privacy Info: The picture you provide is neither saved nor stored. "
            + "It is temporarily held in memory for the model to predict, and then it discarded after results are displayed.")
    
    # Provide option to upload or take a picture
    src = ['Upload an image', 'Take a picture']
    src_choice = st.radio('Select one:', src)
    
    if src_choice == src[0]:
        picture = st.file_uploader(src[0], type=['jpg', 'png', 'jpeg'])
    else:
        picture = st.camera_input(src[1])

    # If image provided, show process button to run app
    if picture is not None:
        #st.success("Image ready for processing.")
        if st.button("Check my pose"):
            run_app(picture)
            picture = None # explicitly discard image after results are displayed

# MENU = ABOUT
if sidebar_choice == sidebar_menu[1]:
    st.write(md_to_string("project-info.md"))
    with st.expander("Walkthrough"):
        st.write("Looking for an in-depth walkthrough of the application?")
        st.write("We have step-by-step instructions in our [GitHub repository](https://github.com/edouarde1/Yoga-Pose-Classification/blob/main/documentation/walkthrough.md).")
