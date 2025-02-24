import random
from utils import QLearningAlgroithm

class QLearningAgent:
    def __init__(self, config):
        self.q_table = {}
        self.alpha = config["ALPHA"]
        self.gamma = config["GAMMA"]
        self.epsilon = config["EPSILON"]
        self.epsilon_decay = config["EPSILON_DECAY"]
        self.epsilon_min = config["EPSILON_MIN"]
        self.action_space = config["ACTIONS"]

    def choose_action(self, state):
        # Exploration: Choose a random action with probability epsilon
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.action_space)  
        else:
            # Exploitation: Choose the best action based on the Q-table
            q_values = {a: self.q_table.get((tuple(state), tuple(a)), 0.0) for a in self.action_space}
            best_action = max(q_values, key=q_values.get)
            return best_action
        
    def update_q(self, state, action, reward, next_state):
        best_next_q = max([self.q_table.get((tuple(next_state), tuple(a)), 0.0) for a in self.action_space])
        current_q = self.q_table.get((tuple(state), tuple(action)), 0.0)

        # Q-Learning update rule
        self.q_table[(tuple(state), tuple(action))] = QLearningAlgroithm(self.alpha, self.gamma, reward, current_q, best_next_q)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
