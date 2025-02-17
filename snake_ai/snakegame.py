import pygame
import random
import numpy as np
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
        self.running = True 
        return self.get_state()
 
    def spawn_food(self):
        while True:
            food = (random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE, 
                    random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE)
            if food not in self.snake:
                return food
        
    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * GRID_SIZE, head_y + self.direction[1] * GRID_SIZE)

        # Si choca con la pared o su cuerpo, termina el juego
        if new_head in self.snake:
            self.running = False
            return REWARD_HIT_SELF, True  # Penalización por chocar con su cuerpo
        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            self.running = False
            return REWARD_HIT_WALL, True  # Penalización por chocar contra la pared

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 10  
            return REWARD_EAT, False  # Mayor recompensa por comer
        else:
            food_x, food_y = self.food
            old_distance = abs(head_x - food_x) + abs(head_y - food_y)
            new_distance = abs(new_head[0] - food_x) + abs(new_head[1] - food_y)

            if new_distance > old_distance:
                reward = REWARD_MOVE_AWAY_FOOD  # Penalización por alejarse
            else:
                reward = REWARD_SAFE_MOVE  # Recompensa por moverse sin alejarse

            self.snake.pop()  # Evita crecimiento indebido
            return reward, False

    def step(self, action):
        self.direction = action
        reward, done = self.move_snake()
        return self.get_state(), reward, done
    
    def get_state(self):
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # Verifica si hay paredes cercanas
        danger_left = head_x - GRID_SIZE < 0
        danger_right = head_x + GRID_SIZE >= WIDTH
        danger_up = head_y - GRID_SIZE < 0
        danger_down = head_y + GRID_SIZE >= HEIGHT

        # Verifica si hay cuerpo de la serpiente en cada dirección
        body_left = (head_x - GRID_SIZE, head_y) in self.snake
        body_right = (head_x + GRID_SIZE, head_y) in self.snake
        body_up = (head_x, head_y - GRID_SIZE) in self.snake
        body_down = (head_x, head_y + GRID_SIZE) in self.snake
        
        return np.array([
            head_x < food_x, head_x > food_x, 
            head_y < food_y, head_y > food_y, 
            self.direction == UP, self.direction == DOWN, 
            self.direction == LEFT, self.direction == RIGHT,
            danger_left, danger_right, danger_up, danger_down,  # Paredes
            body_left, body_right, body_up, body_down  # Cuerpo de la serpiente
        ], dtype=int)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
    
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


