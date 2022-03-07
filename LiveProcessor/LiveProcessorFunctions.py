import librosa
import numpy as np
import sox
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


# Perform some audio processing on the file
# For now this is removing 0.3 seconds from start of file to remove white noise from blackhole implementation
# TODO: experiment with extracting percussive audio
def processAudio(audioFileName):
    tfm = sox.Transformer()
    tfm.trim(0.3)
    tfm.gain(20)
    tfm.build_file(audioFileName, './trimmed_buffer.wav')

    y, _ = librosa.load('./trimmed_buffer.wav')
    D = librosa.stft(y)
    _, D_percussive8 = librosa.decompose.hpss(D, margin=8)
    y_percussive8 = librosa.istft(D_percussive8, length=len(y))
    sf.write("./processed_buffer.wav",y_percussive8,22050)


# Separates the audio into hopefully keypress files
# returns the number of chunks
def separateAudio(audioFileName):
    fileToSplit = AudioSegment.from_wav(audioFileName)

    # Split track where the silence is 0.2 seconds or more and get chunks using 
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        fileToSplit, 
        # Specify that a silent chunk must be at least 0.05 seconds or 50 ms long.
        min_silence_len = 50,
        # Consider a chunk silent if it's quieter than -48
        silence_thresh = -32
    )

    print("Number of chunks found - ", len(chunks))

    

    # Process each chunk and export to a temp file
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        audio_chunk = audio_chunk.apply_gain(20)
        
        audio_chunk.export(
            './tempSplitFiles/' + str(i) + '.wav',
            bitrate = "192k",
            format = "wav"
        )

    return len(chunks)


# Given an audio file and a machine learning model
# features will be extracted and a prediction will be made and this will be returned
def makePredictionForFile(audioFileName, model, scaler):
    # Load file into librosa
    y, sr = librosa.load(audioFileName, sr=22050)

    if(y is None or len(y) == 0):
        # File too small to make prediction so just skip
        return ""
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
        scaledDatapoint = scaler.transform(reshapedDatapoint)
        output = model.predict(scaledDatapoint)

        prediction = output[0]
        if prediction == "Space":
            prediction = " "
        if prediction == "FullStop":
            prediction = "."

        return prediction
        

# Writes a word/ prediction to the file
def writeStringPredictionToFile(predictionString, textFileName):
    print("Writing to File...")
    f = open(textFileName, "a")
    f.write(predictionString)
    f.close()
    print("Finished Writing")

