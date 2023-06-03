import os
import torch
from torch.autograd import Variable
from app.GAN.Generator import Generator

def load_model(model_name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'GAN', model_name+'.pth')
    model = Generator()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model

model_p2g = load_model("model_p2g")
model_g2p = load_model("model_g2p")

def predict(data, jenis):
    print("predicting")
    prediction = []
    model = model_p2g

    if (jenis=="g2p"):
        model = model_g2p
    
    with torch.no_grad():
        for i in range(len(data)):
            xt = Variable(torch.from_numpy(data[i]).type(torch.float32)).unsqueeze(0)
            y_hat = model(xt).squeeze(0)
            prediction.append(y_hat.numpy())
    return prediction