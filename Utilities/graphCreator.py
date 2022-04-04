import wave
import matplotlib.pyplot as plt
import librosa
import librosa.display
import numpy as np
import soundfile as sf


# Script takes in a specified audio file path and produces a mel-scaled spectrogram
AUDIO_FILE_PATH = "../LiveProcessor/buffer.wav"
KEPRESS_LABEL = "Buffer File"

# Load specified audio file
print("Loading audio file...")
y, sr = librosa.load(AUDIO_FILE_PATH)
print("Audio File Loaded")


# Test
fig, ax = plt.subplots(nrows=3, sharex=True)
librosa.display.waveshow(y, sr=sr, ax=ax[0])
ax[0].set(title='Mono View of Audio')
ax[0].label_outer()
# Create spectogram
print("Creating Spectogram...")
spectogram = librosa.feature.melspectrogram(y=y, sr=sr)
print("Created Spectogram")

y_harm, y_perc = librosa.effects.hpss(y)
librosa.display.waveshow(y_harm, sr=sr, alpha=0.5, ax=ax[1], label='Harmonic')
librosa.display.waveshow(y_perc, sr=sr, color='r', alpha=0.5, ax=ax[1], label='Percussive')
ax[1].set(title='Multiple waveforms')
ax[1].legend()

# Passing through arguments to the Mel filters
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,
                                    fmax=8000)

S_dB = librosa.power_to_db(S, ref=np.max)
img = librosa.display.specshow(S_dB, x_axis='time',
                         y_axis='mel', sr=sr,
                         fmax=8000, ax=ax[2])
fig.colorbar(img, ax=ax[2], format='%+2.0f dB')
ax[2].set(title="Mel-frequency spectrogram for " + KEPRESS_LABEL)
plt.show()


print("Saving Recording...")
D = librosa.stft(y)
D_harmonic2, D_percussive2 = librosa.decompose.hpss(D, margin=2)
D_harmonic4, D_percussive4 = librosa.decompose.hpss(D, margin=4)
D_harmonic8, D_percussive8 = librosa.decompose.hpss(D, margin=8)
D_harmonic16, D_percussive16 = librosa.decompose.hpss(D, margin=16)

y_percussive2 = librosa.istft(D_percussive2, length=len(y))
y_percussive4 = librosa.istft(D_percussive4, length=len(y))
y_percussive8 = librosa.istft(D_percussive8, length=len(y))
y_percussive16 = librosa.istft(D_percussive16, length=len(y))

sf.write("test2.wav",y_percussive2,22050)
sf.write("test4.wav",y_percussive4,22050)
sf.write("test8.wav",y_percussive8,22050)
sf.write("test16.wav",y_percussive16,22050)
print("Saved Recording")


