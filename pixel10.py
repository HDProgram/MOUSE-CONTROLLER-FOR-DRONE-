from pynput import mouse
from plutocontrol import pluto
from threading import Thread
import time

# Initialize and connect to the drone
my_pluto = pluto()
my_pluto.connect()
time.sleep(2)

# Global flag to control the listener loop
keep_running = True
prevx = 0
prevy = 0

# Variables for double-click detection
last_click_time = 0
double_click_threshold = 1.0  # seconds

# Movement threshold
move_threshold = 500 # pixels

def identify_mouse_action(action, x, y, button, pressed, dx, dy, keep_run):
    global prevy
    global prevx
    if action == 'click':
        if button == mouse.Button.left and pressed:
            print("Left click: Arming")
            my_pluto.arm()
        elif button == mouse.Button.left and not pressed:
            print("Left click released")
        elif button == mouse.Button.right and pressed:
            print("Right click: Landing")
            my_pluto.land()
        elif button == mouse.Button.right and not pressed:
            print("Right click released")
    elif action == 'double_click':
        if button == mouse.Button.left:
            print("Double left click: Taking off")
            my_pluto.take_off()
        elif button == mouse.Button.right:
            print("Double right click: Disarming")
            my_pluto.disarm()
    elif keep_running and action == 'move':
        dx = x - prevx
        dy = y - prevy
        if abs(dx) >= move_threshold:
            if dx > 0:
                print("Moving right")
                my_pluto.right()
            else:
                print("Moving left")
                my_pluto.left()
            prevx = x
        if abs(dy) >= move_threshold:
            if dy > 0:
                print("Moving backward")
                my_pluto.backward()
            else:
                print("Moving forward")
                my_pluto.forward()
            prevy = y
    elif keep_running and action == 'scroll':
        if dy > 0:
            print("Increasing height")
            my_pluto.increase_height()
        elif dy < 0:
            print("Decreasing height")
            my_pluto.decrease_height()
    elif not keep_running:
        clean_exit()

def on_click(x, y, button, pressed):
    global last_click_time
    current_time = time.time()
    if pressed:
        if current_time - last_click_time <= double_click_threshold:
            identify_mouse_action('double_click', x, y, button, pressed, None, None, keep_running)
        else:
            identify_mouse_action('click', x, y, button, pressed, None, None, keep_running)
    last_click_time = current_time

def on_move(x, y):
    identify_mouse_action('move', x, y, None, None, None, None, keep_running)

def on_scroll(x, y, dx, dy):
    identify_mouse_action('scroll', x, y, None, None, dx, dy, keep_running)

def start_listener():
    # Start the mouse listener in a separate thread
    print("Starting mouse listener...")
    listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)
    listener.start()
    listener.join()

def clean_exit():
    global keep_running
    global prevy
    global prevx
    keep_running = False
    try:
        print("Disarming...")
        my_pluto.disarm()
        time.sleep(2)
        print("Disconnecting...")
        my_pluto.disconnect()
    except Exception as e:
        prevx = 0
        prevy = 0
        print(f"Exception during cleanup: {e}")
    finally:
        print("Exiting...")
        exit()

# Main loop
if __name__ == "__main__":
    listener_thread = Thread(target=start_listener)
    listener_thread.start()

    try:
        while keep_running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        keep_running = False
        print("KeyboardInterrupt caught. Exiting...")
        clean_exit()
    
    listener_thread.join()
