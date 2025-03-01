import pickle
import os
import pygame
import sys
import time
import math
from qlearning_agent import *
from configuration import *
from RacingGame import RacingGame

def calculate_reward(game, state, action):
    car_posX = state[0]
    car_posY = state[1]
    car_angle = state[2]
    car_speed = state[3]
    
    print("state", state)
    new_pos = (car_posX + car_speed * action[0], car_posY + car_speed * action[1])
    new_angle = car_angle + action[0]
    new_speed = car_speed + action[1]

    if new_speed < 0:
        new_speed = 0

    if new_speed > MAX_SPEED:
        new_speed = MAX_SPEED

    if new_angle < 0:
        new_angle += 360
    if new_angle >= 360:
        new_angle -= 360

    new_state = (new_pos, new_angle, new_speed)

    if not game.car_on_track(game.car):
        reward = -100
        done = True
    elif game.detect_lap(game.car):
        reward = 100
        done = False
    else:
        reward = 1
        done = False
    
    return reward, new_state, done

def train_ai(game, agent):
    num_episodes = NUM_EPISODES
    actual_episode = 0
    total_score = 0
    average_score = 0
    best_score = 0

    check_interval = 1000
    last_improvement_episode = 0
    last_average_score = 0

    if os.path.exists("q_table.pkl"):
        with open("q_table.pkl", "rb") as f:
            agent.q_table = pickle.load(f)
        print(f"Tabla Q cargada. Estadfos aprendidos: {len(agent.q_table)}")
        agent.epsilon = EPSILON_MIN

    while actual_episode < num_episodes:
        Finished = False
        state = game.reset()
        while not Finished:
            action = agent.choose_action(state)
            print("action", game.car.direction)
            if action == (-game.car.direction[0], -game.car.direction[1]):
                action = random.choice([a for a in ACTIONS if a != (-game.car.direction[0], -game.car.direction[1])])
            reward, done = calculate_reward(game, state, action)
            next_state, reward, done = game.step(action)
            # Update the Q-table
            agent.update_q(state, action, reward, new_state)
            
            print("new_state", new_state)
            Finished = done

        total_score += game.score
        best_score = max(best_score, game.score)
        print(f"\rEpisodio {actual_episode + 1}/{num_episodes} - Mejor Score: {best_score} - Promedio Score: {average_score:.2f}", end='', flush=True)
        actual_episode += 1
        average_score = total_score / (actual_episode + 1)
        agent.decay_epsilon()

        if (actual_episode - last_improvement_episode) >= check_interval:
            if average_score - last_average_score < 1:
                print("\nEl promedio de score no ha aumentado en 1 unidad en los últimos 1000 episodios. Deteniendo el entrenamiento.")
                break
            else:
                last_average_score = average_score
                last_improvement_episode = actual_episode

    with open("q_table.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)

    print("\nEntrenamiento completado y guardado.")

    with open("q_table_summary.txt", "w") as f:
        for i, (key, value) in enumerate(agent.q_table.items()):
            if i >= 50:
                break
            f.write(f"{key}: {value}\n")

    print("Resumen de la tabla Q guardado en 'q_table_summary.txt'.")

def play_with_ai(game, agent):
    try:
        with open("q_table.pkl", "rb") as f:
            agent.q_table = pickle.load(f)
        print(f"Tabla Q cargada. Estados aprendidos: {len(agent.q_table)}")
    except FileNotFoundError:
        print("No se encontró una tabla Q entrenada. Ejecuta el entrenamiento primero.")
        exit()

    agent.epsilon = agent.epsilon_min

    game.start_game(1)  # Start the game with track 1 for AI play
    state = (game.car.pos, game.car.angle, game.car.speed)  # Initialize the state
    game.running = True
    while game.running:
        action = agent.choose_action(state)
        if action == (-game.car.direction[0], -game.car.direction[1]):
            action = random.choice([a for a in ACTIONS if a != (-game.car.direction[0], -game.car.direction[1])])
        state, _, done = game.step(action)
        game.draw()
        game.clock.tick(25)
    pygame.quit()

def play_manual(game):
    game.reset()
    game.state = "playing"
    while game.state == "playing":
        game.screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.car.rotate(1)
        if keys[pygame.K_RIGHT]:
            game.car.rotate(-1)

        game.car.update()

        if not game.car_on_track(game.car):
            game.state = "game_over"

        if game.detect_lap(game.car):
            game.laps += 1
            game.score += 100 * game.laps
            game.lap_counted = True
        if not game.start_line_rect.collidepoint(game.car.pos.x, game.car.pos.y):
            game.lap_counted = False

        game.screen.blit(game.track_surface, (0, 0))
        game.car.draw(game.screen)
        info = game.font.render(f"Laps: {game.laps}  Score: {game.score}", True, WHITE)
        game.screen.blit(info, (WIDTH - info.get_width() - 20, 20))
        pygame.display.flip()
        game.clock.tick(25)

    if game.state == "game_over":
        game.screen.fill(BLACK)
        msg = game.font.render("Game Over!", True, RED)
        msg2 = game.font.render(f"Laps: {game.laps}  Score: {game.score}", True, WHITE)
        game.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
        game.screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + msg2.get_height()))
        pygame.display.flip()
        time.sleep(3)
        game.reset()

def dump_database():
    if os.path.exists("q_table.pkl"):
        os.remove("q_table.pkl")
        print("Tabla Q eliminada correctamente.")
    else:
        print("No hay una tabla Q guardada.")

    if os.path.exists("q_table_summary.txt"):
        os.remove("q_table_summary.txt")
        print("Resumen de la tabla Q eliminado.")

def main():
    print("Selecciona una opción:")
    print("(1) Entrenar IA")
    print("(2) Jugar con IA")
    print("(3) Jugar manualmente")
    print("(4) Borrar datos de la tabla Q")

    choice = input("Opción: ")
    game = RacingGame()
    
    AGENT_CONFIG = {
        "ALPHA": ALPHA,
        "GAMMA": GAMMA,
        "EPSILON": EPSILON,
        "EPSILON_DECAY": EPSILON_DECAY,
        "EPSILON_MIN": EPSILON_MIN,
        "ACTIONS": ACTIONS,
    }
    
    agent = QLearningAgent(AGENT_CONFIG)

    if choice == "1":
        train_ai(game, agent)
    elif choice == "2":
        play_with_ai(game, agent)
    elif choice == "3":
        play_manual(game)
    elif choice == "4":
        dump_database()
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()