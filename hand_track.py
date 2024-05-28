import cv2
import mediapipe as mp
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#video capture
video= cv2.VideoCapture(0)
hand=mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5)

#video reading
while True: 
    ret, frame = video.read()
    #frame_flipped = cv2.flip(frame, 1)
    
    results = hand.process(frame)
    k = cv2.waitKey(10) #exit key
    # Draw the hand annotations on the image.
    frame.flags.writeable = True
    
    if results.multi_hand_landmarks:# if you recon. an hand
      #just to show points 
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
       # end  
      hand_coor= enumerate(hand_landmarks.landmark) 
      for idx, landmark in hand_coor: #idx = # of the point in the hand
            pass
            #normalized to [0.0, 1.0] by the image width and height, respectively
            #To normalize values, we divide coordinates in pixels 
            #for the x- and y-axis by the width and the height of the image.
            # landmark contains x, y, z coordinates of each landmark
            # Access landmark data like this: landmark.x, landmark.y, landmark.z
    cv2.imshow("Video", cv2.flip(frame,1))

    if k == ord("q"): #exit button
            break
