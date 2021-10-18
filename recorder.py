import pyaudio
import wave
import datetime


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

# Class that handles recording sessions


class Recorder:

    sessionActive = False

    def __init__(self):
        self.p = pyaudio.PyAudio()

    def isRecordingSessionActive(self):
        return self.sessionActive

    def startNewRecordingSession(self, keyToRecord):
        self.sessionActive = True
        WAVE_OUTPUT_FILENAME = "KeyPressAudioFiles/" + keyToRecord + \
            "_" + datetime.datetime.utcnow().isoformat() + ".wav"
        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        print("Recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording Done")

        print("Writing To File")
        stream.stop_stream()
        stream.close()
        self.p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("Writing Done")

        self.sessionActive = False
