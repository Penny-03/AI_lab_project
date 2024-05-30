import mediapipe 
import pyautogui

# function for putting the game in pause
def is_pause(hand_landmarks, image_width, image_height):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calcola le coordinate del centro tra medio e indice
    center_x = (index_tip.x + middle_tip.x) / 2 * image_width
    center_y = (index_tip.y + middle_tip.y) / 2 * image_height

    # Verifica se il pollice tocca il centro calcolato
    return (abs(thumb_tip.x * image_width - center_x) < 0.05 * image_width and abs(
        thumb_tip.y * image_height - center_y) < 0.05 * image_height) and len(results.multi_hand_landmarks) == 2

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


