import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

from TheSmartPantsBrain import QNetwork
from utils.replay_buffer import ReplayBuffer


class DQNAgent:
    def __init__(self, state_dim=16, action_dim=4, hidden_dim=128, lr=1e-3, gamma=0.99, epsilon=1.0,
                 epsilon_decay=0.995, min_epsilon=0.1):
        self.q_net = QNetwork(state_dim, hidden_dim, action_dim)
        self.target_net = QNetwork(state_dim, hidden_dim, action_dim)
        self.target_net.load_state_dict(self.q_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.ADamW(self.q_net.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

        self.replay_buffer = ReplayBuffer()
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.action_dim = action_dim

    def make_move(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_dim-1)
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            q_values = self.q_net(state_tensor)
        return int(torch.argmax(q_values).item())

    def update(self, batch_size):
        if len(self.replay_buffer) < batch_size:
            return

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(batch_size)

        states = torch.tensor(states)
        actions = torch.tensor(actions)
        rewards = torch.tensor(rewards)
        next_states = torch.tensor(next_states)
        dones = torch.tensor(dones)

        q_values = self.q_net(states).gather(1, actions)

        with torch.no_grad():
            max_next_q = self.target_net(next_states).max(1, keepdim=True)[0]
            target_q = rewards + (1-dones) * self.gamma * max_next_q

        loss = self.loss_fn(q_values, target_q)

        self.optimizer.zero_grad()
        loss.backwards()
        self.optimizer.step()

        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def sync_target(self):
        self.target_net.load_state_dict(self.q_net.state_dict())