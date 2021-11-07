import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


class Recorder:
    fileName = ""
    frames = []
    recording = False

    def __init__(self):
        self.p = pyaudio.PyAudio()

    def startLocalRecording(self, fileName):
        print("Starting Local Audio Recording")

        self.fileName = fileName

        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

        print("Recording")
        self.frames = []
        recording = True
        while(recording == True):
            data = self.stream.read(CHUNK)
            self.frames.append(data)

    def stopLocalRecording(self):
        print("Stopped Recording")
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        print("Saving Recording...")
        wf = wave.open(self.fileName, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print("Saved Recording")
