import os
import torch
import librosa
from app.GAN.Generator import Generator

def load_model(model_type, input_type):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'GAN', model_type + '_' + input_type +'.pth')
    
    if (input_type == 'mel'):
        model = Generator(-80, 0)
    elif (input_type == 'mfcc'):
        model = Generator(-1808.6875, 492.521)

    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model

model_p2g_mel = load_model("p2g","mel")
model_p2g_mfcc = load_model("p2g","mfcc")
model_g2p_mel = load_model("g2p","mel")
model_g2p_mfcc = load_model("g2p","mfcc")

def predict(data, jenis):
    print("predicting")

    inputType = 'mel-spectrogram'
    if (jenis == "p2g_mel-spectrogram"):
        model = model_p2g_mel
    elif (jenis == "p2g_mfcc"):
        model = model_p2g_mfcc
        inputType = 'mfcc'
    elif (jenis == "g2p_mel-spectrogram"):
        model = model_g2p_mel
    elif (jenis == "g2p_mfcc"):
        model = model_g2p_mfcc
        inputType = 'mfcc'

    with torch.no_grad():
        data = torch.tensor(data[:, :258], dtype=torch.float32).unsqueeze(0).unsqueeze(0)
        _ , prediction = model(data)
        prediction = prediction.detach().cpu().numpy()

        if (inputType == 'mel-spectrogram'):
            prediction = librosa.db_to_power(prediction, ref=10.0)
        elif (inputType == 'mfcc'):
            prediction = librosa.feature.inverse.mfcc_to_mel(prediction, ref=10.0, n_mels=512)

    return prediction