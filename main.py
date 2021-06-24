# importing libraries
import cv2
   
# Create a VideoCapture object and read from webcam
videostream = cv2.VideoCapture(0)

# Read until video is completed
while True:
  # Capture frame-by-frame
  cap,frame = videostream.read()

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