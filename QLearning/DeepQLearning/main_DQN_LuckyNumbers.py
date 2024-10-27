import numpy as np
import tensorflow as tf
from Game import Game
from DQN_algo import Agent
from model.Player import Player
from model.Board import Board
from model.TileBag import TileBag
from utils import plotLearning, SkipEnv


class LuckyNumbersEnv:
    def __init__(self, players):
        self.players = players
        self.game = Game(players)
        self.tile_bag = TileBag(len(players))
        self.done = False
        self.current_tile = None
        self.current_player = self.players[0]  # Since we're using only one player

    def reset(self):
        self.game.reset()
        self.tile_bag.reset()
        self.done = False
        self.current_player = self.players[0]
        self.current_tile = self.tile_bag.draw_tile()
        return self.get_state()

    def get_state(self):
        return self.game.get_state_description()

    def get_valid_actions(self):
        return self.game.get_valid_actions()

    def step(self, action):
        # Appel à step_action() pour exécuter l'action et obtenir l'état de progression du jeu
        player, reward, done = self.game.step_action(action)

        # Affichage du plateau après l'action
        # print(f"\nPlateau après l'action {action}: \n")
        # player.board.display_board()

        # État du jeu après exécution de l'action
        # print(f"Action exécutée: {action}")
        # print(f"État du plateau:\n{player.board.grid}")
        # print(f"Tuile courante après action: {self.current_tile}")
        # print(f"Fin du jeu: {done}")


        valid_actions_after_step = self.get_valid_actions()

        reward += self.calculate_reward()

        # Récupération de l'état actuel du jeu pour le retour de fonction
        state = self.get_state()

        return state, reward, done

    def calculate_reward(self):
        correct_placements = 0
        for row in range(4):
            for col in range(4):
                if self.current_player.board.grid[row, col] != 0:
                    if self.current_player.board.is_tile_placement_valid(row, col):
                        correct_placements += 1
        bonus_reward = 0
        if self.current_player.board.is_complete():
            bonus_reward += 100
        return correct_placements + bonus_reward

    def get_action_space(self):
        return 38  # Based on the action space defined in the Game class

    def get_state_space(self):
        return len(self.game.get_state_description())

# Deep Q Learning Algorithm
if __name__ == '__main__':
    try:
        gpu_devices = tf.config.experimental.list_physical_devices('GPU')
        if gpu_devices:
            for device in gpu_devices:
                tf.config.experimental.set_memory_growth(device, True)
            print("Configuration pour utiliser toute la mémoire GPU réussie.")
        else:
            print("Aucun GPU détecté.")

    except RuntimeError as e:
        print("Erreur lors de la configuration de la mémoire GPU :", e)
    except Exception as e:
        print("Une erreur inattendue est survenue :", e)
    except RuntimeError as e:
        print("Erreur lors de la configuration de la mémoire GPU :", e)
    except Exception as e:
        print("Une erreur inattendue est survenue :", e)

    players = [Player("Agent 1")]
    env = LuckyNumbersEnv(players)

    # Create the agent
    state_dim = env.get_state_space()
    n_actions = env.get_action_space()
    agent = Agent(gamma=0.99,
                  epsilon=1.0,
                  lr=0.0001,
                  input_dims=[state_dim],
                  n_actions=n_actions,
                  mem_size=50000,
                  batch_size=64,
                  epsilon_end=0.01,
                  epsilon_dec=1e-5,
                  fname='lucky_numbers_dqn.h5')
    scores = []
    eps_history = []

    # Train the agent
    n_games = 1000
    max_steps_per_episode = 180

    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        step_count = 0

        print(f"\nEpisode {i + 1}/{n_games}")
        print("--------------------")

        while not done and step_count < max_steps_per_episode:
            state = env.get_state()
            valid_actions = env.get_valid_actions()
            # print(f"valid_actions: {valid_actions}")
            action = agent.choose_action(state, valid_actions, i, 0.01, n_games)
            observation_, reward, done= env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
            step_count += 1

            # print(f"Step {step_count}: Action = {action}, Reward = {reward}, Done = {done}")

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print(f"\nEpisode Summary:")
        print(f"Score: {score}")
        print(f"Average Score (last 100): {avg_score:.2f}")
        print(f"Epsilon: {agent.epsilon:.4f}")
        print(f"Steps: {step_count}")

    agent.save_model()
    print(f"Model saved at episode {i + 1}")
    print("\nTraining completed.")

    # Plot learning curve
    x = [i + 1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename='lucky_numbers_learning.png')
    print("Learning curve plotted and saved as 'lucky_numbers_learning.png'")
