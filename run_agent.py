from tensorflow.keras.models import load_model
from REINFORCEAgent import REINFORCEAgent
from model.RandomPlayer import RandomPlayer
from Game import Game

def run_game(agent, random_player):
    game = Game([agent, random_player])
    state = game.reset()
    done = False
    while not done:
        action = agent.act(state)
        state, _, done = game.step(action, game.tile_bag)
        if done:
            return "Agent Wins"
        
        action = random_player.act(state)
        state, _, done = game.step(action, game.tile_bag)
        if done:
            return "Random Wins"
    
    return "Draw"

# Initialisation de l'agent
agent = REINFORCEAgent(state_size=53, action_size=38)  # Assurez-vous que les tailles sont correctes
agent.model = load_model('REINFORCE_model.h5')  # Chargement du modèle entier

# Création du joueur aléatoire
random_player = RandomPlayer("Joueur Aléatoire")

# Exécution des parties
results = [run_game(agent, random_player) for _ in range(1000)]

# Affichage des résultats
from collections import Counter
result_counts = Counter(results)

print(f"Agent Wins: {result_counts['Agent Wins']}")
print(f"Random Wins: {result_counts['Random Wins']}")
print(f"Draws: {result_counts['Draw']}")
