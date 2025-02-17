# Configuración del juego
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
WHITE, GREEN, RED, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)

# Dirección del movimiento
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
ACTIONS = [UP, DOWN, LEFT, RIGHT]

# Parámetros de aprendizaje
ALPHA = 0.1  # Tasa de aprendizaje
GAMMA = 0.9  # Descuento de recompensa futura
EPSILON = 1.0  # Probabilidad de exploración inicial
EPSILON_DECAY = 0.995  # Factor de reducción de exploración
EPSILON_MIN = 0.01  # Valor mínimo de epsilon
NUM_EPISODES = 50000 # Número de episodios de entrenamiento

# Recompensas
REWARD_EAT = 40  # Recompensa por comer
REWARD_MOVE_TOWARDS_FOOD = 5  # Recompensa por acercarse a la comida
REWARD_MOVE_AWAY_FOOD = -1  # Penalización por alejarse de la comida
REWARD_HIT_WALL = -100  # Penalización por chocar contra la pared
REWARD_HIT_SELF = -100  # Penalización por chocar contra sí mismo
REWARD_SAFE_MOVE = 1  # Recompensa por moverse sin alejarse de la comida
REWARD_DANGER_ZONE = -1  # Penalización por moverse a una zona peligrosa
REWARD_TRAPPED = 0  # Penalización fuerte por reducir demasiado el espacio disponible

