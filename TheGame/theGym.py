import numpy as np
import pygame


ACTION_SPACE = {
    0: pygame.K_UP,
    1: pygame.K_DOWN,
    2: pygame.K_LEFT,
    3: pygame.K_RIGHT
}


class GameEnv:
    def __init__(self, game):
        self.game = game
        self.action_space = [0, 1, 2, 3]
        self.observation_space_shape = (4, 4)

    def observe_state(self):
        board = np.array(self.game.state, dtype=np.float32)
        result = np.zeros_like(board)
        np.log2(board, out=result, where=board > 0)
        return result

    def reset(self):
        self.game.reset_game()
        return self.observe_state()

    def step(self, action):
        self.game.handle_move(ACTION_SPACE[action])
        reward, done = self.game.score, self.game.game_over
        next_state = self.observe_state()
        return next_state, reward, done, {}
