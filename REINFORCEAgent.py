import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from model.Board import Board
from model.TileBag import TileBag
from tensorflow.keras.models import load_model

class REINFORCEAgent:
    def __init__(self, state_size, action_size, learning_rate=0.02):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.model = self._build_model()
        self.board = Board()
        self.current_tile = None  # Add current tile if the agent needs to remember its last drawn tile
        self.gradients = []
        self.rewards = []
        self.states = []  # Add this line to initialize the list for storing states
        self.actions = []  # Add this line to initialize the list for storing actions
        self.epsilon = 1.0  # Epsilon initial
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.985
        self.optimizer = Adam(learning_rate=self.learning_rate)
        self.entropy_beta = 0.01

    def _build_model(self):
        model = Sequential([
            Input(shape=(self.state_size,)),
            Dense(32, activation='relu', kernel_regularizer=l2(0.01)),  # Ajout d'une régularisation L2 sur la première couche cachée
            #Dense(32, activation='relu', kernel_regularizer=l2(0.01)),  # Ajout d'une régularisation L2 sur la deuxième couche cachée
            Dense(24, activation='relu', kernel_regularizer=l2(0.01)),  # Ajout d'une régularisation L2 sur la troisième couche cachée
            Dense(24, activation='relu', kernel_regularizer=l2(0.01)),  # Ajout d'une régularisation L2 sur la quatrième couche cachée
            Dense(self.action_size, activation='softmax')
        ])
        #model.compile(optimizer=self.optimizer, loss='mse')
        return model
    
    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def act(self, state):
        #print(f"Original State: {state}")
        state = np.reshape(state, [1, self.state_size])
        action_prob = self.model(state).numpy()
       # print(f"Action Probabilities: {action_prob}")
        action = np.random.choice(self.action_size, p=action_prob[0])
        #print(f"Chosen Action: {action}")
        return action


    def discount_rewards(self, rewards, gamma=0.99):
        discounted_r = np.zeros_like(rewards)
        running_add = 0
        for t in reversed(range(len(rewards))):
            running_add = running_add * gamma + rewards[t]
            discounted_r[t] = running_add
        return discounted_r

    def learn(self):
        if not self.rewards:
            #print("No rewards to process.")
            return  # Avoid processing if no rewards have been recorded

        rewards = np.array(self.rewards, dtype=float)
        discounted_rewards = self.discount_rewards(rewards)
        #print(f"Discounted Rewards: {discounted_rewards}")

        mean_rewards = np.mean(discounted_rewards)
        std_rewards = np.std(discounted_rewards) + 1e-10
        discounted_rewards = (discounted_rewards - mean_rewards) / std_rewards
        #print(f"Normalized Rewards: {discounted_rewards}")

        with tf.GradientTape() as tape:
            losses = []
            for state, action, reward in zip(self.states, self.actions, discounted_rewards):
                state = np.reshape(state, [1, self.state_size])
                probs = self.model(state, training=True)
                action_prob = probs[0, action]
                log_prob = tf.math.log(action_prob)
                loss = -log_prob * reward
                losses.append(loss)
            total_loss = tf.reduce_mean(losses)
            #print(f"Total Loss: {total_loss}")

        grads = tape.gradient(total_loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        #print("Gradients applied.")

        self.states, self.actions, self.rewards = [], [], []

    def store_transition(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        #print(f"Stored transition - State: {state}, Action: {action}, Reward: {reward}")


    def take_action(self, action, tile_bag):
        """
        Exécute une action choisie par l'agent et renvoie la récompense ainsi que l'état de terminaison du jeu.

        :param action: L'action à exécuter.
        :param tile_bag: L'instance de TileBag pour tirer ou défausser les tuiles.
        :return: tuple (reward, done)
        """
        reward = 0  # Réinitialiser la récompense pour ne pas récompenser d'actions intermédiaires
        done = False
        board = self.board

        if self.current_tile is None:
            self.current_tile = tile_bag.draw_tile()  # S'assurer d'avoir une tuile pour agir
            if self.current_tile == -1:
                # Jeu terminé, évaluer l'issue
                if board.tile_count() > board.opponent_tile_count():
                    return 1, True  # Récompense si l'agent a plus de tuiles que l'adversaire en fin de partie
                elif board.tile_count() == board.opponent_tile_count():
                    return 0, True  # Pas de récompense ou pénalité si égalité
                else:
                    return -1, True  # Pénalité si l'adversaire a plus de tuiles

        if action < 4**2:
            row, col = divmod(action, 4)
            if board.is_valid_move(row, col, self.current_tile):
                board.place_tile(row, col, self.current_tile)
                self.current_tile = None  # Réinitialiser la tuile après le placement
                done = board.is_complete()  # Vérifie si le placement termine le jeu
                if done:
                    if board.tile_count() > board.opponent_tile_count():
                        reward = 1  # Récompense si l'agent a plus de tuiles que l'adversaire en fin de partie
                    elif board.tile_count() == board.opponent_tile_count():
                        reward = 0  # Pas de récompense ou pénalité si égalité
                    else:
                        reward = -1  # Pénalité si l'adversaire a plus de tuiles
            else:
                done = True  # Terminer le jeu avec une pénalité pour mouvement invalide
                reward = -1  # Pénalité immédiate
        elif action == 4**2:
            if self.current_tile is not None:
                tile_bag.discard_tile(self.current_tile)
                self.current_tile = None
                # Aucune récompense pour défausser une tuile, même si c'est une action valide

        return reward, done


    
    def load_model(self, model_path):
        """
        Load a trained model from a file.
        """
        self.model = load_model(model_path)
        print("Model loaded successfully!")

    def save_weights(self, filepath):
        """Save the model's weights."""
        self.model.save_weights(filepath)

    def load_weights(self, filepath):
        """Load weights into the model."""
        self.model.load_weights(filepath)

