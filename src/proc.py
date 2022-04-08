import os
import io
import subprocess

def save_img(file, path):
    g = io.BytesIO(file.read())  # BytesIO Object
    with open(path, 'wb') as out:  # Open temporary file as bytes
        out.write(g.read())  # Read bytes into file
        out.close()
        
def render_img():
    current = os.getcwd()
    os.chdir("../../openpose/")
    subprocess.Popen("bin/OpenPoseDemo.exe --image_dir ../Yoga-Pose-Classification/src/images/ --write_images ../Yoga-Pose-Classification/src/images/ --disable_blending --display 0")
    os.chdir(current)
