import pygame
import sys
import time
import math

# Window settings and FPS
WIDTH = 1280
HEIGHT = 1280
FPS = 60

# Define some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREY_REFERENCE = (111, 112, 115)  # Reference gray color for the road

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game with Image-based Tracks")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Car class definition
class Car:
    def __init__(self, x, y):
        # Load the car image (assuming car.png is in the same folder).
        # Use convert_alpha() if the image has transparency.
        car_image = pygame.image.load("pictures/car.png").convert_alpha()
        
        # Optionally, scale the image if it's too large or too small.
        # Example: car_image = pygame.transform.scale(car_image, (50, 100))

        # Keep the original image to handle rotation without losing quality.
        self.original_image = car_image
        self.image = self.original_image

        # Align the image so that its center is at (x, y).
        self.rect = self.image.get_rect(center=(x, y))

        # Position and movement parameters.
        self.pos = pygame.math.Vector2(x, y)
        self.angle = 0
        self.speed = 1  # Initial speed, adjust as needed.

    def update(self):
        # Move the car according to speed and angle.
        rad = math.radians(self.angle)
        self.pos.x += self.speed * math.cos(rad)
        self.pos.y -= self.speed * math.sin(rad)
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.speed += 0.001

    def rotate(self, direction):
        # Rotate the car: -1 for left, 1 for right
        self.angle += direction * 3  # Rotation speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

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

def countdown():
    counter = 3
    while counter > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BLACK)
        text = font.render(str(counter), True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)
        counter -= 1
    # Show "Go!"
    screen.fill(BLACK)
    text = font.render("Go!", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

def color_is_road(color):
    """
    Determines if a given pixel color is considered "on the road."
    We check if it's close to a reference grey. 
    Adjust the threshold as needed based on your track's actual colors.
    """
    threshold = 10
    r, g, b = color
    ref1_r, ref1_g, ref1_b = GREY_REFERENCE
    ref2_r, ref2_g, ref2_b = GREEN
    # Check if the color is roughly within the threshold range of grey
    
    if ((abs(r - ref1_r) < threshold and
        abs(g - ref1_g) < threshold and
        abs(b - ref1_b) < threshold) or
        (abs(r - ref2_r) < threshold and
        abs(g - ref2_g) < threshold and
        abs(b - ref2_b) < threshold)):
        return True
    
    # and include green also as part of the road.
    return False

def car_on_track(track_surface, car):
    """
    Returns True if the car is on the grey road area (approx), False otherwise.
    """
    x = int(car.pos.x)
    y = int(car.pos.y)
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return False

    color = track_surface.get_at((x, y))[:3]  # (R, G, B)
    print(x, y, color)
    return color_is_road(color)

def detect_lap(car, start_line_rect, lap_counted):
    if start_line_rect.collidepoint(car.pos.x, car.pos.y) and not lap_counted:
        return True
    return False

def main():
    state = "menu"
    track_surface = None
    start_line_rect = None
    car = None
    laps = 0
    score = 0
    lap_counted = False

    while True:
        if state == "menu":
            screen.fill(BLACK)
            title = font.render("Select a track:", True, WHITE)
            option1 = font.render("1 - Track 1 (Image)", True, WHITE)
            option2 = font.render("2 - Track 2 (Image)", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
            screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, HEIGHT // 3 + 40))
            screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, HEIGHT // 3 + 80))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        track_surface, start_line_rect = load_track1()
                        car = Car(1050, 175)
                        state = "countdown"
                    elif event.key == pygame.K_2:
                        track_surface, start_line_rect = load_track2()
                        car = Car(WIDTH // 2, HEIGHT - 80)
                        state = "countdown"

        elif state == "countdown":
            # Display start message: "Press Enter to start"
            waiting = True
            while waiting:
                screen.fill(BLACK)
                message = font.render("Press Enter to start", True, WHITE)
                screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False
            countdown()
            state = "playing"

        elif state == "playing":
            screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle left and right arrow key inputs for steering
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                car.rotate(1)
            if keys[pygame.K_RIGHT]:
                car.rotate(-1)

            car.update()

            # Check if the car is on the road (grey area)
            if not car_on_track(track_surface, car):
                state = "game_over"

            # Detect crossing the start line to count a lap
            if detect_lap(car, start_line_rect, lap_counted):
                laps += 1
                score += 100 * laps
                lap_counted = True
            # Once the car is no longer on the start line rect, we allow the next lap to be counted
            if not start_line_rect.collidepoint(car.pos.x, car.pos.y):
                lap_counted = False

            # Draw the track and the car
            screen.blit(track_surface, (0, 0))
            car.draw(screen)
            info = font.render(f"Laps: {laps}  Score: {score}", True, WHITE)
            screen.blit(info, (WIDTH - info.get_width() - 20, 20))
            pygame.display.flip()
            clock.tick(FPS)

        elif state == "game_over":
            screen.fill(BLACK)
            msg = font.render("Game Over!", True, RED)
            msg2 = font.render(f"Laps: {laps}  Score: {score}", True, WHITE)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + msg2.get_height()))
            pygame.display.flip()
            time.sleep(3)
            state = "menu"
            laps = 0
            score = 0
            car = None

        # Placeholder for integrating Machine Learning in the future.
        # For example, this could be used to adjust the difficulty or train an agent to drive.
        # def apply_ml():
        #     # ML code to analyze game data and adjust parameters goes here
        #     pass
        # apply_ml()

if __name__ == "__main__":
    main()
