# import the needed libraries
import pyautogui
import cv2
import time
import math
import keyboard


# function for calculating the distance between two given points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)


# function for PAUSING the game: put the game in pause if thumb and pinky touch and if another pause
# was not made within the last second
def is_pause(finger_tips, last_pause):
    current_time = time.time()
    if current_time - last_pause > 1.0:
        last_pause = current_time
        return calculate_distance(finger_tips[0], finger_tips[4]) < 0.05, last_pause
    return False, last_pause


# function for CLICKING: the click is read only if you are in pause, if thumb and ring finger touch, and
# another click was not made in the last second
def is_click(image, finger_tips, last_click_time, click_cooldown):
    current_time = time.time()
    if calculate_distance(finger_tips[0], finger_tips[3]) < 0.05 and (
            current_time - last_click_time > click_cooldown):
        last_click_time = current_time
        # overlay on the video that there has been a click
        cv2.putText(image, "Click!", (120, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (66, 166, 254), 2)
        return True, last_click_time
    return False, last_click_time


# function for verifying if we are entering MOUSE mode: put the game in mouse mode if thumb and
# middle finger touch and there has not been a mouse mode in the last second
def is_mouse(finger_tips, last_mouse):
    current_time = time.time()
    if current_time - last_mouse > 1.0:
        last_mouse = current_time
        return calculate_distance(finger_tips[0], finger_tips[2]) < 0.05, last_mouse
    return False, last_mouse


# function for MOVING the MOUSE cursor
def move_mouse(image, finger_tips, last_click_time, click_cooldown):
    screen_width, screen_height = pyautogui.size()
    index_tip = finger_tips[1]
    h, w, _ = image.shape
    cx, cy = int(index_tip.x * w), int(index_tip.y * h)

    # convert the finger coordinates to screen coordinates
    screen_x = int(index_tip.x * screen_width)
    screen_y = int(index_tip.y * screen_height)

    # move the mouse to the coordinates
    pyautogui.moveTo(screen_x, screen_y)

    # verify if there is a click and update the last click time
    isclick = is_click(image, finger_tips, last_click_time, click_cooldown)
    if isclick[0]:
        last_click_time = isclick[1]
        pyautogui.click()

    # draw a circle on the index fingertip to indicate the cursor
    cv2.circle(image, (cx, cy), 10, (66, 166, 254), -1)
    # overlay on the video the fact that we are in mouse mode
    cv2.putText(image, "MOUSE", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)
    # return the last click time to update the global variable
    return last_click_time


# function for moving objects on the screen: if thumb and ring finger hold for a longer period of time
def click_move(finger_tips, clicking, image):
    if calculate_distance(finger_tips[0], finger_tips[3]) < 0.05:
        # overlay on the video the fact that we are holding the click button and the program is ready to
        # move the objects
        cv2.putText(image, "HOLDING", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 73, 255), 2)
        if not clicking:
            clicking = True
            # if we are clicking for a long time hold the mouse down
            pyautogui.mouseDown(button='left')
        else:
            current_pos = finger_tips[1]
            pyautogui.moveTo(current_pos[0], current_pos[1])
    else:
        if clicking:
            clicking = False
            # if we are not clicking anymore hold the mouse up
            pyautogui.mouseUp(button='left')
    return clicking


# function to determine whether the ending movement indicates a yes or a no
def end_game_movement(finger_tips):
    # if thumb and pinky touch then restart the game
    if calculate_distance(finger_tips[0], finger_tips[4]) < 0.05:
        return "No"
    # if thumb and index touch then quit the game
    if calculate_distance(finger_tips[0], finger_tips[1]) < 0.05:
        return "Yes"
    else:
        return "Unknown"


# function for sending the commands detected by hand movements to the game
def send_direction_command(direction):
    if direction == "Up":
        keyboard.press_and_release('w')
    elif direction == "Left":
        keyboard.press_and_release('a')
    elif direction == "Down":
        keyboard.press_and_release('s')
    elif direction == "Right":
        keyboard.press_and_release('d')
    elif direction == "Yes":
        keyboard.press_and_release('y')
    elif direction == "No":
        keyboard.press_and_release('n')
