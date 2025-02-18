def QLearningAlgroithm(alpha, gamma, reward, current_value, optimal_future_value):
    return (1 - alpha) * current_value + \
            alpha * (reward + gamma * optimal_future_value)
