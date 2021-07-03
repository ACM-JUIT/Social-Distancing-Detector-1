# importing libraries and required files
import cv2
import numpy as np
from config import *
from boundingboxes import *
from detect import *

#Loading YOLOv4-tiny configuration file and weights 
#Initializing network
net = cv2.dnn.readNetFromDarknet(Modelconfig,Modelweights)

#Storing Label Names of each object in coco dataset
classes = []
with open(Modelclasses,"r") as file:
    classes=[eachline.strip() for eachline in file.readlines()]

#Setting backend as OpenCV
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)

#Setting target processor as CPU
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#Grabbing Layer Names from the Network
layernames = net.getLayerNames()

#Grabbing Output Layer Names from the Network
outputlayers = [layernames[index[0]-1] for index in net.getUnconnectedOutLayers()]

# Create a VideoCapture object and read from webcam
videostream = cv2.VideoCapture(0)

#Get original height and width of videostream to be modified
originalheight = videostream.get(4)
originalwidth = videostream.get(3)

#Calculate modified height in ratio with 800 pixels
ratio = modwidth / float(originalwidth)
modheight = int(originalheight * ratio)

# Read until video is completed
while True:
  
  # Capture frame-by-frame
  cap,frame = videostream.read()

  #Grabs results after sending it into the network
  results = detect(net,frame,modwidth,modheight,outputlayers)
  
  #Draws bounding boxes on each frame 
  frame = bboxes(results,classes,frame)
 
  # Display the resulting frame
  cv2.imshow('Frame', frame)
   
  # Press q on keyboard to  exit
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release 
# the video capture object
videostream.release()
   
# Closes all the frames
cv2.destroyAllWindows()