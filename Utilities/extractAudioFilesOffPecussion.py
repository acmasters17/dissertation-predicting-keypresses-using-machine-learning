import wave
import matplotlib.pyplot as plt
import librosa
import librosa.display
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
from scipy.fft import rfft, rfftfreq


# Script takes in a specified audio file path and produces a mel-scaled spectrogram
AUDIO_FILE_PATH = "./test8.wav"
KEPRESS_LABEL = "Buffer File"

# Load specified audio file
print("Loading audio file...")
y, sr = librosa.load(AUDIO_FILE_PATH)
print("Audio File Loaded")

fig, ax = plt.subplots(nrows=3, sharex=True)
librosa.display.waveshow(y, sr=sr, ax=ax[0])
ax[0].set(title='Mono View of Audio')
ax[0].label_outer()



plt.show()


def split(filepath):
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 100,
        silence_thresh = dBFS)

    print(len(chunks))
    return chunks


chunks  = split(AUDIO_FILE_PATH)

# Process each chunk and export to a temp file
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
    silence_chunk = AudioSegment.silent(duration=500)

    # Add the padding chunk to beginning and end of the entire chunk.
    audio_chunk = silence_chunk + chunk + silence_chunk
        
    audio_chunk.export(
        './testSplittingOffPercussion/' + str(i) + '.wav',
        bitrate = "192k",
        format = "wav"
    )





