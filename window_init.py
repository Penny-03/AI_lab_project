import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout
import ctypes
import win32gui

# Function to set window position and size
def set_window_pos_and_size(window_handle, x, y, width, height):
    ctypes.windll.user32.SetWindowPos(window_handle, 0, x, y, width, height, 0)

def get_window_handle(window_title):
    handle = win32gui.FindWindow(None, window_title)
    return handle

def window_combine():

    window_title1 = "Hand Tracking"  # Replace with the title of your first window
    window_title2 = "2048"  # Replace with the title of your second window

    window_handle1 = get_window_handle(window_title1)
    window_handle2 = get_window_handle(window_title2)

    app = QApplication(sys.argv)


    # Set the position and size of the first window
    set_window_pos_and_size(window_handle1, 0, 0, 800, 600)

    # Set the position and size of the second window next to the first window
    set_window_pos_and_size(window_handle2, 800, 0, 800, 800)

    # Create a new window to contain both windows
    main_window = QWidget()
    main_layout = QHBoxLayout()
    main_window.setLayout(main_layout)


    main_window.show()
    sys.exit(app.exec_())