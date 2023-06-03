import numpy as np
import scipy.signal as signal
import librosa

# low & high pass filter
def lh_pass_melspec(melspec, sr, cutoff_freq, filter='high'):
    # Convert mel-spectrogram to power spectrogram
    power_spec = librosa.feature.inverse.mel_to_stft(melspec)
    power_spec = np.abs(power_spec)**2
    
    # Calculate the filter coefficients using a Butterworth filter
    order = 5
    nyquist_freq = sr/2
    
    if(filter=='high'):
      b, a = signal.butter(order, cutoff_freq/nyquist_freq, btype='highpass', analog=False)
    else:
      b, a = signal.butter(order, cutoff_freq/nyquist_freq, btype='lowpass', analog=False)
    
    # Apply the filter to the power spectrogram using the difference equation
    filtered_power_spec = signal.filtfilt(b, a, power_spec, axis=0)
    
    # Convert the filtered power spectrogram back to mel-spectrogram
    filtered_melspec = librosa.feature.melspectrogram(S=filtered_power_spec, sr=sr, n_mels=melspec.shape[0])
    
    return filtered_melspec

def mel_to_wave(mel):
    S = librosa.feature.inverse.mel_to_stft(mel)
    y_inv = librosa.griffinlim(S)
    return y_inv