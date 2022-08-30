import cv2
import mediapipe as mp
import time
import numpy as np
import easyocr

reader = easyocr.Reader(['ko']) 

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

arr = []
# For webcam input:
cap = cv2.VideoCapture(0)
startTime = time.time()
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    
    

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # mp_drawing.draw_landmarks(
    #     image,
    #     results.pose_landmarks,
    #     mp_pose.POSE_CONNECTIONS,
    #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    timeNow = time.time()
    # print(results.pose_landmarks.landmark[0].z)
    if results.pose_landmarks:
      if len(arr) < 20:
        arr.append(results.pose_landmarks.landmark[0].z)
      else:
        arr = arr[1:20]
        arr.append(results.pose_landmarks.landmark[0].z)
      if timeNow-startTime >0.5:
        startTime = timeNow
        #print("distance : " , round(np.mean(arr), 3))
        result_ocr = reader.readtext(image)
        print(result_ocr)
      
    cv2.imshow('Sixth Sense - Team Boyjo No.1', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()