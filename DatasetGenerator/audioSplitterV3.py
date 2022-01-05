import requests
import sox
from config import COMPUTER_ID, SECRET, SESSION_NAME, FILE_NAME
from datetime import datetime
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Motivation for this splitter is a combo of the others

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

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

    # Get Offset from local recording to teams recording
    # In first demo that is 1 min 28 seconds.053 = 88.053
    # Second is 2 min 43 seconds .682 = 163.682
    offset = 163.682

    keypressArray = keyPressTimeStampArray[1:]

    wasLastWindow2 = False
    countSilentFiles = 0
    # For every keypress timestamp split the meeting audio into windows
    for keypress in keypressArray:
        print("Creating File for " + keypress['keyPressed'])

        # Convert keypress to storable format
        mappedKey = keypress['keyPressed']
        if(mappedKey == "."):
            mappedKey = "FullStop"
        elif(mappedKey == "!" or mappedKey == "1"):
            mappedKey = "1!"
        elif(mappedKey == "\\"):
            mappedKey = "ForwardsSlash"
        elif(mappedKey == "/"):
            mappedKey = "?"
        else:
            mappedKey = mappedKey

        # Get start of key press time
        keypressStartTime = offset + \
            convertTimestampIntoFloat(keypress['timeStamp'])

        # window we want is like 0.25 seconds either side of this time so we have a 0.5 second window
        windowStartTime = keypressStartTime - 0.25
        windowEndTime  = keypressStartTime + 0.25

        # Now right we need to handle keypress clustering
        # Large amounts of the time keypresses arent pressed individually
        # so we can use silence detection in here this window to normalise the audio files and also split them up further

        # First build a temp file
        tfm = sox.Transformer()
        tfm.trim(windowStartTime, windowEndTime)
        tfm.build_file('./InputAudioFiles/' + FILE_NAME, './SplitAudioFiles/temp.wav')

        # Now load temp file
        fileWindow = AudioSegment.from_wav('./SplitAudioFiles/temp.wav')

        # Split this file window up into chunks without the silence
        chunks = split_on_silence (
                    # Use the loaded audio.
                    fileWindow, 
                    # Specify that a silent chunk must be at least 0.25 seconds or 25 ms long.
                    min_silence_len = 25,
                    # Consider a chunk silent if it's quieter than -48
                    silence_thresh = -48
                )
        
        

        # Get current time
        time = datetime.now()

        # Now depending on chunks
        # Hopefully we just get 1 as one 1 wave in window but unlikely
        if(len(chunks) == 0):
            # All silence? so ignore but count
            wasLastWindow2 = False
            countSilentFiles = countSilentFiles + 1
            continue
        if(len(chunks) == 1):
            # One wave detected in window so take first wave and build sample file
            chunkToBuild = chunks[0]
            wasLastWindow2 = False
        elif(len(chunks) == 2):
            if wasLastWindow2:
                chunkToBuild = chunks[1]
            else:
                chunkToBuild = chunks[0]
                wasLastWindow2 = True
        else:
            # multiple chunk waves detected
            # since we take like a window around a timestamp we should take chunk thats in middle of ones found as most likely to be the correct wave
            chunkIndex = len(chunks) // 2
            chunkToBuild = chunks[chunkIndex] 
             



        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)

        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunkToBuild + silence_chunk
            
        # Normalize the entire chunk.
        # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        normalized_chunk = audio_chunk

        # Export the audio chunk with new bitrate.
        print("Exporting file for " + mappedKey)
        
        normalized_chunk.export(
            './SplitAudioFiles/' + mappedKey + '/' + mappedKey + '_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav',
            bitrate = "192k",
            format = "wav"
        )



        

    print("FINISHED SPLITTING")
    print("Number of silent files:", countSilentFiles)
else:
    print("Failed getting keypress data")



