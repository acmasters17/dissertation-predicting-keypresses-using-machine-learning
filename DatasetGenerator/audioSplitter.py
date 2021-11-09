import requests
import sox
from config import COMPUTER_ID, SECRET, SESSION_NAME
from datetime import datetime

print("Retrieving Key Press Data...")
# Load key press timestamps
ploads = {'secret': SECRET, 'id': COMPUTER_ID, 'sessionName': SESSION_NAME}
r = requests.post(
    'https://us-central1-dissertation---pkp.cloudfunctions.net/retrieveKeyPressDataForComputerNameSession', data=ploads)

# Takes in value like 0:00:05.509253
# and 0:01:05.761893 and converts it into just seconds
def convertTimestampIntoFloat(timestamp:str):
    minsAsSeconds = float(timestamp[2:4]) * 60
    seconds = float(timestamp[5:])
    return minsAsSeconds + seconds

# Handle request
if(r.ok):
    print("Retrieved Key Press Data")
    keyPressTimeStampArray = r.json()["keyPressData"]
    print(len(keyPressTimeStampArray))

    # Get Offset from local recording to teams recording
    # In first demo that is 1 min 28 seconds.053
    offset = 88.053

    # For every keypress timestamp split the meeting audio 
    for keypress in keyPressTimeStampArray:
        if(keypress['keyPressed'] == "START SESSION"):
            # Dont do anything as start of session key press
            print("STARTING SPLITTING")
        else:
            print("Creating File for " + keypress['keyPressed'])
            # Get start of key press time
            keypressStartTime = offset + convertTimestampIntoFloat(keypress['timeStamp'])
            # create transformer
            tfm = sox.Transformer()
            # add a command to trim the audio between keypressStartTime and .5 seconds after
            tfm.trim(keypressStartTime, keypressStartTime + 0.5)
            # create an output file.
            time = datetime.now()
            tfm.build_file('./InputAudioFiles/Test Bed 1.wav', './SplitAudioFiles/' + keypress['keyPressed'] + '_' + time.strftime("%d-%m-%Y_%H:%M%:%S:%f") + '.wav')
    
    print("FINISHED SPLITTING")
else :
    print("Failed getting keypress data")
