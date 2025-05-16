import librosa
import numpy as np

def mp3_to_mel(filepath):
    print("mp3 to np")
    y, sr = librosa.load(filepath, sr=22050)

    print("np to mel")    
    n_fft = 2048  # FFT window size
    hop_length = 512  # Hop length
    n_mels = 512  # Number of Mel bands
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    mel = librosa.power_to_db(mel, ref=np.max)

    return mel

def mel_to_mfcc(mel):
    mfcc = librosa.feature.mfcc(S=mel, n_mfcc=512)

    return mfcc