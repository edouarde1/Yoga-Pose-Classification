import os
import io
import subprocess
import time

def save_img(file, path):
    g = io.BytesIO(file.read())  # BytesIO Object
    with open(path, 'wb') as out:  # Open temporary file as bytes
        out.write(g.read())  # Read bytes into file
        # the 'with' auto-closes the file
        
def render_img():
    current = os.getcwd()
    os.chdir("../../openpose/")
    subprocess.Popen("bin/OpenPoseDemo.exe --image_dir ../Yoga-Pose-Classification/temp/ --write_images ../Yoga-Pose-Classification/temp/ --disable_blending --display 0")
    os.chdir(current)

def waitUntilExists(file):
    timeout = 0
    while not os.path.exists(file) and timeout!=20:
            time.sleep(1)
            timeout+=1
        