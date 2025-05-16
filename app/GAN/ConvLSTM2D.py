import torch
import torch.nn as nn

class ConvLSTM2D(nn.Module):
    def __init__(self, input_channels, hidden_channels, kernel_size):
        super(ConvLSTM2D, self).__init__()
        self.hidden_channels = hidden_channels
        padding = kernel_size // 2

        # Forward ConvLSTM layer
        self.forward_conv = nn.Conv2d(input_channels + hidden_channels, 4 * hidden_channels, kernel_size, padding=padding)
        self.backward_conv = nn.Conv2d(input_channels + hidden_channels, 4 * hidden_channels, kernel_size, padding=padding)

    def forward_lstm(self, input_tensor, hidden_state, conv_layer):
        h_cur, c_cur = hidden_state
        combined = torch.cat([input_tensor, h_cur], dim=1)  # Concatenate along channel dimension
        combined_conv = conv_layer(combined)

        i, f, o, g = torch.split(combined_conv, self.hidden_channels, dim=1)
        i = torch.sigmoid(i)
        f = torch.sigmoid(f)
        o = torch.sigmoid(o)
        g = torch.tanh(g)

        c_next = f * c_cur + i * g
        h_next = o * torch.tanh(c_next)

        return h_next, (h_next, c_next)

    def forward(self, input_tensor, hidden_state):
        h_cur, c_cur = hidden_state

        # Forward pass
        h_next_f, (h_f, c_f) = self.forward_lstm(input_tensor, (h_cur, c_cur), self.forward_conv)

        # Reverse the input tensor for backward processing
        reversed_input = torch.flip(input_tensor, dims=[-1])
        h_next_b, (h_b, c_b) = self.forward_lstm(reversed_input, (h_cur, c_cur), self.backward_conv)
        h_next_b = torch.flip(h_next_b, dims=[-1])

        # Combine forward and backward outputs
        h_next = torch.cat([h_next_f, h_next_b], dim=1)
        c_next = torch.cat([c_f, c_b], dim=1)

        return h_next, (h_next, c_next)