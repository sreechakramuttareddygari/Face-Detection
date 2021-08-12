import cv2
import face_recognition
import numpy as np
import os
#os.system("pip3 install pafy")
#os.system("sudo pip install --upgrade youtube_dl")
import pafy
import youtube_dl
url = "https://youtu.be/Egcx63-FfTE?t=29"
vPafy = pafy.new(url)
print(vPafy.title)
play = vPafy.getbest()
# Load the cascade
face_cascade = cv2.CascadeClassifier('/Users/muttareddygarisreechakra/Desktop/haarcascade_frontalface_default.xml')

# To capture video from webcam.
#cap = cv2.VideoCapture("/Users/muttareddygarisreechakra/Desktop/Gambler.mp4")
cap = cv2.VideoCapture(play.url)
# To use a video file as input
# cap = cv2.VideoCapture('filename.mp4')
obama_image = face_recognition.load_image_file("/Users/muttareddygarisreechakra/Desktop/RobertDrowney.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("/Users/muttareddygarisreechakra/Desktop/Offenders/Offender2.JPG")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "Robert Droney",
    "Joe Biden"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
while True:
    # Read the frame
    _, img = cap.read()
    img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = img[:, :, ::-1]
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 2, 3)
    print(faces)
    # Draw the rectangle around each face
    face_locations = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_locations.append([y,x+w,y+h,x])
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations )
    #print(face_encodings)
    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    print(face_names)

    # Display
    cv2.imshow('img', img)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break

# Release the VideoCapture object
cap.release()
