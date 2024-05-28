
def start():
    import cv2
    import mediapipe as mp
    import time

    # Inizializza Mediapipe Hands e le utilità di disegno
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    # Imposta la webcam
    cap = cv2.VideoCapture(0)

    # Variabili per tracciare il movimento delle dita
    prev_finger_x = None
    prev_finger_y = None
    prev_index_y = None
    movement_threshold = 30  # Soglia per determinare un movimento significativo
    click_threshold = 20  # Soglia per determinare un clic
    click_cooldown = 1.0  # Tempo di attesa tra un clic e l'altro (in secondi)
    last_click_time = 0

    # Usa Hands di Mediapipe
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
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
                    
                    # Ottieni le coordinate delle punte delle dita
                    finger_tips = [
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    ]
                    index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0]
                    # Ottieni le coordinate del polso e delle punte delle dita
                    wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0]
                    middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * frame.shape[0]
                    ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * frame.shape[0]
                    pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * frame.shape[0]
                    
                    # Determina se le dita sono abbassate rispetto al polso
                    fingers_lowered = middle_y > wrist_y and ring_y > wrist_y and pinky_y > wrist_y
                    
                    
                    avg_x = sum([tip.x for tip in finger_tips]) / 5 * frame.shape[1]
                    avg_y = sum([tip.y for tip in finger_tips]) / 5 * frame.shape[0]
                    
                    # Determina la direzione del movimento
                    if prev_finger_x is not None and prev_finger_y is not None:
                        if avg_x - prev_finger_x > movement_threshold:
                            direction_x = "Right"
                        elif prev_finger_x - avg_x > movement_threshold:
                            direction_x = "Left"
                        else:
                            direction_x = "Still"

                        if avg_y - prev_finger_y > movement_threshold:
                            direction_y = "Down"
                        elif prev_finger_y - avg_y > movement_threshold:
                            direction_y = "Up"
                        else:
                            direction_y = "Still"
                        
                        # Mostra la direzione del movimento
                        direction = f"Horizontal: {direction_x}, Vertical: {direction_y}"
                        cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (144, 66, 245), 2)

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
start()
