# importing libraries
import cv2
import numpy as np
from config import *


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

  #Resizes the current frame to 800 pixels width
  frame = cv2.resize(frame,(modwidth,modheight),interpolation=cv2.INTER_AREA)
  results = []

  #Converting current frame to blob to pass thorugh network
  blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (320, 320),swapRB=True, crop=False)
	
  #Pass the blob through the network
  net.setInput(blob)
	#grabbing output layers with predictions
  layerOutputs = net.forward(outputlayers)

	#Intializing Lists for bounding boxes , labels , centriods and confidences of each prediction
  boxes = []
  classids = []
  centroids = []
  confidences = []

	#Looping over each output layer
  for output in layerOutputs:
    
    for detection in output:

			#Extracting prediction values
      scores = detection[5:]
			#Extracting the classid of the highest score
      classID = np.argmax(scores)
			#Storing the confidence of highest scoring index
      confidence = scores[classID]

			#filtering off weak predictions
      if confidence > confidencethreshold:

        #Storing the Border box for the detection
        box = detection[0:4] * np.array([modwidth, modheight, modwidth, modheight])
        (centerX, centerY, width, height) = box.astype("int")

        #Calculating the values for the centriod of the borderbox
        x = int(centerX - (width / 2))
        y = int(centerY - (height / 2))

        #Adding the values of the borderboxes,centroids, confidences and classids   
        boxes.append([x, y, int(width), int(height)])
        centroids.append((centerX, centerY))
        confidences.append(float(confidence))
        classids.append(classID)
  #Applying Non maximum suppression to select one borderbox per perdiction
  finalindexs = cv2.dnn.NMSBoxes(boxes, confidences,confidencethreshold,nmsthreshold)
  
  if len(finalindexs) > 0:
    for i in finalindexs.flatten():
      
      #Grabbing the coordinates of the primary box
      (x, y) = (boxes[i][0], boxes[i][1])
      (w, h) = (boxes[i][2], boxes[i][3])

      #Adding the resulant boxes to final results
      r = (classids[i],confidences[i], (x, y, x + w, y + h), centroids[i])
      results.append(r)  

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