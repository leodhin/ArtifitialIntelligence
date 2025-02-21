import pygame
import random
import numpy as np
from collections import deque
from configuration import *
from qlearning_agent import *

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset()
    
    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.spawn_food()
        self.score = 0
        self.trap_deaths = 0
        self.wall_deaths = 0
        self.self_deaths = 0
        self.running = True 
        return self.get_state()
 
    def spawn_food(self):
        while True:
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE, 
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if food not in self.snake:
                return food
        
    def risk_score(self, pos):
        """
        Calcula un score simple contando cuántos vecinos (4 direcciones) están ocupados
        por el cuerpo de la serpiente.
        """
        score = 0
        for dx, dy in [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]:
            neighbor = (pos[0] + dx, pos[1] + dy)
            if neighbor in self.snake:
                score += 1
        return score

    def calculate_free_area(self, start, max_iterations=200):
        """
        Realiza una búsqueda en anchura (BFS) a partir de 'start', pero limita la cantidad
        de iteraciones para ahorrar tiempo. Devuelve el número de celdas libres alcanzadas.
        """
        visited = set()
        queue = deque([start])
        free_count = 0
        iterations = 0
        while queue and iterations < max_iterations:
            pos = queue.popleft()
            iterations += 1
            if pos in visited:
                continue
            visited.add(pos)
            free_count += 1
            for dx, dy in [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                new_pos = (nx, ny)
                if not (0 <= nx < WIDTH and 0 <= ny < HEIGHT):
                    continue
                # Se permite la cola, ya que se libera en el siguiente tick
                if new_pos in self.snake and new_pos != self.snake[-1]:
                    continue
                if new_pos not in visited:
                    queue.append(new_pos)
        return free_count

    def is_trapped(self):
        """
        Considera que la serpiente está atrapada si el área libre accesible desde la cabeza,
        evaluada con un BFS limitado, es menor que un umbral relativo (mínimo 50 o 2 veces la longitud).
        """
        threshold = max(50, len(self.snake) * 2)
        free_area = self.calculate_free_area(self.snake[0], max_iterations=200)
        return free_area < threshold

    def _is_adjacent_to_body(self, pos):
        """
        Comprueba si la posición dada (usualmente la nueva cabeza) está adyacente a alguna
        parte del cuerpo (excluyendo la cabeza y, opcionalmente, la cola).
        """
        x, y = pos
        for dx, dy in [(GRID_SIZE, 0), (-GRID_SIZE, 0), (0, GRID_SIZE), (0, -GRID_SIZE)]:
            neighbor = (x + dx, y + dy)
            # Se ignora la cabeza y se asume que la cola se libera en el siguiente movimiento
            if neighbor in self.snake[1:-1]:
                return True
        return False

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)
        reward = 0

        # Verificar colisión con el cuerpo o la pared
        if new_head in self.snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            self.running = False
            if new_head in self.snake:
                reward += REWARD_HIT_SELF
                self.self_deaths += 1
                # Si la nueva cabeza está adyacente al cuerpo, evaluar atrapamiento
                if len(self.snake) > 1 and self._is_adjacent_to_body(new_head):
                    if self.is_trapped():
                        self.trap_deaths += 1
                        reward += REWARD_TRAPPED
            else:
                reward += REWARD_HIT_WALL
                self.wall_deaths += 1
            return reward, True

        # Inserta la nueva cabeza
        self.snake.insert(0, new_head)
    
        # Si el score de riesgo es alto, evaluamos el área libre
        if self.risk_score(new_head) >= 2:
            free_area = self.calculate_free_area(new_head, max_iterations=200)
            threshold = max(50, len(self.snake) * 2)
            if free_area < threshold:
                # Penalización proporcional a la diferencia
                reward += REWARD_UNSAFE_ACTION * (threshold - free_area)

        # Evaluar atrapamiento en zonas críticas (adyacente al cuerpo)
        if self._is_adjacent_to_body(new_head) and self.is_trapped():
            reward += REWARD_TRAPPED
            self.trap_deaths += 1
            self.running = False
            return reward, True

        # Calcular la distancia a la comida
        food_x, food_y = self.food
        old_distance = abs(head_x - food_x) + abs(head_y - food_y)
        new_distance = abs(new_head[0] - food_x) + abs(new_head[1] - food_y)

        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 10  
            reward += REWARD_EAT
        else:
            if new_distance > old_distance:
                reward += REWARD_MOVE_AWAY_FOOD
            else:
                reward += REWARD_MOVE_TOWARDS_FOOD / max(1, new_distance)
            self.snake.pop()  # Eliminar la cola si no come
            
        return reward, False

    def step(self, action):
        self.direction = action
        reward, done = self.move_snake()
        return self.get_state(), reward, done
    
    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # Determinar peligros respecto a la cabeza
        danger_left = head_x - GRID_SIZE < 0
        danger_right = head_x + GRID_SIZE >= WIDTH
        danger_up = head_y - GRID_SIZE < 0
        danger_down = head_y + GRID_SIZE >= HEIGHT

        # Comprobar si hay cuerpo en las celdas adyacentes
        body_left = (head_x - GRID_SIZE, head_y) in self.snake
        body_right = (head_x + GRID_SIZE, head_y) in self.snake
        body_up = (head_x, head_y - GRID_SIZE) in self.snake
        body_down = (head_x, head_y + GRID_SIZE) in self.snake
        
        return np.array([
            head_x < food_x, head_x > food_x, 
            head_y < food_y, head_y > food_y, 
            self.direction == UP, self.direction == DOWN, 
            self.direction == LEFT, self.direction == RIGHT,
            danger_left, danger_right, danger_up, danger_down,
            body_left, body_right, body_up, body_down
        ], dtype=int)
    
    def get_safe_actions(self):
        safe = []
        head_x, head_y = self.snake[0]
        for action in ACTIONS:
            new_head = (head_x + action[0] * GRID_SIZE, head_y + action[1] * GRID_SIZE)
            if new_head not in self.snake and (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
                safe.append(action)
        return safe
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
                break  # Se procesa solo un evento por tick
    
    def draw(self):
        self.screen.fill(BLACK)
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, (*segment, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(self.screen, RED, (*self.food, GRID_SIZE, GRID_SIZE))
        self.draw_score()
        pygame.display.update()
        pygame.event.pump()

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (WIDTH - 120, 10))
