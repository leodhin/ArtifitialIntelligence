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

    def choose_action(self, state, current_direction):
        if random.uniform(0, 1) < self.epsilon:
            # Definir las acciones válidas excluyendo la dirección opuesta
            valid_actions = [action for action in ACTIONS if action != (-current_direction[0], -current_direction[1])]
            return random.choice(valid_actions)  # Exploración con restricción
        else:
            # Explotación: Elegir la mejor acción basada en la tabla Q
            q_values = {a: self.q_table.get((tuple(state), tuple(a)), 0.0) for a in ACTIONS}
            best_action = max(q_values, key=q_values.get)

            # Asegurar que la mejor acción no sea la dirección contraria
            if best_action == (-current_direction[0], -current_direction[1]):
                valid_actions = [action for action in ACTIONS if action != best_action]
                return random.choice(valid_actions)  # Escoge otra acción válida

        return best_action
        
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

        # Reforzar la penalización si la serpiente ya estaba atrapada en el estado anterior**
        if state[8] and state[9] and state[10] and state[11]:  # Si hay paredes en todas direcciones
                reward += REWARD_TRAPPED

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
