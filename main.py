from Game import Game
from model.RandomPlayer import RandomPlayer
from REINFORCEAgent import REINFORCEAgent
import os
import psutil

def print_memory_usage():
    process = psutil.Process(os.getpid())
    #print(f'Memory Usage: {process.memory_info().rss / 1024 ** 2:.2f} MB')

def main_loop(game, episodes, max_steps_per_episode=800):
    for episode in range(episodes):
        state = game.reset()
        done = False
        total_reward = 0
        steps = 0  # Compteur de pas pour l'épisode courant

        print(f"Starting Episode {episode + 1}")

        while not done and steps < max_steps_per_episode:
            action = agent.act(state)
            next_state, reward, done = game.step(action, game.tile_bag)
            agent.store_transition(state, action, reward)
            state = next_state
            total_reward += reward
            steps += 1

            if steps >= max_steps_per_episode:
                print(f"Episode {episode + 1} terminated after reaching maximum of {max_steps_per_episode} steps.")
                done = True  # Assurez-vous de sortir de la boucle

        agent.learn()
        agent.update_epsilon()
        print(f"Episode {episode + 1}: Total Reward: {total_reward}")

        # Log the memory usage at the end of each episode
        #memory_usage = print_memory_usage()
        #print(f"Memory Usage: {memory_usage} MB")
        
        #if total_reward == 0:
            #print("Warning: Zero reward obtained, possible stuck state")



if __name__ == "__main__":
    state_size = 53  # Assurez-vous que cette taille est correcte selon votre environnement
    action_size = 38  # Assurez-vous que cette taille est correcte selon votre environnement

    agent = REINFORCEAgent(state_size, action_size)
    game = Game([agent, RandomPlayer("Random")])
    num_episodes = 1000

    main_loop(game, num_episodes)

    # Choisissez une des deux lignes suivantes selon votre besoin :
    agent.save_weights("REINFORCE.weights.h5")  # Pour sauver seulement les poids
    agent.model.save('REINFORCE_model.h5')  # Pour sauver le modèle complet

    print("Model and weights saved successfully!")