import librosa
import numpy as np

def normalize_audio(audio):
    return audio / np.max(np.abs(audio))

def mel_to_wave(mel):
    sr = 22050
    n_fft = 2048
    hop_length = 512
    n_iter = 128

    wave = librosa.feature.inverse.mel_to_audio(mel, sr=sr, n_fft=n_fft, hop_length=hop_length, n_iter=n_iter)
    wave = normalize_audio(wave.squeeze())

    return wave