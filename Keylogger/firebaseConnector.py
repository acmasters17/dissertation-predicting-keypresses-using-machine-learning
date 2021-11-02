
# import aiohttp
# import asyncio


# async def main():

#     async with aiohttp.ClientSession() as session:

#         pokemon_url = 'https://pokeapi.co/api/v2/pokemon/151'
#         async with session.get(pokemon_url) as resp:
#             pokemon = await resp.json()
#             print(pokemon['name'])

# asyncio.run(main())

import requests
import constants
import json
from debouncer import debounce


class FirebaseConnector:

    sessionActive = False
    keypressBuffer = []

    def __init__(self):
        self.getShouldBeStoringKeypressData()

    # Makes a request to firebase to ask if should be storing key press data for the running computer
    def getShouldBeStoringKeypressData(self):
        # Fire Request
        ploads = {'secret': constants.secret, 'id': constants.computerId}
        r = requests.post(
            'https://us-central1-dissertation---pkp.cloudfunctions.net/getShouldBeStoringKeyPressData', data=ploads)

        # Handle request
        if(r.ok):
            self.sessionActive = r.json()["status"]
            print("Session Active - {0}".format(self.sessionActive))

    # {"keyPressed":"a","timeStamp":"01-11-2021_10:05:09"}
    # Adds current keypress to buffer and calls a send

    def storeKeypressData(self, keypressData):
        print("Adding to buffer")
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
        ploads = {'secret': constants.secret, 'id': constants.computerId,
                  "newKeypressData": json.dumps(self.keypressBuffer, separators=(',', ':'))}
        r = requests.post(
            'https://us-central1-dissertation---pkp.cloudfunctions.net/storeKeyPressDataForComputerName', data=ploads)

        # If Synced Properly clear the buffer
        if(r.ok):
            self.keypressBuffer = []
            print("Synced")

    def isRecordingSessionActive(self):
        return self.sessionActive
