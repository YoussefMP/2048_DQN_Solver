import random
import pygame


class Game:

    def __init__(self):
        self.state = []
        self.score = 0
        self.game_over = False
        self.start_game()

    def start_game(self):
        for _ in range(4):
            self.state.append([0, 0, 0, 0])

        i, j = random.randint(0, 3), random.randint(0, 3)
        self.state[i][j] = Game.fill_cell()
        self.compute_score()
        return self.state

    def reset_game(self):
        self.state = []
        self.game_over = False
        self.start_game()

    def check_game_over(self):
        for row in self.state:
            if 0 in row:
                return False

        for row in self.state:
            for i in range(3):
                if row[i] == row[i + 1]:
                    return False  # Merge possible

        # 3. Check vertical merges
        for col in range(4):
            for row in range(3):
                if self.state[row][col] == self.state[row + 1][col]:
                    return False  # Merge possible

        # No empty cells and no merges possible
        self.game_over = True

    def compute_score(self):
        self.score = sum(sum(self.state[i]) for i in range(4))

    @staticmethod
    def fill_cell():
        x = 4 if random.random() > 0.8 else 2
        return x

    def fill_random_cell(self):
        empty_cells = []
        for r in range(4):
            for c in range(4):
                if self.state[r][c] == 0:
                    empty_cells.append((r, c))

        cell = random.randint(0, len(empty_cells)-1)
        try:
            self.state[empty_cells[cell][0]][empty_cells[cell][1]] = Game.fill_cell()
        except IndexError:
            print(f"cell = {cell}")
            print(f"len(empty_cells) = {len(empty_cells)}")
            print(f"empty_cells[cell] = {empty_cells[cell]}")
        return self.state

    def handle_move(self, move):
        moved = False

        if move == pygame.K_UP:
            moved = self.move_up()
        elif move == pygame.K_DOWN:
            moved = self.move_down()
        elif move == pygame.K_RIGHT:
            moved = self.move_right()
        elif move == pygame.K_LEFT:
            moved = self.move_left()
        elif move == pygame.K_RETURN and self.game_over:
            self.reset_game()
            return

        if moved:
            self.fill_random_cell()
            self.compute_score()
            self.check_game_over()

    def move_up(self):
        moved = False
        for col in range(4):
            for row in range(1, 4):

                if self.state[row][col] == 0:
                    continue
                else:
                    curr_row = row
                    while curr_row >= 1:
                        if self.state[curr_row-1][col] == 0:
                            self.state[curr_row-1][col] = self.state[curr_row][col]
                            self.state[curr_row][col] = 0
                            curr_row -= 1
                            moved = True
                            continue
                        elif self.state[curr_row-1][col] == self.state[curr_row][col]:
                            self.state[curr_row-1][col] *= 2
                            self.state[curr_row][col] = 0
                            moved = True
                            break
                        else:
                            break
        return moved

    def move_down(self):
        moved = False
        for col in range(4):
            for row in range(2, -1, -1):

                if self.state[row][col] == 0:
                    continue
                else:
                    curr_row = row
                    while curr_row <= 2:
                        if self.state[curr_row+1][col] == 0:
                            self.state[curr_row+1][col] = self.state[curr_row][col]
                            self.state[curr_row][col] = 0
                            curr_row += 1
                            moved = True
                            continue
                        elif self.state[curr_row+1][col] == self.state[curr_row][col]:
                            self.state[curr_row+1][col] *= 2
                            self.state[curr_row][col] = 0
                            moved = True
                            break
                        else:
                            break
        return moved

    def move_right(self):
        moved = False
        for row in range(4):
            for col in range(2, -1, -1):

                if self.state[row][col] == 0:
                    continue
                else:
                    curr_col = col
                    while curr_col <= 2:
                        if self.state[row][curr_col+1] == 0:
                            self.state[row][curr_col+1] = self.state[row][curr_col]
                            self.state[row][curr_col] = 0
                            curr_col += 1
                            moved = True
                            continue
                        elif self.state[row][curr_col+1] == self.state[row][curr_col]:
                            self.state[row][curr_col+1] *= 2
                            self.state[row][curr_col] = 0
                            moved = True
                            break
                        else:
                            break
        return moved

    def move_left(self):
        moved = False
        for row in range(4):
            for col in range(1, 4):

                if self.state[row][col] == 0:
                    continue
                else:
                    curr_col = col
                    while curr_col >= 1:
                        if self.state[row][curr_col-1] == 0:
                            self.state[row][curr_col-1] = self.state[row][curr_col]
                            self.state[row][curr_col] = 0
                            curr_col -= 1
                            moved = True
                            continue
                        elif self.state[row][curr_col-1] == self.state[row][curr_col]:
                            self.state[row][curr_col-1] *= 2
                            self.state[row][curr_col] = 0
                            moved = True
                            break
                        else:
                            break
        return moved

