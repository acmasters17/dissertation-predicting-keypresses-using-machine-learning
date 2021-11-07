import requests
from constants import COMPUTER_ID, SECRET
import json
from debouncer import debounce


class FirebaseConnector:

    sessionActive = False
    keypressBuffer = []

    def __init__(self):
        self.getShouldBeStoringKeypressData()

    # Makes a request to firebase to ask if should be storing key press data for the running computer
    def getShouldBeStoringKeypressData(self):
        print("Connecting to Firebase Session...")
        # Fire Request
        ploads = {'secret': SECRET, 'id': COMPUTER_ID}
        r = requests.post(
            'https://us-central1-dissertation---pkp.cloudfunctions.net/getShouldBeStoringKeyPressData', data=ploads)

        # Handle request
        if(r.ok):
            self.sessionActive = r.json()["status"]
            print("Connected, Session Active - {0}".format(self.sessionActive))

    # {"keyPressed":"a","timeStamp":"01-11-2021_10:05:09"}
    # Adds current keypress to buffer and calls a send

    def storeKeypressData(self, keypressData):
        # Add to buffer
        self.keypressBuffer.append(keypressData)
        # Call send
        self.syncKeypressData()

    # If should be storing data then send keypress array of data to be stored
    # Should be an array of key presses and timestamps
    # [{"keyPressed":"a","timeStamp":"01-11-2021_10:05:09"},{...}]"
    @debounce(10)
    def syncKeypressData(self):
        if(self.sessionActive == False):
            print("Session Not Active")
            self.keypressBuffer = []
            return

        print("Syncing...")
        # Fire Request with array
        ploads = {'secret': SECRET, 'id': COMPUTER_ID,
                  "newKeypressData": json.dumps(self.keypressBuffer, separators=(',', ':'))}
        r = requests.post(
            'https://us-central1-dissertation---pkp.cloudfunctions.net/storeKeyPressDataForComputerName', data=ploads)

        # If Synced Properly clear the buffer
        if(r.ok):
            self.keypressBuffer = []
            print("Synced")

    def isRecordingSessionActive(self):
        return self.sessionActive
