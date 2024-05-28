import cv2
import mediapipe as mp
import time
import keyboard
import threading
import subprocess
from window_init import *

# Inizializza Mediapipe Hands e le utilità di disegno
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Variabili per tracciare il movimento della mano e del dito
prev_finger_x = None
prev_finger_y = None
prev_index_y = None
movement_threshold = 30  # Soglia per determinare un movimento significativo
movement_cooldown=0.3
click_threshold = 20  # Soglia per determinare un clic
click_cooldown = 1.0  # Tempo di attesa tra un clic e l'altro (in secondi)
last_click_time = 0
last_mov_time=0
pause = False #utilizzata per mettere il gioco in pausa

# Funzione per inviare comandi direzionali al gioco 2048
def send_direction_command(direction):
    if direction == "Right":
        keyboard.press_and_release('d')
    elif direction == "Left":
        keyboard.press_and_release('a')
    elif direction == "Up":
        keyboard.press_and_release('w')
    elif direction == "Down":
        keyboard.press_and_release('s')

# Imposta la webcam
cap = cv2.VideoCapture(0)
# Funzione per avviare il gioco 2048
def start_game():
    subprocess.run(["python", "game_2048/main.py"])


# Avvia il gioco 2048 in un thread separato
game_thread = threading.Thread(target=start_game)
game_thread.start()



###########

########pausaa##############
def is_pause(hand_landmarks, image_width, image_height):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    
    # Calcola le coordinate del centro tra medio e indice
    center_x = (index_tip.x + middle_tip.x) / 2 * image_width
    center_y = (index_tip.y + middle_tip.y) / 2 * image_height
    
    # Verifica se il pollice tocca il centro calcolato
    return (abs(thumb_tip.x * image_width - center_x) < 0.05 * image_width and abs(thumb_tip.y * image_height - center_y) < 0.05 * image_height) and len(results.multi_hand_landmarks)==2  

# Usa Hands di Mediapipe
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        # Converti l'immagine da BGR a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Inverti l'immagine lateralmente per un effetto specchio
        image = cv2.flip(image, 1)
        # Imposta le variabili per il disegno
        results = hands.process(image)
        
        # Converti l'immagine da RGB a BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Controlla se ci sono mani rilevate
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Disegna i punti di riferimento della mano
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # Controlla se il gesto di pausa è rilevato
                if is_pause(hand_landmarks, frame.shape[1], frame.shape[0]):
                    pause = not pause
                    time.sleep(1) 

                if not pause:
                    # Ottieni le coordinate delle punte delle dita
                    finger_tips = [
                        #hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                        #hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    ]
                    index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0]

                    avg_x = sum([tip.x for tip in finger_tips]) / 3 * frame.shape[1]##ricorda di dividere per il numero esatto di dita
                    avg_y = sum([tip.y for tip in finger_tips]) / 3 * frame.shape[0]##
                    
                    current_time = time.time()
                    # Determina la direzione del movimento
                    if prev_finger_x is not None and prev_finger_y is not None:
                        if avg_x - prev_finger_x > movement_threshold and (current_time - last_mov_time > click_cooldown):
                            direction_x = "Right"
                            last_mov_time = current_time
                        elif prev_finger_x - avg_x > movement_threshold and (current_time - last_mov_time > click_cooldown):
                            direction_x = "Left"
                            last_mov_time = current_time
                        else:
                            direction_x = "Still"

                        if avg_y - prev_finger_y > movement_threshold and (current_time - last_mov_time > click_cooldown):
                            direction_y = "Down"
                            last_mov_time = current_time
                        elif prev_finger_y - avg_y > movement_threshold and (current_time - last_mov_time > click_cooldown):
                            direction_y = "Up"
                            last_mov_time = current_time
                        else:
                            direction_y = "Still"

                        # Mostra la direzione del movimento
                        direction = f"Horizontal: {direction_x}, Vertical: {direction_y}"
                        cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (144, 66, 245), 2)

                    
                        # Invia comando al gioco se c'è movimento significativo
                        if direction_x != "Still":
                            send_direction_command(direction_x)
                        if direction_y != "Still":
                            send_direction_command(direction_y)
                    
                    
                    # Determina se c'è stato un clic
                    current_time = time.time()
                    if prev_index_y is not None:
                        if (prev_index_y - index_y > click_threshold) and (current_time - last_click_time > click_cooldown):
                            last_click_time = current_time
                            cv2.putText(image, "Clic!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                    # Aggiorna le posizioni precedenti
                    prev_finger_x = avg_x
                    prev_finger_y = avg_y
                    prev_index_y = index_y
        
        # Mostra l'immagine con i punti di riferimento delle mani e la direzione del movimento
        cv2.imshow('Hand Tracking', image)
        
        if cv2.waitKey(5) & 0xFF == 27:
            break


# Rilascia la webcam e chiudi le finestre
cap.release()
cv2.destroyAllWindows()
