import cv2
import math
def open_pose_to_image(img):

    # We can choose different types of model here
    # Body-25
    protoFile = "../openpose/models/pose/body_25/pose_deploy.prototxt"
    weightsFile = "../openpose/models/pose/body_25/pose_iter_584000.caffemodel"
    # MPI
    # protoFile = "../openpose/models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    # weightsFile = "../openpose/models/pose/mpi/pose_iter_160000.caffemodel"
    # COCO
    # protoFile = "../openpose/models/pose/coco/pose_deploy_linevec.prototxt"
    # weightsFile = "../openpose/models/pose/coco/pose_iter_440000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    # Read image
    frame = cv2.imdecode(np.asarray(bytearray(img)), cv2.IMREAD_COLOR)
    height, width, channels = frame.shape

    # Resize
    width_out = 368
    frame1 = cv2.resize(frame, (width_out, int(width_out * height / width)), cv2.INTER_AREA)
    height1, width1, channels1 = frame1.shape

    # Create black img for drawing skeleton structure
    black_img = np.zeros((int(width_out * height / width), width_out, 3), dtype = "uint8")

    # Specify the input image dimensions
    inWidth = 368
    inHeight = 368

    # Prepare the frame to be fed to the network
    inpBlob = cv2.dnn.blobFromImage(frame1, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

    # Set the prepared object as the input blob of the network
    net.setInput(inpBlob)

    # Make Predictions and Parse Keypoints
    output = net.forward()
    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []
    for i in range(25):
        # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]
        # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        # Scale the point to fit on the original image
        x = (width1 * point[0]) / W
        y = (height1 * point[1]) / H
        if prob > 0:
            cv2.circle(black_img, (int(x), int(y)), 3, (255, 0, 0), thickness=-1, lineType=cv2.FILLED)
            # cv2.putText(black_img, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
            # Add the point to the list if the probability is greater than the threshold
            points.append((int(x), int(y)))
        else:
            points.append(None)

    # Draw Skeleton
    POSE_PAIRS = [[0, 1, 153, 0, 51], [1, 2, 153, 51, 0], [2, 3, 153, 102, 0], [3, 4, 153, 153, 0], [1, 5, 102, 153, 0],
                  [5, 6, 51, 153, 0], [6, 7, 0, 153, 0], [1, 8, 153, 0, 0], [8, 9, 0, 153, 51], [9, 10, 0, 153, 102],
                  [10, 11, 0, 153, 153], [8, 12, 0, 102, 153], [12, 13, 0, 51, 153], [13, 14, 0, 0, 153],
                  [0, 15, 153, 0, 102], [15, 17, 153, 0, 153], [0, 16, 102, 0, 153], [16, 18, 51, 0, 153],
                  [11, 23, 0, 153, 153], [11, 22, 0, 153, 153], [22, 23, 0, 153, 153], [14, 21, 0, 0, 153],
                  [14, 19, 0, 0, 153], [19, 20, 0, 0, 153]]
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
        r = pair[2]
        g = pair[3]
        b = pair[4]
        if points[partA] and points[partB]:
            # Set threshold so that long line (which result in wrong line), will be removed
            if math.sqrt(pow(points[partA][0] - points[partB][0], 2) + pow(points[partA][1] - points[partB][1], 2)) < (150 * height1 / width1):
                cv2.line(black_img, points[partA], points[partB], (r, g, b), 2)

    return black_img


# This part is for video process
# # capture video
# cap = cv2.VideoCapture("video.mp4")
# fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# out = cv2.VideoWriter('videoName.avi', fourcc, 20, (1920, 1080))
#
# if cap.isOpened():
#     # # get vcap property
#     # width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
#     # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
#     # print(width, height)
#
#     # Check if video file is opened successfully
#     if not cap.isOpened():
#         print("Error opening video stream or file")
#     else:
#         width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
#         height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
#         print(width, height)
#     # Read until video is completed
#     while cap.isOpened():
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if ret == True:
#             width_out = int(width)
#             frame = cv2.resize(frame, (width_out, int(width_out * height / width)), cv2.INTER_AREA)
#             # process the frame here
#             inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (224, 224), (0, 0, 0), swapRB=False, crop=False)
#             net.setInput(inpBlob)
#             output = net.forward()
#
#             H = output.shape[2]
#             W = output.shape[3]
#             # Empty list to store the detected keypoints
#             points = []
#             for i in range(15):
#                 # confidence map of corresponding body's part.
#                 probMap = output[0, i, :, :]
#                 # Find global maxima of the probMap.
#                 minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
#                 # Scale the point to fit on the original image
#                 x = (width * point[0]) / W
#                 y = (height * point[1]) / H
#                 if prob > 1:
#                     cv2.circle(frame, (int(x), int(y)), 15, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
#                     cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 3,
#                                 lineType=cv2.LINE_AA)
#                     # Add the point to the list if the probability is greater than the threshold
#                     points.append((int(x), int(y)))
#                 else:
#                     points.append(None)
#
#             POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9], [9, 10],
#                           [14, 11], [11, 12], [12, 13]]
#
#             for pair in POSE_PAIRS:
#                 partA = pair[0]
#                 partB = pair[1]
#                 if points[partA] and points[partB]:
#                     cv2.line(frame, points[partA], points[partB], (0, 255, 0), 3)
#
#             out.write(frame)
#
#         # Break the loop
#         else:
#             break


import numpy as np
