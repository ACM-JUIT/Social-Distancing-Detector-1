from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np

def videoloop():
    #Read each frame from the webcam
    success, img = webcam.read()  
    
    if success:
               
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

webcam = cv2.VideoCapture(0)
width = webcam.get(3)
height = webcam.get(4)

#Setting up colors for the app
colors = ("","#8155ba","#008180","#e43d40","#2ed162")

#Intializing our app
root = Tk()
root.title("Social Distance Detector")
root.configure(bg = "black")

#Frame to hold heading
frame1 = Frame(root, background = colors[2])
headline = Label(frame1, text = "Social Distance Detector", font = ("times new roman", 28, "bold"), bg = "black", fg = "white", relief = RIDGE)

#Packing the Social Distance Title Frame
frame1.pack(padx = 10 , pady = 10)
headline.pack(padx = 1.5, pady = 3)

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

#Button to start the program
startwebcambutton = Button(root, text = "Start Webcam", font = ("Bahnschrift", 15, "bold"), activebackground = colors[4], activeforeground = "black", bg = "grey", fg = "black", relief = RAISED,command = lambda : starteverything())
startwebcambutton.pack(padx=10, pady=10)

#Running our app loop
root.mainloop()

webcam.release()
cv2.destroyAllWindows()