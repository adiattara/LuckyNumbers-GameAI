import os
import numpy as np
import tensorflow as tf
from tensorflow import keras

#### THE AGENT MEMORY ####
# Replay buffer : it's a memory of the transitions that the agent observes
class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_cntr = 0
        # store the transitions in the replay buffer
        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        # store the next state in the replay buffer
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        # store the action in the replay
        self.action_memory = np.zeros(self.mem_size, dtype=np.int32)
        # store the reward in the replay
        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        # store the terminal in the replay
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.bool_)

    # store the transition in the replay buffer
    def store_transition(self, state, action, reward, state_, done):
        index = self.mem_cntr % self.mem_size # to know where to store the transition
        self.state_memory[index] = state
        self.new_state_memory[index] = state_
        self.action_memory[index] = action
        self.reward_memory[index] = reward
        self.terminal_memory[index] = 1 - int(done)
        self.mem_cntr += 1 # to know how many transitions we have stored

    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_cntr, self.mem_size) # to know the maximum number of transitions we have stored
        batch = np.random.choice(max_mem, batch_size, replace=False) # to get a random sample of the transitions. replace=False to avoid the same transition to be sampled more than once
        states = self.state_memory[batch] # to get the states
        states_ = self.new_state_memory[batch] # to get the next states
        rewards = self.reward_memory[batch] # to get the rewards
        actions = self.action_memory[batch] # to get the actions
        terminal = self.terminal_memory[batch] # to get the terminal
        return states, actions, rewards, states_, terminal

def build_dqn(lr, n_actions, input_dims, fc1_dims, fc2_dims):
    model = keras.Sequential([
        keras.layers.Dense(fc1_dims, activation='relu'),
        keras.layers.Dense(fc2_dims, activation='relu'),
        NoisyDense(n_actions, activation=None)
    ])
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss='mse')
    return model

class NoisyDense(keras.layers.Layer):
    def __init__(self, units, activation=None):
        super(NoisyDense, self).__init__()
        self.units = units
        self.activation = activation

    def build(self, input_shape):
        self.kernel_mu = self.add_weight(shape=(input_shape[-1], self.units),
                                         initializer='glorot_uniform',
                                         trainable=True)
        self.kernel_sigma = self.add_weight(shape=(input_shape[-1], self.units),
                                            initializer=keras.initializers.Constant(0.017),
                                            trainable=True)
        self.bias_mu = self.add_weight(shape=(self.units,),
                                       initializer='zeros',
                                       trainable=True)
        self.bias_sigma = self.add_weight(shape=(self.units,),
                                          initializer=keras.initializers.Constant(0.017),
                                          trainable=True)

    def call(self, inputs):
        kernel_epsilon = tf.random.normal(shape=(inputs.shape[-1], self.units))
        bias_epsilon = tf.random.normal(shape=(self.units,))

        kernel = self.kernel_mu + tf.multiply(self.kernel_sigma, kernel_epsilon)
        bias = self.bias_mu + tf.multiply(self.bias_sigma, bias_epsilon)

        output = tf.matmul(inputs, kernel) + bias

        if self.activation is not None:
            output = self.activation(output)

        return output

    def get_config(self):
        config = super(NoisyDense, self).get_config()
        config.update({
            'units': self.units,
            'activation': self.activation
        })
        return config

#### THE AGENT ####
# Agent : it's the brain of the agent that will take the decisions
class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, input_dims,
                 epsilon_dec=1e-7, epsilon_end=0.01, mem_size=1000000, fname=r'D:\DRL 5éme\NEW\LuckyNumbers-GameAI\QLearning\DeepQLearning\dqn_model.h5'):
        """
        :param lr:
        :param gamma: the discount factor which is the importance of the future rewards
        :param n_actions: the number of actions that the agent can take in the environment
        :param epsilon: the exploration rate which is the probability to take a random action
        :param batch_size: the number of transitions that the agent will sample from the replay buffer
        :param input_dims:
        :param epsilon_dec: the rate at which the exploration rate will decrease
        :param epsilon_end: the minimum exploration rate
        :param mem_size: the maximum number of transitions that the agent will store in the replay buffer
        :param fname: the name of the file where the model will be saved
        """
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = fname
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, n_actions, input_dims, 256, 128)


    def store_transition(self, state, action, reward, state_, done):
        self.memory.store_transition(state, action, reward, state_, done)

    def choose_action(self, state, valid_actions, ep_id, end_eps, episodes):
        state = np.array([state])
        q_s = self.q_eval.predict(state)

        # Ajustement de la taille de valid_actions pour correspondre à q_s si nécessaire
        if len(valid_actions) > len(self.action_space):
            valid_actions = valid_actions[:len(self.action_space)]

        mask = np.zeros(len(self.action_space))
        mask[valid_actions] = 1

        dec_eps = (1.0 - ep_id / episodes) * self.epsilon + (ep_id / episodes) * end_eps
        if np.random.rand() < dec_eps:
            return np.random.choice([i for i, val in enumerate(valid_actions) if val != 0])
        else:
            masked_q_s = q_s * np.array(valid_actions) + np.min(q_s) * (1 - np.array(valid_actions))
            return int(np.argmax(masked_q_s))

    def learn(self):

        if self.memory.mem_cntr < self.batch_size:
            return
        states, actions, rewards, states_, dones = self.memory.sample_buffer(self.batch_size)
        q_eval = self.q_eval.predict(states) # to get the Q values of the actions
        q_next = self.q_eval.predict(states_) # to get the Q values of the next states
        q_target = np.copy(q_eval) # The target is the direction in which we want our updates to go
        batch_index = np.arange(self.batch_size, dtype=np.int32) # to get the indices of the batch : [0, 1, 2, ..., batch_size] so that we can update the Q values of the actions in order to minimize the loss
        q_target[batch_index, actions] = rewards + self.gamma * np.max(q_next, axis=1) * (1 - dones) # to update the Q values of the actions
        self.q_eval.train_on_batch(states, q_target) # to train the model on a batch of transitions
        self.epsilon = max(self.eps_min, self.epsilon - self.eps_dec)

    def save_model(self):
        if os.path.exists(self.model_file):
            os.remove(self.model_file)
        self.q_eval.save(self.model_file.replace('.h5', '.keras'), overwrite=True)

    def load_model(self):
        self.q_eval = keras.models.load_model(self.model_file)