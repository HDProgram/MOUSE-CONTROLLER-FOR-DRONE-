# MOUSE-CONTROLLER-FOR-DRONE-
Python script that allows users to control a drone using mouse inputs. It leverages the pynput library for mouse events and a custom drone control library called plutocontrol.
The script supports various drone commands such as arming, taking off, landing, and directional movements based on mouse actions.

Features
Mouse Click Actions:
Left-click: Arm the drone.
Right-click: Land the drone.
Double left-click: Take off.
Double right-click: Disarm the drone.
Mouse Movement:
Move the mouse right/left: Move the drone right/left.
Move the mouse forward/backward: Move the drone forward/backward.
Mouse Scroll:
Scroll up: Increase the drone's height.
Scroll down: Decrease the drone's height.

#The main components of the script are:

Global Variables:

keep_running: A flag to control the listener loop.
prevx, prevy: Variables to track the previous mouse positions.
last_click_time: Variable to detect double clicks.
move_threshold: The minimum pixel movement required to trigger a drone movement.
identify_mouse_action(action, x, y, button, pressed, dx, dy, keep_run):

Identifies and handles various mouse actions (click, double click, move, scroll) to send corresponding commands to the drone.
on_click(x, y, button, pressed):

Handles mouse click events.
on_move(x, y):

Handles mouse movement events.
on_scroll(x, y, dx, dy):

Handles mouse scroll events.
start_listener():

Starts the mouse listener in a separate thread.
clean_exit():

Ensures a clean exit by disarming and disconnecting the drone.
Main Loop:

Initiates the listener thread and maintains the main loop until a keyboard interrupt is caught.

