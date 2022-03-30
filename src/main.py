import streamlit as st

# TODO: Move this function to another file to separate model and web page
def classify(img, pose):
    """
    Classifies the user's Yoga pose.

    Args:
        img (_type): user photo
        pose (String): yoga pose name

    Returns:
        Boolean: True if classified correctly
    """
    # TODO: decide if we want pass/fail or Double for probability of classification
    # TODO: Adjust image for model
    # TODO: Load model - should this be done elsewhere?
    # TODO: Classify the image
    return True
    
# Main Page Info
st.title('Yoga Pose Classification App')
st.subheader('This app lets you practice Yoga poses!')
st.text('We used Streamlit for this app.')

# TODO: Provide users more instructions
st.text("First, choose a pose that you want to try.")
st.text("Second, take a picture or upload an image of yourself doing that pose.")
st.text("Finally, click `Process` to run our model.")

# SIDEBAR
st.sidebar.header('Yoga Pose Classification App')

# MENU options in the sidebar
menu = ['Yoga Pose Classification', 'About']
choice = st.sidebar.selectbox('Menu', menu)

# Bottom of sidebar
st.sidebar.info("COSC 490 Project\n11 April 2022")

# SIDEBAR MENU CHOICE
if choice == menu[0]:
    
    # Add poses to the sidebar
    pose = ['Pose 1', 'Pose 2', 'Pose 3', 'Pose 4', 'Pose 5']
    pose_choice = st.radio('Choose a Yoga Pose', pose)
    
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
    st.subheader('Yoga Pose')
    
    # Give option to upload or take a picture
    src = ['Upload Image', 'Take a picture']
    src_choice = st.radio('Source', src)
    
    if src_choice == src[0]:
        image_file = st.file_uploader(src[0], type=['jpg', 'png', 'jpeg'])
    else:
        image_file = st.camera_input(src[1])

    # Display the user's photo
    if image_file:
        st.text("Your photo")
        st.image(image_file)
        
    # Process the image with the model
    if st.button("Process"):
        # Check if we received an image  
        if(image_file): 
            result = classify(image_file, pose_choice)
            if result:
                st.success("Success message")
            else:
                st.text("Fail message")
        # If no image received
        else:
            st.text('Please take a picture or upload a photo.')
            
# SIDEBAR MENU CHOICE
if choice == menu[1]:
    st.subheader('COSC 490 Group Project')
    
    # TODO: Add information about project or direct users to GitHub
    st.text('')
