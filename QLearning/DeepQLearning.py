import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import MSE

# Enable eager execution
# tf.config.run_functions_eagerly(True)

# Deep Q-Learning Agent

class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0

        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32)

    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.reward_memory[index] = reward
        self.action_memory[index] = action
        self.terminal_memory[index] = 1 - int(done)
        self.mem_cntr += 1

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        states_ = self.new_state_memory[batch]
        rewards = self.reward_memory[batch]
        actions = self.action_memory[batch]
        terminal = self.terminal_memory[batch]

        return states, actions, rewards, states_, terminal


def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    model = keras.Sequential([
        keras.layers.Dense(fc1_dims, activation='relu', input_shape=(input_dims[0],)),
        keras.layers.Dense(fc2_dims, activation='relu'),
        keras.layers.Dense(n_actions, activation=None)])
    model.compile(optimizer=Adam(learning_rate=lr), loss='mse')

    return model


class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, input_dims,
                 epsilon_dec=1e-3, epsilon_end=0.01, mem_size=1000000, fname='dqn_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.n_actions = n_actions  # Store n_actions as class attribute
        self.q_eval = build_dqn(lr, n_actions, input_dims, 256, 256)

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, observation):
        if np.random.random() < self.epsilon:
            action = np.random.choice(self.action_space)
        else:
            state = np.array([observation], dtype=np.float32)
            actions = self.q_eval.predict(state, verbose=0)
            action = np.argmax(actions)

        return action

    @tf.function
    def train_step(self, states, actions, rewards, next_states, dones):
        with tf.GradientTape() as tape:
            q_values = self.q_eval(states, training=True)
            next_q_values = self.q_eval(next_states, training=False)

            max_next_q_values = tf.reduce_max(next_q_values, axis=1)
            target_q_values = rewards + (1 - dones) * self.gamma * max_next_q_values

            # Use self.n_actions instead of trying to get it from the model output
            mask = tf.one_hot(actions, self.n_actions)
            q_values_masked = tf.reduce_sum(q_values * mask, axis=1)

            loss = MSE(target_q_values, q_values_masked)

        gradients = tape.gradient(loss, self.q_eval.trainable_variables)
        self.q_eval.optimizer.apply_gradients(zip(gradients, self.q_eval.trainable_variables))

        return loss

    def learn(self):
        if self.memory.mem_cntr < self.batch_size:
            return

        # Sample from the memory buffer
        states, actions, rewards, next_states, dones = \
            self.memory.sample_buffer(self.batch_size)

        # Convert to TensorFlow tensors if not already
        states = tf.convert_to_tensor(states, dtype=tf.float32)
        next_states = tf.convert_to_tensor(next_states, dtype=tf.float32)
        rewards = tf.convert_to_tensor(rewards, dtype=tf.float32)
        actions = tf.convert_to_tensor(actions, dtype=tf.int32)
        dones = tf.convert_to_tensor(dones, dtype=tf.float32)

        # Perform the model predictions
        loss = self.train_step(states, actions, rewards, next_states, dones)

        self.epsilon = max(self.epsilon - self.eps_dec, self.eps_min)

        return loss

    def save_model(self):
        self.q_eval.save(self.model_file.replace('.h5', '.keras'))

    def load_model(self):
        self.q_eval = keras.models.load_model(self.model_file.replace('.h5', '.keras'))
