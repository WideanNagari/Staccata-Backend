import torch
import torch.nn as nn

class CustomSigmoid(nn.Module):
    def __init__(self, min_val, max_val):
        super(CustomSigmoid, self).__init__()
        self.min_val = min_val
        self.max_val = max_val

    def forward(self, x):
        scaled_sigmoid = torch.sigmoid(x) * (self.max_val - self.min_val) + self.min_val
        return scaled_sigmoid