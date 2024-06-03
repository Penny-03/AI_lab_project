import mediapipe as mp
import keyboard
import threading
import subprocess
from functions_movement import *
#from game_2048.window_init import *
import pygetwindow as gw

# Inizializza Mediapipe Hands e le utilità di disegno
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Variabili per tracciare il movimento della mano e del dito
prev_finger_x = None
prev_finger_y = None
prev_index_y = None
movement_threshold = 10  # Soglia per determinare un movimento significativo
movement_cooldown = 0.3
click_threshold = 20  # Soglia per determinare un click
click_cooldown = 1.0  # Tempo di attesa tra un click e l'altro
last_click_time = 0
last_mov_time = 0
pause = True  # utilizzata per mettere il gioco in pausa
mouse = False #utlizzata per mettere il gioco in modalità mouse
clicking = False #utilizzata per vedere se si sta cliccando

# Funzione per inviare comandi al gioco 2048
def send_direction_command(direction):
    if direction == "Right":
        keyboard.press_and_release('d')
    elif direction == "Left":
        keyboard.press_and_release('a')
    elif direction == "Up":
        keyboard.press_and_release('w')
    elif direction == "Down":
        keyboard.press_and_release('s')
    elif direction == "Yes":
        keyboard.press_and_release('y')
    elif direction == "No":
        keyboard.press_and_release('n')

# Imposta la webcam
cap = cv2.VideoCapture(0)

# Funzione per avviare il gioco 2048
def start_game():
    subprocess.run(["python", "game_2048/main.py"])


# Avvia il gioco 2048 in un thread separato
game_thread = threading.Thread(target=start_game)
game_thread.start()

#sleeps so the game has time to start and then moves the window to a certain spot on the screen
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
time.sleep(3)
game_window = gw.getWindowsWithTitle('2048')[0]
game_window.resizeTo(500, 800)
game_window.moveTo(1152, 100)

# Usa Hands di Mediapipe
with mp_hands.Hands(
        static_image_mode=False,  # per far si che funzioni in live stream
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        # Inverti l'immagine lateralmente per un effetto specchio
        image = cv2.flip(img, 1)
        # Imposta le variabili per il disegno
        results = hands.process(image)
        # Controlla se ci sono mani rilevate
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Disegna i punti di riferimento della mano
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Ottieni le coordinate delle punte delle dita
                finger_tips = [
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],  # 0
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],  # 1
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],  # 2
                    hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],  # 3
                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]  # 4
                ]

                # Controlla se il gesto di pausa è rilevato e cambia la variabile
                if is_pause(finger_tips):
                    pause = not pause

                if not pause:  # se non stai in pausa

                    avg_x = finger_tips[1].x * image.shape[1]
                    avg_y = finger_tips[1].y * image.shape[0]

                    current_time = time.time()
                    if prev_finger_x is not None and prev_finger_y is not None:
                        if avg_x - prev_finger_x > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_x = "Right"
                            last_mov_time = current_time
                        elif prev_finger_x - avg_x > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_x = "Left"
                            last_mov_time = current_time
                        else:
                            direction_x = "Still"

                        if avg_y - prev_finger_y > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_y = "Down"
                            last_mov_time = current_time
                        elif prev_finger_y - avg_y > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_y = "Up"
                            last_mov_time = current_time
                        else:
                            direction_y = "Still"

                        # calling function to determine the ending movement meaning
                        gesture = end_game_movement(finger_tips)

                        # Mostra su schermo la direzione del movimento
                        direction = f" MOVE: Horizontal: {direction_x}, Vertical: {direction_y}" #############################################################
                        cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (144, 66, 245), 2)
                        #if game.end:
                            #pass                                                           ##############display the instructions for ending game
                        # Invia comando al gioco se c'è un movimento
                        if direction_x != "Still":
                            send_direction_command(direction_x)
                        if direction_y != "Still":
                            send_direction_command(direction_y)
                        if gesture != "Unknown":
                            send_direction_command(gesture)

                    # Aggiorna le posizioni precedenti
                    prev_finger_x = avg_x
                    prev_finger_y = avg_y

                else:  # stai in pausa
                    cv2.putText(image, "PAUSE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)
                    # if stai usando il mouse
                    if is_mouse(finger_tips):
                        mouse = not mouse
                    if mouse:
                        click_move(finger_tips,clicking,image)
                        move_mouse(image, finger_tips, click_threshold, last_click_time, click_cooldown)


        # Mostra l'immagine con i punti di riferimento delle mani e la direzione del movimento
        cv2.imshow('Hand Tracking', image)

        #getting the original size of videocapture and then resizing the window by a scaling factor
        original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        new_height = int(original_height * 3)
        new_width = int(original_width * 3)

        cv2.moveWindow('Hand Tracking', 0, 0)
        cv2.resizeWindow('Hand Tracking', new_width, new_height)

        if cv2.waitKey(5) & 0xFF == 27:  # premi esc per chiudere
            break

# Rilascia la webcam e chiudi le finestre
cap.release()
cv2.destroyAllWindows()
