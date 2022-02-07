import numpy as np
import pandas as pd
import pyaudio
import wave
from sklearn.svm import SVC
from config import INPUT_CSV_FILENAME
import keyboard
import librosa
import sox
from sklearn.neighbors import KNeighborsClassifier


# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/' + INPUT_CSV_FILENAME)

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values
# y = np.concatenate([y, y])

model = KNeighborsClassifier(n_neighbors=8)

model.fit(X, y)


# Start recording and processing
while True:
    # Record 2 second clips then process them and predict using fully trained model above
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 1
    

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=chunk)


    print("Recording Audio")
    frames = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        frames.append(data)

    print ("Finished Recording")
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Creating File")
    # write data to test WAVE file
    wf = wave.open("buffer.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Removing Silence")
    tfm = sox.Transformer()
    # Remove Silence
    tfm.silence(0)
    tfm.build_file('./buffer.wav', './silenced_buffer.wav')

    print("Processing of recorded audio")
    # Load file into librosa
    y, sr = librosa.load("./silenced_buffer.wav", sr=None)

    if(y is None or len(y) == 0):
        print("Prediction")
        print("Nothing")
    else:
        # Create an mfcc for file
        mfccForFile = librosa.feature.mfcc(y=y, sr=sr)

        datapoint = [] 
        for columnList in mfccForFile:
            # Calculate average mean
            total = 0
            for value in columnList:
                total += value

            mean = total / len(columnList)
            datapoint.append(mean)

        # We now have an x datapoint so predict
        reshapedDatapoint = np.reshape(datapoint, (1,-1))
        output = model.predict(reshapedDatapoint)

        print("Prediction")
        print(output)

    

    


