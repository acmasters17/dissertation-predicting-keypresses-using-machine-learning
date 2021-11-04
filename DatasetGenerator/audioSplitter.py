import requests
from DatasetGenerator.config import COMPUTER_ID, SECRET

# Load key press data for session specified in config
ploads = {'secret': SECRET, 'id': COMPUTER_ID}
r = requests.post(
    'https://us-central1-dissertation---pkp.cloudfunctions.net/getShouldBeStoringKeyPressData', data=ploads)

# Handle request
# if(r.ok):
#     self.sessionActive = r.json()["status"]
#     print("Session Active - {0}".format(self.sessionActive))
