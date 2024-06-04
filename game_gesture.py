# importing necessary libraries
import mediapipe as mp
import threading
import subprocess
from functions_movement import *
import cv2
import pygetwindow as gw

# initialize mediapipe and the drawing utils
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles

# global variables to keep track of hand and finger movement
prev_finger_x = None
prev_finger_y = None
prev_index_y = None
movement_threshold = 10
movement_cooldown = 0.3
click_cooldown = 1.0  # time between one click and another
last_click_time = 0
last_mov_time = 0
last_mouse = 0
last_pause = 0
pause = True  # used to put the game in pause
mouse = False  # used to put the game in mouse mode
clicking = False  # used to see if we are holding the click


# determine the webcam on which to take the videocapture
cap = cv2.VideoCapture(0)


# function to start the 2048 game
def start_game():
    subprocess.run(["python", "main.py"])


# start the game on a separate thread
game_thread = threading.Thread(target=start_game)
game_thread.start()

# program sleeps so the game has time to start and then moves the window to a certain spot on the screen,
# also opens a window where the videocapture will be
screen_width, screen_height = pyautogui.size()
cv2.namedWindow('Hand Tracking', cv2.WINDOW_NORMAL)
time.sleep(3)
game_window = gw.getWindowsWithTitle('2048')[0]
game_window.resizeTo(500, 800)
game_window.moveTo(screen_width - 768, screen_height - 1000)

# using mediapipe hands, start the loop for recognizing and handling hand movements and gestures
with mp_hands.Hands(
        static_image_mode=False,  # to make it work in live stream
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        # mirroring the image to get a mirror effect, and for easier playing
        image = cv2.flip(img, 1)
        # process each frame of the video and apply the hand landmarks
        results = hands.process(image)
        # check if any hands were captured
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # physically draw the landmarks on the hands, this can be modified to have different styles
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_style.get_default_hand_landmarks_style())

                # get the coordinates for each fingertip
                finger_tips = [
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],  # 0
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],  # 1
                    hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],  # 2
                    hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],  # 3
                    hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]  # 4
                ]

                # check if the pause gesture is made, if yes change the pause variable to actually put the game in pause
                ispause = is_pause(finger_tips, last_pause)
                if ispause[0]:
                    pause = not pause
                    last_pause = ispause[1]

                # if no pause was detected enter, and check for hand movements to move the tiles
                if not pause:

                    # get the current finger positions
                    x_point = finger_tips[1].x * image.shape[1]
                    y_point = finger_tips[1].y * image.shape[0]

                    current_time = time.time()
                    # check for movement on x-axis
                    if prev_finger_x is not None and prev_finger_y is not None:
                        if x_point - prev_finger_x > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_x = "Right"
                            last_mov_time = current_time
                        elif prev_finger_x - x_point > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_x = "Left"
                            last_mov_time = current_time
                        else:
                            direction_x = "Still"

                        # check for movement on y-axis
                        if y_point - prev_finger_y > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_y = "Down"
                            last_mov_time = current_time
                        elif prev_finger_y - y_point > movement_threshold and (
                                current_time - last_mov_time > click_cooldown):
                            direction_y = "Up"
                            last_mov_time = current_time
                        else:
                            direction_y = "Still"

                        # calling function to determine the ending movement meaning, when the end of the game is reached
                        gesture = end_game_movement(finger_tips)

                        # overlay on the video screen the direction of movement
                        direction = f"MOVE: Horizontal = {direction_x}, Vertical = {direction_y}"
                        cv2.putText(image, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)

                        # send command to game, if any was detected
                        if direction_x != "Still":
                            send_direction_command(direction_x)
                        if direction_y != "Still":
                            send_direction_command(direction_y)
                        if gesture != "Unknown":
                            send_direction_command(gesture)

                    # update the previous finger positions
                    prev_finger_x = x_point
                    prev_finger_y = y_point

                # if instead you are in pause mode, overlay on the video the fact you are in pause
                else:
                    cv2.putText(image, "PAUSE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)
                    # if the movement to switch between pause mode and mouse mode was detected, change the mouse
                    # variable to actually enter mouse mode
                    ismouse = is_mouse(finger_tips, last_mouse)
                    if ismouse[0]:
                        last_mouse = ismouse[1]
                        mouse = not mouse
                    # and enter the mouse mode
                    if mouse:
                        # check if there is a holding click, to move objects on the screen
                        click_move(finger_tips, clicking, image)
                        # move the mouse and determine the last click time, returned by the function
                        last_click_time = move_mouse(image, finger_tips, last_click_time, click_cooldown)

        # display the instructions for ending the game on the video
        cv2.rectangle(image, (5, 385), (425, 470), (66, 212, 254), -1)
        cv2.putText(image, 'When you reach the end of the game:', (10, 400),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108, 108, 108), 1)
        cv2.putText(image, '- to play again -> touch thumb and index finger', (10, 420),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108, 108, 108), 1)
        cv2.putText(image, '- to exit the game -> touch thumb and pinky', (10, 440),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (108, 108, 108), 1)

        # show the image with the hand landmarks and the various overlaid text
        cv2.imshow('Hand Tracking', image)

        # resizing the videocapture window to fit full screen size
        cv2.moveWindow('Hand Tracking', 0, 0)
        cv2.resizeWindow('Hand Tracking', screen_width, screen_height)

        # press ESC to close the videocapture
        if cv2.waitKey(5) & 0xFF == 27:
            break

# release the webcam and close all open windows
cap.release()
cv2.destroyAllWindows()
