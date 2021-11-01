
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

secret = "V3UDaLge29tD3Uddje3FRs3CCAcjzuuQ"


class FirebaseConnector:

    sessionActive = False

    def __init__(self):
        self.getShouldBeStoringKeypressData()

    def getShouldBeStoringKeypressData(self):
        ploads = {'secret': secret, 'id': "test"}
        r = requests.post('https://us-central1-dissertation---pkp.cloudfunctions.net/getShouldBeStoringKeyPressData', data=ploads)
        print(r.json())

    def isRecordingSessionActive(self):
        return self.sessionActive
