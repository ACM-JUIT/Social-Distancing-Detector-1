import cv2
import numpy as np

def bboxes(results,classes,frame,violations,violatedistance=75):
    #makes a copy of the frame 
    img = frame 

    count = 0

    #Function to draw frame on people using the coordinates appended
    #loop over the results
    for (index,(classid,prob,bbox,centeriod)) in enumerate(results):

        #filters the function for people detection 
        if classid == 0:

            count = count + 1

            #extract the bounding box and centroid coordinates 
            (startx,starty,endx,endy) = bbox

            #setup the color of the bounding box
            color = (0,255,0)
            
            #setup the color for the bounding box given violations 
            if index in violations:
                color = (0,0,255)
                
            #grabbing the centroid 
            (cx,cy) = centeriod

            #grabbing the class name of the prediction 
            label = str(classes[classid])

            #draw a bounding box around the detected objects
            cv2.rectangle(img,(startx,starty),(endx,endy),color,2)

            #draw circle around centroid coordinates of the person
            cv2.circle(img,(cx,cy),5,color,1)

            #put text for number of people violating the safe distance
            # cv2.putText(img,"violates = "+str(len(violations)),(10,frame.shape[0]-15),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    Safe_Distance = "Safe distance: > {} px".format(violatedistance)
    cv2.putText(frame, Safe_Distance, (10, frame.shape[0] - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0, 255,255), 2)
    human_count = "Human count: {}".format(count)
    text = "Total no of violations: {}".format(len(violations))
    cv2.putText(frame, text, (10, frame.shape[0] - 50),cv2.FONT_HERSHEY_SIMPLEX, 0.80, (0, 0, 255), 2)
    cv2.putText(frame, human_count, (10, frame.shape[0] - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (255, 51, 51), 2)


    return img