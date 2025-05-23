"""Simple Tetris Game using Pygame.

Controls:
    Arrow keys to move and rotate pieces
    Down arrow to drop faster
    Esc to quit

Requires Python 3 and the ``pygame`` library.
"""

import pygame
import random

# Game configuration
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]]  # O
]

COLORS = [
    (0, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (128, 0, 128),
    (255, 165, 0),
    (0, 0, 255),
    (255, 255, 0)
]

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = COLS // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.current = self.new_piece()
        self.drop_counter = 0

    def new_piece(self):
        idx = random.randrange(len(SHAPES))
        return Piece([row[:] for row in SHAPES[idx]], COLORS[idx])

    def valid_position(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + dx
                    new_y = piece.y + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def lock_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell and piece.y + y >= 0:
                    self.board[piece.y + y][piece.x + x] = piece.color
        self.clear_lines()
        self.current = self.new_piece()
        if not self.valid_position(self.current):
            self.game_over()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = ROWS - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [None for _ in range(COLS)])
        self.board = new_board

    def game_over(self):
        pygame.quit()
        quit()

    def drop(self):
        if self.valid_position(self.current, dy=1):
            self.current.y += 1
        else:
            self.lock_piece(self.current)

    def draw_cell(self, x, y, color):
        pygame.draw.rect(
            self.screen,
            color,
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            1
        )

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(x, y, cell)
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_cell(self.current.x + x, self.current.y + y, self.current.color)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.drop_counter += 1
            if self.drop_counter >= FPS // 2:
                self.drop_counter = 0
                self.drop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_LEFT:
                        if self.valid_position(self.current, dx=-1):
                            self.current.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.valid_position(self.current, dx=1):
                            self.current.x += 1
                    elif event.key == pygame.K_DOWN:
                        self.drop()
                    elif event.key == pygame.K_UP:
                        old_shape = [row[:] for row in self.current.shape]
                        self.current.rotate()
                        if not self.valid_position(self.current):
                            self.current.shape = old_shape
            self.draw_board()
        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()
