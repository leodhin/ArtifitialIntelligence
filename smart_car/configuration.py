# Game configuration
WIDTH = 1280
HEIGHT = 1280
FPS = 60

# Define some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREY_REFERENCE = (111, 112, 115)  # Reference gray color for the road

# Car configuration
MAX_SPEED = 10

# Dirección del movimiento
LEFT, RIGHT = (-1, 0), (1, 0)
ACTIONS = [LEFT, RIGHT]

# Parámetros de aprendizaje
ALPHA = 0.1  # Tasa de aprendizaje
GAMMA = 0.9  # Descuento de recompensa futura
EPSILON = 1.0  # Probabilidad de exploración inicial
EPSILON_DECAY = 0.995  # Factor de reducción de exploración
EPSILON_MIN = 0.01  # Valor mínimo de epsilon
NUM_EPISODES = 500 # Número de episodios de entrenamiento

# Recompensas
CROSS_LINE = 500  # Recompensa por comer
REWARD_HIT_WALL = -100  # Penalización por chocar contra la pared