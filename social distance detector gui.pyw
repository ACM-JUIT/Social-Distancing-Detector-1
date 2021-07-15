from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np
from resources.violate import breachsocialdistance
from resources.boundingboxes import bboxes
from resources.detect import detect
from resources.config import *
from resources.savelog import addtolog
import time
from playsound import playsound

def videoloop():
    #Read each frame from the webcam
    success, frame = webcam.read()  
    
    if success:
        #Grabs results after sending it into the network
        results = detect(frame,net,outputlayers,height,width)
        
        #acquires the results of violations in distance 
        violates = breachsocialdistance(results,scale.get())
        
        #If violates is more than 2 it plays an alert audio
        if len(violates) > 0: 
            alert(len(violates))
        
        #Draws bounding boxes on each frame
        img = bboxes(results,classes,frame,violates,scale.get())
        
        #Converting Image from BGR to RGBA
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)  
        
        #Creates an image memory from an object
        current_image = Image.fromarray(cv2image)

        #Makes Tkinter-compatible photo image  
        imgtk = ImageTk.PhotoImage(image=current_image)

        #Packs frame onto webcampanel
        webcampanel.imgtk = imgtk
        webcampanel.config(image=imgtk)

        #Loops the frame after one millisecond
        root.after(1, videoloop)

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
webcam = cv2.VideoCapture(0)

#Get original height and width of videostream
width = webcam.get(3)
height = webcam.get(4)

#Setting up colors for the app
colors = ("","#8155ba","#008180","#e43d40","#2ed162")

#Intializing our app
root = Tk()
root.title("Social Distance Detector")
root.configure(bg = "black")
photo = PhotoImage(file = "resources/logo.png")
root.iconphoto(False, photo)

#Frame to hold heading
frame1 = Frame(root, background = colors[2])
headline = Label(frame1, text = "Social Distance Detector", font = ("times new roman", 28, "bold"), bg = "black", fg = "white", relief = RIDGE)

# Adding the Logo Image
image = Image.open("resources/detector.png")
resize_image = image.resize((384, 216))
photo = ImageTk.PhotoImage(resize_image)
photo_label = Label (image=photo)

#Packing the Social Distance Title Frame
frame1.pack(padx = 10 , pady = 10)
headline.pack(padx = 1.5, pady = 3)

# Packing the Logo Label
photo_label.pack(padx = 10 , pady = 10)

#Setting panel for webcam feed
webcampanel = Label(root,bg = colors[1]) 
root.config(cursor = "arrow")

#Setting Scale to manually change the violate distance
scale = IntVar()
violatescale = Scale(root, variable = scale, from_= 25, to = 500, orient = HORIZONTAL, activebackground = colors[3], sliderlength = 15, width = 10, troughcolor = colors[2], length = 500)

#Initially safe distance is set at 75 pixels
scale.set(75)

#Frame for the comment
frame2 = Frame(root, background = colors[2])
comment = Label(frame2, text = "Adjust the safe distance", font = ("Bahnschrift", 15, "bold"), bg = "black", fg = "white", relief = SUNKEN, borderwidth = 2)
comment.pack(padx = 1.5, pady = 5)

#To Pack the program after user clicks start webcam
def starteverything():
    webcampanel.pack(padx = 20, pady = 10)
    violatescale.pack(anchor = CENTER, expand = True,padx = 5)
    frame2.pack(padx = 2 , pady = 10)
    videoloop()
    startwebcambutton.pack_forget()
    photo_label.pack_forget()

#Button to start the program
startwebcambutton = Button(root, text = "Start Webcam", font = ("Bahnschrift", 15, "bold"), activebackground = colors[4], activeforeground = "black", bg = "grey", fg = "black", relief = RAISED,command = lambda : starteverything())
startwebcambutton.pack(padx=10, pady=10)

disable_time = 10

#Alert Audio function that plays an alert audio after every 10 seconds in case of continuous violation
def alert(violations,stamp = [time.time() - disable_time]):
    if time.time() - stamp[0] <= disable_time:
        return
    #Plays alert audio
    playsound('resources/alertaudio.mp3',block=False)

    #Adds Log to file violationlog.csv
    addtolog(violations)
    stamp[0] = time.time()

#Running our app loop
root.mainloop()

webcam.release()
cv2.destroyAllWindows()