from glob import glob
import librosa
import csv
from config import OUTPUTCSVNAME

# File takes list of audio files, extracts features using librosa and stores them in a csv

# Retrieve a list of all audio file paths
data_dir = "./SplitAudioFiles/*/*.wav"
audio_files_paths = glob(data_dir,recursive=True)
print("Found " + str(len(audio_files_paths)) + " Audio Files")

print(audio_files_paths[0])

print("Starting Feature Extraction Process")
# For every file we need to load it
# Extract its features via librosa
# Get a lable for it - can find this from name
# Squash feature array into one row and add label to end
# Concatenate these all together into a csv
outputRows = []
for filepath in audio_files_paths:
   # Get label for file
   # All in format ./SplitAudioFiles/R/ so can split on / and take 2nd slice
   stringSliced = filepath.rsplit("/")
   label = stringSliced[2]

   if(label == "Unknown"):
      # Skip
      continue

   print("Extracting Features for " + label)

   # Load file into librosa
   y, sr = librosa.load(filepath, sr=None)

   if(y is None or len(y) == 0):
      print("Found empty file")
      continue

   # Create an mfcc for file
   mfccForFile = librosa.feature.mfcc(y=y, sr=sr)

   row = [] 
   for columnList in mfccForFile:
      # Calculate average mean
      total = 0
      for value in columnList:
         total += value

      mean = total / len(columnList)
      row.append(mean)

   row.append(label)
   outputRows.append(row)

print("Finished Feature Extraction Process")
print("Saving...")

# Saving the file
outputCSV = "./DataSets/" + OUTPUTCSVNAME
with open(outputCSV,"+w") as f:
 csv_writer = csv.writer(f, delimiter = ",")
 csv_writer.writerows(outputRows)

print("Saved")








