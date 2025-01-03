import pygame
import copy
import os
import sys

pygame.init()
size = width, height = 620, 620
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Life')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Board(pygame.sprite.Sprite):
    image = load_image('animal_cell.png')
    image = pygame.transform.scale(image, (30, 30))
    def __init__(self, width, height):
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        cell_image = load_image('animal_cell.png')
        x, y = self.left, self.top
        for row in range(1, len(self.board) - 1):
            for col in range(1, len(self.board[row]) - 1):
                if self.board[col][row] == 0:
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, self.cell_size, self.cell_size), 1)
                    cell = pygame.sprite.Sprite(all_sprites)
                    cell.image = cell_image
                    cell.rect = cell.image.get_rect()
                    cell.rect.x = x + (self.cell_size // 2)
                    cell.rect.y = y + (self.cell_size // 2)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        if (mouse_pos[0] > self.left + self.width * self.cell_size or mouse_pos[
            1] > self.top + self.height * self.cell_size) \
                or (mouse_pos[0] < self.left or mouse_pos[1] < self.top):
            return None
        else:
            x, y = (mouse_pos[0] - self.left + self.cell_size) // self.cell_size, (
                        mouse_pos[1] - self.top + self.cell_size) // self.cell_size
            return (x, y)

    def click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            x, y = cell
            self.board[x][y] = (self.board[x][y] + 1) % 2

    def get_new_board(self, new_board):
        self.board = new_board

    def give_board(self):
        return self.board


class Life:
    def __init__(self, board):
        self.board = board

    def next_move(self):
        board_copy = copy.deepcopy(self.board)
        for row in range(1, len(self.board) - 1):
            for col in range(1, len(self.board[row]) - 1):
                neighbours = [self.board[row - 1][col], self.board[row - 1][col - 1], self.board[row][col - 1],
                              self.board[row + 1][col - 1], self.board[row + 1][col], self.board[row + 1][col + 1],
                              self.board[row][col + 1], self.board[row - 1][col + 1]]
                if self.board[row][col] == 0:
                    if neighbours.count(1) == 3:
                        board_copy[row][col] = 1
                else:
                    if neighbours.count(1) < 2 or neighbours.count(1) > 3:
                        board_copy[row][col] = 0
        return board_copy


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()

    clock = pygame.time.Clock()
    timer = 10

    board = Board(30, 30)
    board.set_view(30, 30, 20)
    new = Life(board.give_board())

    running = True
    stop = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if stop:
                    if event.key == 32:
                        stop = False
                elif event.key == 32:
                    stop = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if stop:
                    if event.button == 3:
                        stop = False
                    else:
                        board.click(event.pos)
                elif event.button == 3:
                    stop = True
                    continue
                if event.button == 5:
                    if not timer == 1:
                        timer -= 1
                elif event.button == 4:
                    timer += 1

        if stop is False:
            new.board = board.give_board()
            board.get_new_board(new.next_move())

        screen.fill((0, 0, 0))
        board.render(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(timer)
