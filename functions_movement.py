import mediapipe 
import pyautogui
import time

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

# function for putting the game in pause
def is_pause(fingertips):
    return calculate_distance(fingertips[0], fingertips[4])<0.05

#function for verifiying if there is a click
def is_click(fingertips, click_threshold, last_click_time, click_cooldown):
    current_time = time.time()
    if calculate_distance(fingertips[0], fingertips[1])<0.05 and (current_time - last_click_time>click_cooldown): #se le due dita si toccano ed è passato almeno un secondo allora fai click
        last_click_time = current_time #aggiorna il last_click_time
        return True
    return False

#function for verifying if we are entering mouse mode 
def is_mouse(finger_tips):
    return calculate_distance(fingertips[0], fingertips[2])<0.05
    
#function for moving mouse
def move_mouse(finger_tips):
  if is_mouse(finger_tips):
    screen_width, screen_height = pyautogui.size() 
    index_tip = finger_tips[1]
    h, w, _ = image.shape
    cx, cy = int(index_tip.x * w), int(index_tip.y * h)
    
    # Converti le coordinate in base alla risoluzione dello schermo.
    screen_x = int(index_tip.x * screen_width)
    screen_y = int(index_tip.y * screen_height)
    
    # Muovi il mouse.
    pyautogui.moveTo(screen_x, screen_y)
    
    # Disegna un cerchio sulla punta del dito indice.
    cv2.circle(image, (cx, cy), 10, (0, 255, 0), cv2.FILLED)








