import mediapipe 
import pyautogui
import cv2
import time
import math

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

# FUNZIONE PER LA PAUSA DEL GIOCO
# il gioco è in pausa se pollice e mignolo si toccano
def is_pause(finger_tips):
    return calculate_distance(finger_tips[0], finger_tips[4])<0.05

#FUNZIONE PER IL CLICK
#Il click viene preso solo quando sei in pausa e pollice e anulare si toccano
# e se non c'è stato un click nell'ultimo secondo
def is_click(image,finger_tips, click_threshold, last_click_time, click_cooldown):
    current_time = time.time()
    if calculate_distance(finger_tips[0], finger_tips[3])<0.05 and (current_time - last_click_time>click_cooldown): #se le due dita si toccano ed è passato almeno un secondo allora fai click
        last_click_time = current_time #aggiorna il last_click_time
        cv2.putText(image, "Click!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (207, 242, 102), 2)
        return True
    return False

def is_mouse(finger_tips):
    return calculate_distance(finger_tips[0], finger_tips[2])<0.05


#FUNZIONE PER MUOVERE IL CURSORE
#function for verifying if we are entering mouse mode 
def move_mouse(image, finger_tips, click_threshold, last_click_time, click_cooldown):
    
    screen_width, screen_height = pyautogui.size() 
    index_tip = finger_tips[1]
    h, w, _ = image.shape
    cx, cy = int(index_tip.x * w), int(index_tip.y * h)

    # Converti le coordinate in base alla risoluzione dello schermo.
    screen_x = int(index_tip.x * screen_width)
    screen_y = int(index_tip.y * screen_height)

    # Muovi il mouse.
    pyautogui.moveTo(screen_x, screen_y)
    if is_click(image, finger_tips, click_threshold, last_click_time, click_cooldown):
        pyautogui.click()

    # Disegna un cerchio sulla punta del dito indice.
    cv2.circle(image, (cx, cy), 10, (166, 255, 0), -1)
    cv2.putText(image, "MOUSE", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)
    






