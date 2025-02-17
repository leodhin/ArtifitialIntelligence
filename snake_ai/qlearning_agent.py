import random
from configuration import *

class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.epsilon = EPSILON
        self.epsilon_decay = EPSILON_DECAY
        self.epsilon_min = EPSILON_MIN

    def get_q(self, state, action):
        return self.q_table.get((tuple(state), tuple(action)), 0.0)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(ACTIONS)  # Exploración
        else:
            q_values = {a: self.q_table.get((tuple(state), tuple(a)), 0.0) for a in ACTIONS}
            return max(q_values, key=q_values.get)  # Explota la mejor acción aprendida

    def update_q(self, state, action, reward, next_state):
        best_next_q = max([self.q_table.get((tuple(next_state), tuple(a)), 0.0) for a in ACTIONS])
        current_q = self.q_table.get((tuple(state), tuple(action)), 0.0)

        getting_closer = (state[0] and not next_state[1]) or (state[1] and not next_state[0]) or \
                         (state[2] and not next_state[3]) or (state[3] and not next_state[2])

        moving_away = (state[1] and not next_state[0]) or (state[0] and not next_state[1]) or \
                      (state[3] and not next_state[2]) or (state[2] and not next_state[3])

        if getting_closer:
            reward += REWARD_MOVE_TOWARDS_FOOD
        if moving_away:
            reward += REWARD_MOVE_AWAY_FOOD

        # Penalización leve por moverse a zonas peligrosas
        danger_zones = {
            LEFT: state[8] or state[12],
            RIGHT: state[9] or state[13],
            UP: state[10] or state[14],
            DOWN: state[11] or state[15]
        }
        if danger_zones.get(tuple(action), False):
            reward += REWARD_DANGER_ZONE

        # Actualización de la tabla Q
        self.q_table[(tuple(state), tuple(action))] = (1 - self.alpha) * current_q + \
            self.alpha * (reward + self.gamma * best_next_q)

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
