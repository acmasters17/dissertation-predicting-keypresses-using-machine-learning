import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np

# Script takes in a specified audio file path and produces a mel-scaled spectrogram
AUDIO_FILE_PATH = "./silenced_buffer.wav"
KEPRESS_LABEL = "Buffer File"

# Load specified audio file
print("Loading audio file...")
y, sr = librosa.load(AUDIO_FILE_PATH)
print("Audio File Loaded")


# Test
fig, ax = plt.subplots(nrows=3, sharex=True)
librosa.display.waveshow(y, sr=sr, ax=ax[0])
ax[0].set(title='Envelope view, mono')
ax[0].label_outer()
# Create spectogram
print("Creating Spectogram...")
spectogram = librosa.feature.melspectrogram(y=y, sr=sr)
print("Created Spectogram")

y_harm, y_perc = librosa.effects.hpss(y)
librosa.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax[2], label='Harmonic')
librosa.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax[2], label='Percussive')
ax[2].set(title='Multiple waveforms')
ax[2].legend()

# Passing through arguments to the Mel filters
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)

S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax[1])
fig.colorbar(img, ax=ax[1], format='%+2.0f dB')
ax[1].set(title="Mel-frequency spectrogram for " + KEPRESS_LABEL)
plt.show()
