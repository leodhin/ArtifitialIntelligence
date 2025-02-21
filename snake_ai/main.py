import pickle
import os
import sys
import pygame
from snakegame import *
from qlearning_agent import *
from configuration import *

if __name__ == "__main__":
    print("Selecciona una opción:")
    print("(1) Entrenar IA")
    print("(2) Jugar con IA")
    print("(3) Jugar manualmente")
    print("(4) Borrar datos de la tabla Q")

    choice = input("Opción: ")
    game = SnakeGame()
    
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
        num_episodes = NUM_EPISODES
        actual_episode = 0
        total_score = 0
        average_score = 0
        best_score = 0
        trap_deaths_total = 0
        wall_deaths_total = 0
        self_deaths_total = 0

        # Variables para evaluar el crecimiento en bloques de 1000 episodios.
        check_interval = 1000
        last_improvement_episode = 0
        last_average_score = 0

        if os.path.exists("q_table.pkl"):
            with open("q_table.pkl", "rb") as f:
                agent.q_table = pickle.load(f)
            print(f"Tabla Q cargada. Estados aprendidos: {len(agent.q_table)}")
            agent.epsilon = EPSILON_MIN  # Reducimos exploración para aprovechar lo aprendido

        while actual_episode < num_episodes:
            done = False
            state = game.reset()
            while not done:
                valid_actions = [action for action in ACTIONS if action != (-game.direction[0], -game.direction[1])]
                action = agent.choose_action(state, game.direction)
                next_state, reward, done = game.step(action)
                
                agent.update_q(state, action, reward, next_state)
                state = next_state
            
            total_score += game.score
            trap_deaths_total += game.trap_deaths
            wall_deaths_total += game.wall_deaths
            self_deaths_total += game.self_deaths
            best_score = max(best_score, game.score)
            print(f"\rEpisodio {actual_episode + 1}/{num_episodes} - Mejor Score: {best_score} - Promedio Score: {average_score:.2f}", end='', flush=True)
            actual_episode += 1
            average_score = total_score / (actual_episode + 1)
            agent.decay_epsilon()
            
            # Cada 'check_interval' episodios evaluamos el crecimiento del promedio
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
        print(f"Total de veces que la serpiente quedó atrapada: {trap_deaths_total}")
        print(f"Total de veces que la serpiente se chocó con un muro: {wall_deaths_total}")
        print(f"Total de veces que la serpiente se chocó consigo misma: {self_deaths_total}")

        with open("q_table_summary.txt", "w") as f:
            for i, (key, value) in enumerate(agent.q_table.items()):
                if i >= 50:
                    break
                f.write(f"{key}: {value}\n")

        print("Resumen de la tabla Q guardado en 'q_table_summary.txt'.")

    elif choice == "2":
        try:
            with open("q_table.pkl", "rb") as f:
                agent.q_table = pickle.load(f)
            print(f"Tabla Q cargada. Estados aprendidos: {len(agent.q_table)}")
        except FileNotFoundError:
            print("No se encontró una tabla Q entrenada. Ejecuta el entrenamiento primero.")
            exit()
        
        agent.epsilon = agent.epsilon_min  # Fijar epsilon para explotar conocimiento

        state = game.reset()
        game.running = True
        while game.running:
            action = agent.choose_action(state, game.direction)
            state, _, done = game.step(action)
            game.draw()
            game.clock.tick(25)
        if game.trap_deaths != 0:
            print("Trapped!")
        #pygame.quit()

    elif choice == "3":  # Jugar manualmente
        print("Modo manual: Presiona ENTER para comenzar el juego.")
        game.reset()
        
        # Mostrar mensaje de espera
        waiting = True
        while waiting:
            game.screen.fill(BLACK)
            font = pygame.font.Font(None, 36)
            text = font.render("Presiona ENTER para empezar", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            game.screen.blit(text, text_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False

        game.draw()
        game.running = True
        while game.running:
            game.handle_events()
            _, _, done = game.step(game.direction)
            game.draw()
            game.clock.tick(15)
        pygame.quit()

    elif choice == "4":
        if os.path.exists("q_table.pkl"):
            os.remove("q_table.pkl")
            print("Tabla Q eliminada correctamente.")
        else:
            print("No hay una tabla Q guardada.")

        if os.path.exists("q_table_summary.txt"):
            os.remove("q_table_summary.txt")
            print("Resumen de la tabla Q eliminado.")
