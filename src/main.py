import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
import urllib.request
from openpose_functions import open_pose_to_image
from image_process import load_img
from skimage import transform


def get_md_as_string(path):
    url = "https://raw.githubusercontent.com/edouarde1/Yoga-Pose-Classification/main/documentation/" + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")


poses = ['Cow-Face', 'Extended-Hand-to-Big-Toe-Pose', 'Half-Lord-of-the-Fishes-Pose',
         'Half-Moon-Pose', 'Warrior-I-', 'Dancer', 'Extended-Triangle', 'Fire-Log', 'Goddess',
         'Lotus', 'Revolved-Side-Angle', 'Tree-Pose', 'Upward-Salute', 'Warrior-II']


@st.cache(allow_output_mutation=True)
def load_model(model_name):
    model = tf.keras.models.load_model("../models/" + model_name, compile=False)  # removed compile=False
    return model


def run_app(original_img):
    with st.spinner("Processing image..."):
        rendered_image = open_pose_to_image(original_img.getvalue())
        processed_image = np.array(rendered_image).astype('float32') / 255
        processed_image = transform.resize(processed_image, (256, 256, 3))
        processed_image = tf.expand_dims(processed_image, axis=0)
        display_pictures(original_img, rendered_image)

    # Load Model
    model = load_model("efficientnet_pretrain1_openpose")  # TODO: Update model name

    # Prepare processed image for prediction (DOES NOT WORK!)
    # image = tf.convert_to_tensor(processed_img)
    # image = tf.image.resize(image, [256, 256]) # TODO: adjust size if needed
    # image = tf.expand_dims(image, axis=0)  # the shape would be (1, 180, 180, 3)

    # Prepare processed image for prediction
    # image = load_img(processed_image)

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
    return poses[predicted[0]]


# Show original vs. processed images
def display_pictures(original, processed):
    left_col, right_col = st.columns(2)
    left_col.image(original, caption="Original Image")
    right_col.image(processed, caption="Processed Image")


def display_results(results, probabilities, predicted):
    threshold = 0.80
    if probabilities[predicted[0]] > threshold:
        if pose_choice == 'Choose a pose':
            st.write("You have not chosen a model pose. Please select one from the dropdown above.")
            st.write("Your pose was classified as: " + str(results))
        elif pose_choice == str(results):
            st.balloons()
            st.write("Congratulations! You have correctly done the pose")
        else:
            st.write("Your pose does not match the selected pose: " + pose_choice + ".")
            st.write("Were you trying " + str(results) + "?")
    else:
        st.write("Your pose was classified as " + str(results) + " with an accuracy of "
                 + '{0:.2f}'.format(probabilities[predicted[0]]*100) + "%.")
        st.write("This is not high enough to be confident in your pose, please check your form and try again!")


# Main Page Info
st.title('Yoga Pose Classification App')
st.write(" ------ ")

# SIDEBAR
st.sidebar.title("Yoga Pose Classification App")
st.sidebar.write(" ------ ")

sidebar_menu = ['Practice Yoga', 'About']
sidebar_choice = st.sidebar.selectbox('Menu', sidebar_menu)

st.sidebar.write(" ------ ")
st.sidebar.write("Last updated: 10 April 2022")  # TODO: update

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
                st.write("All images are provided by the publicly available dataset Yoga-82")  # TODO: finish reference

    # Update page subheader and text
    st.subheader('Your Turn')

    st.info("Privacy Info: Uploaded images are not saved")
    st.warning("For best results, please upload an image of one (1) person "
               + "doing the Yoga pose in the center of the frame facing the camera.")

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
