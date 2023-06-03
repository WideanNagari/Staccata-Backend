import librosa
import numpy as np

def matrix_to_vector(data):
    vector = []
    mat = data.transpose()
    for i in mat:
        vector.append(i)

    vector = np.array(vector)
    vector = np.asarray(vector).astype(np.float32)
    return vector

def mp3_to_mel(filepath):
    print("mp3 to np")
    y, sr = librosa.load(filepath)
    print("np to mel")
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    return mel