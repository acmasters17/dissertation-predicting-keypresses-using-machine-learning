from glob import glob
import librosa
from librosa import feature
import numpy as np
import csv

fn_list_i = [
 feature.chroma_stft,
 feature.spectral_centroid,
 feature.spectral_bandwidth,
 feature.spectral_rolloff
]
 
fn_list_ii = [
 feature.rmse,
 feature.zero_crossing_rate
]
def get_feature_vector(y,sr): 
   feat_vect_i = [ np.mean(funct(y,sr)) for funct in fn_list_i]
   feat_vect_ii = [ np.mean(funct(y)) for funct in fn_list_ii] 
   feature_vector = feat_vect_i + feat_vect_ii 
   return feature_vector


#directories of normal audios
norm_data_dir = "./DatasetGenerator/SplitAudioFiles/"
norm_audio_files = glob(norm_data_dir + "*.wav")

# Extract audio features
norm_audios_feat = []
for file in norm_audio_files:
   y , sr = librosa.load(file,sr=None)
   feature_vector = get_feature_vector(y, sr)
   norm_audios_feat.append(feature_vector)

# Saving the file
norm_output = "normals_00.csv"
header =[
 "chroma_stft",
 "spectral_centroid",
 "spectral_bandwidth",
 "spectral_rolloff",
 "rmse",
 "zero_crossing_rate"
]
with open(norm_output,"+w") as f:
 csv_writer = csv.writer(f, delimiter = ",")
 csv_writer.writerow(header)
 csv_writer.writerows(norm_audios_feat)





