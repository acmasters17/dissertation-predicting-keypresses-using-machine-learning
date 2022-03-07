import pandas as pd
import pyaudio
import wave
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from config import INPUT_CSV_FILENAME, PREDICTION_SESSION_NAME
from LiveProcessorFunctions import *


# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/' + INPUT_CSV_FILENAME)

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values
# y = np.concatenate([y, y])


X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.20)
model = SVC(kernel="rbf")
scaler = StandardScaler()
X_scaled_train = scaler.fit_transform(X_train,y_train)
model.fit(X_scaled_train,y_train)

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
print(info)
numdevices = info.get('deviceCount')
print(numdevices)
for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))




# Start recording and processing
while True:
    # Record 5 second clips then process them and predict using fully trained model above
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10
    

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=1,
                frames_per_buffer=chunk)


    print("Recording Audio...")
    frames = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print ("Finished Recording")

    print("Creating Initial File...")
    # write data to test WAVE file
    wf = wave.open("buffer.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("Process audio")
    processAudio("./buffer.wav")


    print("Now split file")
    numFilesToPredict = separateAudio("./processed_buffer.wav")

    print("Now make predictions")
    prediction = ""

    for i in range(0,numFilesToPredict):
        character = makePredictionForFile('./tempSplitFiles/' + str(i) + '.wav', model, scaler)

        # Append character to prediction
        prediction = prediction + character

    print("Finished Predictions now write to file")
    writeStringPredictionToFile(prediction, PREDICTION_SESSION_NAME)

    cleanUpDirectory(numFilesToPredict)
    exit(0)
    
    

    


