#!/usr/bin/python3.6
# based on the RL courses:
# 2015 Intro to RL: https://www.youtube.com/playlist?list=PLqYmG7hTraZDM-OYHWgPebj2MfCFzFObQ
# 2021 DeepMind x UCL RL Lecture Series  - https://www.youtube.com/watch?v=TCCjZe0y4Qc&list=PLqYmG7hTraZDVH599EItlEWsUOsJbAodm&ab_channel=DeepMind

import torch
import torch.nn as nn
import torch.nn.functional as F

# network input size: 7*6 = 42
# network output: 7
# based on: https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

model = nn.Sequential(
    nn.Linear(42, 100),
    nn.ReLU(),
    nn.Linear(100, 7),
    nn.SoftMax()
    )

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([],maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)