from pynput import keyboard
import recorder

print("Starting Key Logger Program")
print("----------------------------------")
print(" - Press r to initiate a 3 second recording window")
print(" - Press esc to exit the key logger")

# Initialise Recorder
keypressRecorder = recorder.Recorder()

# On Press Function
def on_press(key):
    try:
        # If key is r and recording session is not active ask for what is going to be recorded then start a new recording
        if(key.char == "r" and keypressRecorder.isRecordingSessionActive() == False):
            # Start new recording session
            keyName = input("Please enter the key you are about to record and then hit enter to start recording: ")
            keypressRecorder.startNewRecordingSession(keyName)
        else:
            # Don't do anthing
            print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press,
#     on_release=on_release)
# listener.start()

