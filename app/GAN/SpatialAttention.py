import torch
import torch.nn as nn

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv = nn.Conv2d(1, 1, kernel_size=kernel_size, padding=kernel_size // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        attention = torch.mean(x, dim=1, keepdim=True)  # Use only average pooling (1-channel input)
        attention = self.conv(attention)
        return x * self.sigmoid(attention)