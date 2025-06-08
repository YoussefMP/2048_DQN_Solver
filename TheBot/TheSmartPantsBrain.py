import torch
import torch.nn as nn
import torch.nn.functional as F


class QNetwork(nn.Module):
    def __init__(self, input_dim=16, hidden_dim=128, output_dim=4):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = x.float()  # ensure tensor is float
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.out(x)


if __name__ == "__main__":
    net = QNetwork()
    dummy_board = torch.rand((1, 16))
    q_values = net(dummy_board)
    print("Q-values:", q_values)

