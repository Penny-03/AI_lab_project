import mediapipe 
import pyautogui


def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

########pausaa##############
def is_pause(hand_landmarks, image_width, image_height):# function for putting the game in pause
    
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    pinky_tip=hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    return calculate_distance(thumb_tip, pinky_tip)<0.05

#function for verifiying if there is a click
def is_click(prev_index_y, index_y, click_threshold,last_click_time,click_cooldown):
  current_time = time.time()
  if prev_index_y is not None:
      if (prev_index_y - index_y > click_threshold) and (
              current_time - last_click_time > click_cooldown):
          last_click_time = current_time
          cv2.putText(image, "Clic!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#function for moving mouse
def move_mouse():
  if is_mouse():
    screen_width, screen_height = pyautogui.size() 
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    h, w, _ = image.shape
    cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
    
    # Converti le coordinate in base alla risoluzione dello schermo.
    screen_x = int(index_finger_tip.x * screen_width)
    screen_y = int(index_finger_tip.y * screen_height)
    
    # Muovi il mouse.
    pyautogui.moveTo(screen_x, screen_y)
    
    # Disegna un cerchio sulla punta del dito indice.
    cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)



# Ottieni la risoluzione dello schermo.
screen_width, screen_height = pyautogui.size()






    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            

    # Mostra l'immagine con le annotazioni.
    cv2.imshow('Hand Tracking', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


