import numpy as np
import cv2
from resources.config import *

def detect(frame, net, outputlayers,height,width):
	(H, W) = height,width
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
				box = detection[0:4] * np.array([W, H, W, H])
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

        #Returning the filtered results with coordinates,classids and confidences
	return results               