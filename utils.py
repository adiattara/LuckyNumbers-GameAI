import matplotlib.pyplot as plt
import numpy as np

def plotLearning(x, scores, epsilons, filename, lines=None):
    fig=plt.figure()
    ax=fig.add_subplot(111, label="1")
    ax2=fig.add_subplot(111, label="2", frame_on=False)

    # Tracer l'évolution d'epsilon
    ax.plot(x, epsilons, color="C0")
    ax.set_xlabel("Game", color="C0")
    ax.set_ylabel("Epsilon", color="C0")
    ax.tick_params(axis='x', colors="C0")
    ax.tick_params(axis='y', colors="C0")

    # Calcul de la moyenne glissante des scores sur les 20 derniers jeux
    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = np.mean(scores[max(0, t-20):(t+1)])

    # Tracer la moyenne glissante des scores
    ax2.scatter(x, running_avg, color="C1")
    ax2.yaxis.tick_right()
    ax2.set_ylabel('Score', color="C1")
    ax2.yaxis.set_label_position('right')
    ax2.tick_params(axis='y', colors="C1")

    # Ajouter des lignes verticales pour marquer des événements si nécessaire
    if lines is not None:
        for line in lines:
            plt.axvline(x=line)

    # Sauvegarder le graphique
    plt.savefig(filename)

# Wrapper qui peut être utile pour combiner plusieurs actions en une seule étape, à conserver si nécessaire
class SkipEnv:
    def __init__(self, env=None, skip=4):
        self.env = env
        self._skip = skip

    def step(self, action):
        t_reward = 0.0
        done = False
        for _ in range(self._skip):
            obs, reward, done, info = self.env.step(action)
            t_reward += reward
            if done:
                break
        return obs, t_reward, done, info

    def reset(self):
        return self.env.reset()
