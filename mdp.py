# implementing Markov Decision Proccess
# Value and Policy iteration

from dataclasses import dataclass

# An MDP is a 5-tuple defined over
# set of states
# set of actions
# rewards 
# discount factor
# transition process -> in our case will be deterministic

import numpy as np
import matplotlib.pyplot as plt
gamma = 0.9 # discount factor

width = 4
height = 3

states = [(i,j) for i in range(height) for j in range(width)] # indexes in a matrix
actions = ['U', 'D', 'L', 'R'] # up, down, left, right
rewards = {
	(2,2): -1,
	(2,3): 1,
	(1,2): -1
}
for s in states:
	if s not in rewards:
		rewards[s] = 0

def next_state(state, action):
	if action == 'U':
		nxt = (state[0] - 1, state[1])
	if action == 'D':
		nxt = (state[0] + 1, state[1])
	if action == 'L':
		nxt = (state[0], state[1] - 1)
	if action == 'R':
		nxt = (state[0], state[1] + 1)

	nxt0 = min(max(nxt[0], 0), height-1)
	nxt1 = min(max(nxt[1], 0), width-1)
	nxt = (nxt0, nxt1)
	return nxt

@dataclass
class MDP:
	states: list
	actions: list
	rewards: dict
	gamma: float
	next_state: None

class MDP_solver:
	def __init__(self, mdp: MDP):
		self.mdp = mdp

		self.policy = {}
		self.values = self.mdp.rewards.copy()
		for s in mdp.states:
			if mdp.rewards[s] != 0:
				self.policy[s] = 'X'
			else:
				self.policy[s] = np.random.choice(mdp.actions)
		# self.values[s] = 0

	def value_iteration(self, max_iter = 100, thresh = 0.005):
		for i in range(max_iter):
			if i in [2 ** j for j in range(30)]:
				print(f"ITER {i} {diff}")

			diff = 0
			for s in self.mdp.states:
				if self.mdp.rewards[s] != 0: continue

				new_v = 0
				old_v = self.values[s]

				for a in self.mdp.actions:
					nxt = next_state(s, a)
					if nxt == s: continue

					v = self.mdp.rewards[s] + self.mdp.gamma * self.values[nxt]
					if v > new_v:
						new_v = v
						self.policy[s] = a

				diff = float(max(diff, np.abs(new_v - old_v)))
				self.values[s] = new_v

			if diff < thresh:
				print(f"Done after {i} iters: {diff:.3}")
				break

m = MDP(states, actions, rewards, gamma, next_state)
s = MDP_solver(m)
s.value_iteration(100)
print(s.policy)

# plot
board = np.zeros((height, width))
for i in s.values:
	board[i[0], i[1]] = s.values[i]
plt.matshow(board)
ax = plt.gca()
ax.set_xticks(np.arange(-.5, width, 1))
ax.set_yticks(np.arange(-.5, height, 1))
ax.set_xticklabels(np.arange(0, width + 1, 1))
ax.set_yticklabels(np.arange(0, height + 1, 1))
ax.grid(color='white', linestyle='-.', linewidth=1)
for i in s.values:
	ax.text(i[1], i[0], f"{float(s.values[i]):.3}", ha="center", va="center", color='white')
for i in s.policy:
	ax.text(i[1], i[0], f"\n\n\n{s.policy[i]}", ha="center", va="center", color='white')

plt.colorbar()	
plt.show()
