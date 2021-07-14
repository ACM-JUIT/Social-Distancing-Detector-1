# importing libraries and required files
import cv2
import numpy as np
import argparse
from resources.config import *
from resources.boundingboxes import *
from resources.detect import *
from resources.violate import *

#Add argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="",
	help="path to (optional) output video file")
args = vars(ap.parse_args())

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

# Create a VideoCapture object and read from webcam or an input video file
videostream = cv2.VideoCapture("resources/videos/input/"+args["input"] if args["input"] else 0)

#Get original height and width of videostream to be modified
originalheight = videostream.get(4)
originalwidth = videostream.get(3)
modw = originalwidth
modh = originalheight

resize = False
if (originalwidth > 1100):
  modw = 1100
  modh = (int)(originalheight * modw / originalwidth)
  resize = True

#Frame writer to save video is set to none
writer = None

# Read until video is completed
while True:

  # Capture frame-by-frame
  cap,frame = videostream.read()

  if  resize:
    frame = cv2.resize(frame,(modw,modh),interpolation=cv2.INTER_AREA)

  #Grabs results after sending it into the network
  results = detect(frame,net,outputlayers,modh,modw)
  
  #acquires the results of violations in distance 
  violations=breachsocialdistance(results,violatedistance=75)

  #Draws bounding boxes on each frame 
  frame = bboxes(results,classes,frame,violations)
 
  # Display the resulting frame
  cv2.imshow('Frame', frame)
   
  # Press q on keyboard to  exit
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
  if args["output"] != "" and writer is None:
		# initialize our video writer
	  fourcc = cv2.VideoWriter_fourcc(*"MJPG")
	  writer = cv2.VideoWriter("resources/videos/output/"+args["output"], fourcc, 25,
			(frame.shape[1], frame.shape[0]), True)
	# if the video writer is not None, write the frame to the output
	# video file
  if writer is not None:
	  writer.write(frame)

# When everything done, release 
# the video capture object
videostream.release()
   
# Closes all the frames
cv2.destroyAllWindows()