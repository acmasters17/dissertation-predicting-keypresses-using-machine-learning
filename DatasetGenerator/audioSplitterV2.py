import requests
import sox
from config import COMPUTER_ID, SECRET, SESSION_NAME, FILE_NAME, KEYLOGGER_START_OFFSET_IN_MS
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

# Second version of audio splitter
# This attempt is based on the assumption that all sounds found will be a keypress and that order will be same
# going to use pydub
print("Loading Audio...")
teamsRecording = AudioSegment.from_wav('./InputAudioFiles/' + FILE_NAME)
print("Loaded Audio")

# We want to skip the first offset seconds as thats when the keylogger is not running
recording = teamsRecording[KEYLOGGER_START_OFFSET_IN_MS:]

print(len(recording))

# Split track where the silence is 0.2 seconds or more and get chunks using 
# the imported function.
chunks = split_on_silence (
    # Use the loaded audio.
    recording, 
    # Specify that a silent chunk must be at least 0.05 seconds or 50 ms long.
    min_silence_len = 25,
    # Consider a chunk silent if it's quieter than -48
    silence_thresh = -54
)

print("Number of keypress audio chunks found - ", len(chunks))

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


# Handle request
if(r.ok):
    print("Retrieved Key Press Data")
    keyPressTimeStampArray = r.json()["keyPressData"]
    print(len(keyPressTimeStampArray))

    print("Starting Mapping...")
    keyPressArray = keyPressTimeStampArray[1:]

    # Process each chunk / we should map chunk to keypress
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Check if we are still mapping within keypress array range
        if(i < len(keyPressArray)):
            # Now map audio chunk to keypress
            mappedKey = (keyPressArray[i])['keyPressed']
            print("Creating File for " + mappedKey)

            # Convert mapped key to storable name if problem
            if(mappedKey == "."):
                mappedKey = "FullStop"
            elif(mappedKey == "!" or mappedKey == "1"):
                mappedKey = "1!"
            else:
                mappedKey = mappedKey
        else:
            # Outside of range we know so set mapped key to be N/A
            mappedKey = "Unknown"

        # Get current time
        time = datetime.now()


        # # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        # Export the audio chunk with new bitrate.
        print("Exporting file for " + mappedKey)
        
        normalized_chunk.export(
            './SplitAudioFiles/' + mappedKey + '/' + mappedKey + '_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav',
            bitrate = "192k",
            format = "wav"
        )


    print("FINISHED SPLITTING")
else:
    print("Failed getting keypress data")





