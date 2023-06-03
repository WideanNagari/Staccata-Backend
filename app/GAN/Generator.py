import torch
import torch.nn as nn
from app.GAN.Attention import Attention

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.lstm1 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.lstm2 = nn.LSTM(128, 64, bidirectional=True, batch_first=True)
        self.attention_layer = Attention(1, 128)
        self.fc1 = nn.Linear(64 * 2, 512)
        self.fc2 = nn.Linear(512, 128)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = torch.unsqueeze(x, 1)
        x = self.attention_layer(x)
        x, _ = self.lstm2(x)
        x = self.fc1(x)
        x = self.fc2(x)
        return x