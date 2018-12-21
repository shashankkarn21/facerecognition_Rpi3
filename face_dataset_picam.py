####################################################
# Modified by Nazmi Asri                           #
# Original code: http://thecodacus.com/            #
# All right reserved to the respective owner       #
####################################################

# Import OpenCV2 for image processing
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os 

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# Start capturing video 
#vid_cam = cv2.VideoCapture(0)

# Detect object in video stream using Haarcascade Frontal Face
##face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cascadePath = "haarcascade_frontalface_default.xml"

# Create classifier from prebuilt model
faceCascade = cv2.CascadeClassifier(cascadePath);
# For each person, one face id
face_id = input("enter id no : ")

# Initialize sample face image
count = 0

assure_path_exists("dataset/")

# Start looping
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    im = frame.array

    # Convert frame to grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Detect frames of different sizes, list of faces rectangles
    faces = faceCascade.detectMultiScale(gray, 1.1,5)

    # Loops for each faces
    for (x,y,w,h) in faces:

        # Crop the image frame into rectangle
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)
        
        # Increment sample face image
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

        # Display the video frame, with bounded rectangle on the person's face
    cv2.imshow('frame', im)
        
    rawCapture.truncate(0)

    # To stop taking video, press 'q' for at least 100ms
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    # If image taken reach 100, stop taking video
    elif count>20:
        break

# Stop video
#vid_cam.release()

# Close all started windows
#cv2.destroyAllWindows()

