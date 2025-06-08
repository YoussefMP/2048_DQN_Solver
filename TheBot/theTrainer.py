import numpy as np
from TheSmartPants import DQNAgent
from TheGame.theGym import GameEnv


def play_random_episode(env, agent):
    state = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = agent.play_move(state)
        next_state, reward, done, _ = env.step(action)
        total_reward = reward
        state = next_state

    return total_reward


def train(env: GameEnv, agent: DQNAgent, episodes=100, batch_size=63, sync_freq=10):
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            action = agent.make_move(state)
            next_state, reward, done, _ = env.step(action)

            agent.replay_buffer.push(state, action, reward, next_state, done)
            state = next_state
            total_reward = reward

            agent.update(batch_size)

        if episode % sync_freq == 0:
            agent.sync_target()

        print(f"Episode {episodes} ended with score {total_reward}")


if __name__ == "__main__":
    from TheGame.TOFE_Game import Game
    env = GameEnv(Game())
    agent = DQNAgent()

    train(env, agent)
