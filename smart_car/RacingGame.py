import pygame
import sys
import time
import math
import numpy as np
from configuration import *

class Car:
    def __init__(self, x, y):
        car_image = pygame.image.load("pictures/car.png").convert_alpha()
        self.original_image = car_image
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.speed = 1
        self.direction = RIGHT

    def update(self):
        rad = math.radians(self.angle)
        self.pos.x += self.speed * math.cos(rad)
        self.pos.y -= self.speed * math.sin(rad)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.speed += 0.001

    def rotate(self, direction):
        self.angle += direction * 3
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class RacingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Racing Game with Image-based Tracks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.state = "playing"
        self.track_surface = None
        self.start_line_rect = None
        self.car = Car(960, 135)
        self.laps = 0
        self.score = 0
        self.lap_counted = False

    def load_track1(self):
        track = pygame.image.load("pictures/track1.png").convert_alpha()
        track = pygame.transform.scale(track, (WIDTH, HEIGHT))
        start_line_rect = pygame.Rect(960, 135, 5, 105)
        pygame.draw.rect(track, GREEN, start_line_rect)
        return track, start_line_rect

    def load_track2(self):
        track = pygame.image.load("pictures/track2.png").convert()
        track = pygame.transform.scale(track, (WIDTH, HEIGHT))
        start_line_rect = pygame.Rect(380, 50, 40, 5)
        return track, start_line_rect

    def countdown(self):
        counter = 3
        while counter > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill(BLACK)
            text = self.font.render(str(counter), True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            time.sleep(1)
            counter -= 1
        self.screen.fill(BLACK)
        text = self.font.render("Go!", True, WHITE)
        self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

    def color_is_road(self, color):
        threshold = 10
        r, g, b = color
        ref1_r, ref1_g, ref1_b = GREY_REFERENCE
        ref2_r, ref2_g, ref2_b = GREEN
        if ((abs(r - ref1_r) < threshold and
             abs(g - ref1_g) < threshold and
             abs(b - ref1_b) < threshold) or
            (abs(r - ref2_r) < threshold and
             abs(g - ref2_g) < threshold and
             abs(b - ref2_b) < threshold)):
            return True
        return False

    def car_on_track(self, car):
        x = int(car.pos.x)
        y = int(car.pos.y)
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False
        color = self.track_surface.get_at((x, y))[:3]
        return self.color_is_road(color)

    def detect_lap(self, car):
        if self.start_line_rect.collidepoint(car.pos.x, car.pos.y) and not self.lap_counted:
            return True
        return False

    def reset(self):
        self.track_surface, self.start_line_rect = load_track1()
        self.state = "playing"
        self.car = Car(960, 155)
        self.laps = 0
        self.score = 0
        self.lap_counted = False
        self.direction = RIGHT
        return self.get_state()
    
    def get_state(self):
        return np.array([self.car.pos.x, self.car.pos.y, self
                          .car.angle, self.car.speed, self.laps, self
                          .score], dtype=np.float32)
    
    def start_game(self, track_choice):
        if track_choice == 1:
            self.track_surface, self.start_line_rect = load_track1()
            self.car = Car(1050, 175)
        elif track_choice == 2:
            self.track_surface, self.start_line_rect = load_track2()
            self.car = Car(WIDTH // 2, HEIGHT - 80)
        self.state = "countdown"

    def run(self):
        while True:
            if self.state == "playing":
                self.screen.fill(BLACK)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.car.rotate(1)
                if keys[pygame.K_RIGHT]:
                    self.car.rotate(-1)

                self.car.update()

                if not self.car_on_track(self.car):
                    self.state = "game_over"

                if self.detect_lap(self.car):
                    self.laps += 1
                    self.score += 100 * self.laps
                    self.lap_counted = True
                if not self.start_line_rect.collidepoint(self.car.pos.x, self.car.pos.y):
                    self.lap_counted = False

                self.screen.blit(self.track_surface, (0, 0))
                self.car.draw(self.screen)
                info = self.font.render(f"Laps: {self.laps}  Score: {self.score}", True, WHITE)
                self.screen.blit(info, (WIDTH - info.get_width() - 20, 20))
                pygame.display.flip()
                self.clock.tick(FPS)

            elif self.state == "game_over":
                self.screen.fill(BLACK)
                msg = self.font.render("Game Over!", True, RED)
                msg2 = self.font.render(f"Laps: {self.laps}  Score: {self.score}", True, WHITE)
                self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
                self.screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + msg2.get_height()))
                pygame.display.flip()
                time.sleep(3)
                self.reset()
                
def load_track1():
    """
    Loads the first track image and returns:
    1) The track surface
    2) A start line rectangle for lap detection
    """
    track = pygame.image.load("pictures/track1.png").convert_alpha()
    # Optionally resize the image to match WIDTH, HEIGHT if needed:
    track = pygame.transform.scale(track, (WIDTH, HEIGHT))
    # Define a start line rectangle. You can adjust these values
    # depending on where you want the start line in the image.
    # For example, near the top-left or any other region of the track.
    start_line_rect = pygame.Rect(960, 135, 5, 105)  # Example position
    # Set the rectangle color to white for better visibility
    pygame.draw.rect(track, GREEN, start_line_rect)
    return track, start_line_rect

def load_track2():
    """
    Loads the second track image and returns:
    1) The track surface
    2) A start line rectangle for lap detection
    """
    track = pygame.image.load("pictures/track2.png").convert()
    track = pygame.transform.scale(track, (WIDTH, HEIGHT))
    # Define a start line rectangle in a suitable position
    start_line_rect = pygame.Rect(380, 50, 40, 5)  # Example position
    return track, start_line_rect