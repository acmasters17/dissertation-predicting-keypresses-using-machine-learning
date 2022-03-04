import requests
import sox
from config import COMPUTER_ID, SECRET, SESSION_NAME, FILE_NAME
from datetime import datetime
import librosa
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import split_on_silence

print("Retrieving Key Press Data...")
# Load key press timestamps
ploads = {'secret': SECRET, 'id': COMPUTER_ID, 'sessionName': SESSION_NAME}
r = requests.post(
    'https://us-central1-dissertation---pkp.cloudfunctions.net/retrieveKeyPressDataForComputerNameSession', data=ploads)

# Takes in value like 0:00:05.509253
# and 0:01:05.761893 and converts it into just seconds
def convertTimestampIntoFloat(timestamp: str):
    minsAsSeconds = float(timestamp[2:4]) * 60
    seconds = float(timestamp[5:])
    return minsAsSeconds + seconds

def split(filepath):
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, min_silence_len = 100,silence_thresh = dBFS)

    print(len(chunks))
    return chunks


# Handle request
if(r.ok):
    print("Retrieved Key Press Data")
    keyPressTimeStampArray = r.json()["keyPressData"]
    print(len(keyPressTimeStampArray))

    # Get Offset from local recording to teams recording
    # In first demo that is 1 min 28 seconds.053 = 88.053
    # Second is 2 min 40 seconds .890 = 160.890
    offset = 160.890

    # For every keypress timestamp split the meeting audio
    for keypress in keyPressTimeStampArray:
        if(keypress['keyPressed'] == "START SESSION"):
            # Dont do anything as start of session key press
            print("STARTING SPLITTING")
        else:
            print("Creating File for " + keypress['keyPressed'])
            # Get start of key press time
            keypressStartTime = offset + \
                convertTimestampIntoFloat(keypress['timeStamp'])

            # window we want is like 0.25 seconds either side of this time so we have a 0.5 second window
            windowStartTime = keypressStartTime - 0.1
            windowEndTime  = keypressStartTime + 0.5

            


            # create transformer
            tfm = sox.Transformer()
            # add a command to trim the audio and get our window
            tfm.trim(windowStartTime, windowEndTime)
            tfm.gain(20)
            # Build a temporary file
            tfm.build_file('./InputAudioFiles/' + FILE_NAME, './window.wav')

            # Run percussive audio splitter
            y, sr = librosa.load('./window.wav')
            D = librosa.stft(y)
            D_harmonic8, D_percussive8 = librosa.decompose.hpss(D, margin=8)
            y_percussive8 = librosa.istft(D_percussive8, length=len(y))
            sf.write("window8.wav",y_percussive8,22050)

            # Run silence extractor
            chunks  = split('./window8.wav')
            # Save just the first silent chunk
            silence_chunk = AudioSegment.silent(duration=500)

            if len(chunks) == 0:
                # skip
                continue
            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunks[0] + silence_chunk
        
            # create an output file.
            time = datetime.now()
            if(keypress['keyPressed'] == "."):
                audio_chunk.export('./SplitAudioFiles/FullStop/FullStop_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav', bitrate = "192k", format = "wav")
            elif (keypress['keyPressed'] == "!" or keypress['keyPressed'] == "1"):
                audio_chunk.export('./SplitAudioFiles/1!/1!_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav', bitrate = "192k", format = "wav")
            elif (keypress['keyPressed'] == "\\"):
                audio_chunk.export('./SplitAudioFiles/ForwardsSlash/ForwardsSlash_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav', bitrate = "192k", format = "wav")
            else:
                audio_chunk.export('./SplitAudioFiles/' + keypress['keyPressed'] + '/' + keypress['keyPressed'] + '_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav', bitrate = "192k", format = "wav")

    print("FINISHED SPLITTING")
else:
    print("Failed getting keypress data")