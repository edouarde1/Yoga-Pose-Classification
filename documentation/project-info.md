Welcome to Namaste (At Home)!

:person_in_lotus_position: Using a routine with 14 Yoga poses, this app will classify your pose and help you practice Yoga at your own pace with your computer in the location of your choice (please ensure it is a safe place to practice Yoga).

:point_left: To begin, go to the `Practice Yoga` page from the main menu in the sidebar on the left. There, you can practice the pose of your choice with no time limits or restrictions. Once you select a pose, you can either upload an image or take a picture.

:mag: After receiving the image (which is not saved or kept in any way), the app will process the image using OpenPose and then use a modified EfficientNet model to classify the pose.

:muscle: Our model was trained using the public Yoga pose Image classification dataset available on [Kaggle](https://www.kaggle.com/datasets/shrutisaxena/yoga-pose-image-classification-dataset) after it was rendered using [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). The app classifies your pose with a modified [EfficientNet](https://keras.io/api/applications/efficientnet/) model which was pre-trained on [ImageNet](https://www.image-net.org/).

:pushpin: Check out our project's source code on [Github](https://github.com/edouarde1/Yoga-Pose-Classification) and read more about how it works in our [final report](https://github.com/edouarde1/Yoga-Pose-Classification/blob/main/documentation/Project-Report.pdf).

We are students at the University of British Columbia Okanagan Campus, and this project was created for the course COSC 490: Student-Directed Seminar (Topic: Advanced Machine Learning).
