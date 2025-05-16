import torch
import torch.nn as nn
import torch.nn.utils as utils
from app.GAN.CustomSigmoid import CustomSigmoid
from app.GAN.ResidualBlock import ResidualBlock
from app.GAN.SEBlock import SEBlock
from app.GAN.ChannelAttention import ChannelAttention
from app.GAN.SpatialAttention import SpatialAttention
from app.GAN.ConvLSTM2D import ConvLSTM2D

class Generator(nn.Module):
    def __init__(self, min_val, max_val):
        super(Generator, self).__init__()

        # Encoder
        self.encoder = nn.Sequential(
            utils.spectral_norm(nn.Conv2d(1, 16, kernel_size=3, stride=2, padding=1)),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            ResidualBlock(16),
            SEBlock(16),
            utils.spectral_norm(nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1)),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            ResidualBlock(32),
            SEBlock(32),
            ChannelAttention(32),  # CBAM Channel Attention
            SpatialAttention(),
            utils.spectral_norm(nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1)),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            ResidualBlock(64),
            SEBlock(64),
        )

        # ConvLSTM block (bidirectional enabled)
        self.convlstm = ConvLSTM2D(64, 64, kernel_size=3)

        # Decoder
        self.decoder = nn.Sequential(
            utils.spectral_norm(nn.ConvTranspose2d(128, 32, kernel_size=3, stride=2, padding=1, output_padding=(1, 0))),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            ResidualBlock(32),
            SEBlock(32),
            utils.spectral_norm(nn.ConvTranspose2d(32, 16, kernel_size=3, stride=2, padding=1, output_padding=(1, 0))),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            ResidualBlock(16),
            SEBlock(16),
            utils.spectral_norm(nn.ConvTranspose2d(16, 1, kernel_size=3, stride=2, padding=1, output_padding=(1, 1))),
            # CustomSigmoid(-80, 0),  # Custom activation (if needed)
            CustomSigmoid(min_val, max_val),
        )

    def forward(self, x):
        # Encode
        latent = self.encoder(x)

        # Initialize hidden states for ConvLSTM
        batch_size, _, height, width = latent.size()
        h_0 = torch.zeros(batch_size, 64, height, width, device=latent.device)
        c_0 = torch.zeros(batch_size, 64, height, width, device=latent.device)

        # Pass through ConvLSTM
        latent, _ = self.convlstm(latent, (h_0, c_0))

        # Decode
        output = self.decoder(latent)
        return latent, output