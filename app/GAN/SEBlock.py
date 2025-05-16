import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.utils as utils

class SEBlock(nn.Module):
    def __init__(self, channels, reduction=16):
        super(SEBlock, self).__init__()
        self.fc1 = utils.spectral_norm(nn.Linear(channels, channels // reduction, bias=False))
        self.fc2 = utils.spectral_norm(nn.Linear(channels // reduction, channels // reduction, bias=False))
        self.fc3 = utils.spectral_norm(nn.Linear(channels // reduction, channels // reduction, bias=False))
        self.fc4 = utils.spectral_norm(nn.Linear(channels // reduction, channels, bias=False))

    def forward(self, x):
        batch, channels, _ , _ = x.size()
        y = torch.mean(x, dim=(2, 3))
        y = F.relu(self.fc1(y))
        y = F.relu(self.fc2(y))
        y = F.relu(self.fc3(y))
        y = torch.sigmoid(self.fc4(y))
        y = y.view(batch, channels, 1, 1)
        return x * y