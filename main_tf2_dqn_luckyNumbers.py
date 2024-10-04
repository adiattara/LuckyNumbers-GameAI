from QLearning.DeepQLearning import Agent
import numpy as np
import tensorflow as tf
from model.Board import Board
from Game import Game
from model.TileBag import TileBag
from model.Player import Player
from utils import plotLearning


class LuckyNumbersEnv:
    def __init__(self, players):
        self.players = players
        self.game = Game(players)
        self.current_player = self.players[0]  # Start with the first player
        self.tile_bag = TileBag(len(players))
        self.done = False
        self.current_tile = None

    def reset(self):
        self.game = Game(self.players)
        self.done = False
        self.current_player = self.players[0]
        self.current_tile = self.tile_bag.draw_tile()
        return self.get_state()

    def get_state(self):
        # Flatten the current player's board (4x4 grid) to a 16-element array
        state = self.current_player.board.grid.flatten()
        # Add the current tile as the 17th element
        return np.append(state, self.current_tile)

    def step(self, action):
        row, col = divmod(action, 4)
        reward = 0

        if self.current_player.board.is_valid_move(row, col, self.current_tile):
            self.current_player.board.place_tile(row, col, self.current_tile)
            reward = 1
        else:
            reward = -1

        if self.current_player.board.is_complete():
            self.done = True
            reward = 10

        self.current_tile = self.tile_bag.draw_tile()
        if self.current_tile == -1:  # No more tiles
            self.done = True

        return self.get_state(), reward, self.done, {}

    def render(self):
        print(f"Current tile: {self.current_tile}")
        self.current_player.board.display_board()


if __name__ == '__main__':

    # Create players
    players = [Player("Agent 1")]  # Only use one agent for simplicity
    env = LuckyNumbersEnv(players)

    lr = 0.001
    n_games = 10000
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr,
                  input_dims=(17,),  # 4x4 board as a flat array
                  n_actions=16, mem_size=1000000, batch_size=64,
                  epsilon_end=0.01)

    scores = []
    eps_history = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()

        eps_history.append(agent.epsilon)
        scores.append(score)

        avg_score = np.mean(scores[-100:])
        print('episode: ', i, 'score %.2f' % score,
              'average_score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)

        if i % 10 == 0 and i > 0:
            agent.save_model()

    filename = f'lucky_numbers_tf2_{n_games}ep.png'
    x = [i + 1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, filename)
