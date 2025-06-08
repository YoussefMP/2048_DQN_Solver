import pygame
import sys
import threading
import time
from TheGame.theGym import GameEnv
from TheBot.TheRando import Rando
from TheBot.theTrainer import play_random_episode

GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
SCORE_AREA_HEIGHT = 60  # or any value you prefer
SCREEN_SIZE = SCORE_AREA_HEIGHT + GRID_SIZE * (TILE_SIZE + MARGIN) + MARGIN
FONT_SIZE = 40

BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0:    (205, 193, 180),
    2:    (238, 228, 218),
    4:    (237, 224, 200),
    8:    (242, 177, 121),
    16:   (245, 149, 99),
    32:   (246, 124, 95),
    64:   (246, 94, 59),
    128:  (237, 207, 114),
    256:  (237, 204, 97),
    512:  (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (60, 58, 50),
    8192: (30, 28, 20),
}


def run_bot(game):
    # TODO: move this to the trainer class
    env = GameEnv(game)
    agent = Rando()
    while True:
        if game.game_over:
            input("__________\nGame Lost Restart...")
            game.reset_game()

        action = agent.play_move(env.observe_state())
        env.step(action)
        time.sleep(0.05)  # slow down so it's watchable


def draw_score(screen, score, font):
    pygame.draw.rect(screen, (187, 173, 160), (0, 0, SCREEN_SIZE-SCORE_AREA_HEIGHT, SCORE_AREA_HEIGHT))
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_SIZE//2-text.get_size()[0], MARGIN))


def draw_grid(screen, board, font):

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            value = board[y][x]
            color = TILE_COLORS.get(value, (60, 58, 50))
            rect = pygame.Rect(
                MARGIN + x * (TILE_SIZE + MARGIN),
                SCORE_AREA_HEIGHT + MARGIN + y * (TILE_SIZE + MARGIN),
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(screen, color, rect)
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


def main(game):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE-SCORE_AREA_HEIGHT, SCREEN_SIZE))
    pygame.display.set_caption("2048")
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        draw_score(screen, game.score, font)
        draw_grid(screen, game.state, font)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                game.handle_move(event.key)
        clock.tick(10)


if __name__ == "__main__":
    from TOFE_Game import Game
    gameInstance = Game()
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, args=(gameInstance,))
    bot_thread.daemon = True
    bot_thread.start()

    # Launch the game UI
    main(gameInstance)
