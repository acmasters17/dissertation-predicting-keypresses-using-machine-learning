import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

# Script takes in a specified audio file path and produces a mel-scaled spectrogram
AUDIO_FILE_PATH = "./SplitAudioFiles/A/a_09-11-2021_12:28:46:114932.wav"
KEPRESS_LABEL = "A 09/11/2021"

# Load specified audio file
print("Loading audio file...")
y, sr = librosa.load(AUDIO_FILE_PATH)
print("Audio File Loaded")

# Create spectogram
# Test
print("Creating Spectogram...")
spectogram = librosa.feature.melspectrogram(y=y, sr=sr)
print("Created Spectogram")

# Passing through arguments to the Mel filters
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)

# Visualising spectogram
fig, ax = plt.subplots()
S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax)
fig.colorbar(img, ax=ax, format='%+2.0f dB')
ax.set(title="Mel-frequency spectrogram for " + KEPRESS_LABEL)
plt.show()
