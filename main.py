import pygame
import copy
import os
import sys
import random

from pygame.examples.cursors import image
from pygame import Color

pygame.init()
FPS = 60
size = width, height = 620, 620
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Life')
cells_lst = []
GRAVITY = 9
clock = pygame.time.Clock()

with open('data/pre-last board', mode="w") as f:
    for i in range(28):
        for j in range(28):
            f.write('0')
        f.write('\n')


def terminate():
    pygame.quit()
    sys.exit()


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


def main_cycle():
    timer = 10
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
                    if event.button == 1:
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


def end_screen():
    score = '0'
    text = ['Your colony lasted',
            score,
            'seconds']
    fon = pygame.transform.scale(load_image('ending.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font_name = os.path.join('data', 'ofont.ru_NK123.ttf')

    font = pygame.font.Font(font_name, 40)
    string_rendered = font.render(text[0], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 150
    intro_rect.x = 150
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(font_name, 80)
    string_rendered = font.render(text[1], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 230
    intro_rect.x = 300
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(font_name, 40)
    string_rendered = font.render(text[2], 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 350
    intro_rect.x = 250
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main_cycle()
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["LIFE",
                  "Rules:",
                  "Revive do not destroy"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font_name = os.path.join('data', 'ofont.ru_NK123.ttf')
    font = pygame.font.Font(font_name, 40)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        if line == "Revive do not destroy":
            intro_rect.x = 130
        else:
            intro_rect.x = 260
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Board:
    def __init__(self, width, height):
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
        x, y = self.left, self.top
        for row in range(1, len(self.board) - 1):
            for col in range(1, len(self.board[row]) - 1):
                pygame.draw.rect(screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, Color(255, 255, 255, 128), (x, y, self.cell_size, self.cell_size), 1)
                surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                surface.fill((0, 0, 0, 128))
                screen.blit(surface, (x, y))
                pos_x = self.left + row * self.cell_size - self.cell_size
                pos_y = self.top + col * self.cell_size - self.cell_size
                if self.board[row][col] == 1:
                    object_cell = Cells((pos_x, pos_y), self.cell_size)
                    cells_lst.append(object_cell)
                else:
                    for c in cells_lst:
                        if c.rect.x == pos_x and c.rect.y == pos_y:
                            all_sprites.remove(c)
                            cells_lst.remove(c)
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
            pos_x = self.left + x * self.cell_size - self.cell_size
            pos_y = self.top + y * self.cell_size - self.cell_size
            self.board[x][y] = (self.board[x][y] + 1) % 2
            if self.board[x][y] == 1:
                create_particles(pygame.mouse.get_pos())
                object_cell = Cells((pos_x, pos_y), self.cell_size)
                cells_lst.append(object_cell)
            else:
                for c in cells_lst:
                    if c.rect.x == pos_x and c.rect.y == pos_y:
                        all_sprites.remove(c)
                        cells_lst.remove(c)

    def get_new_board(self, new_board):
        self.board = new_board

    def give_board(self):
        return self.board

    def give_cell_size(self):
        return self.cell_size


class Life:
    def __init__(self, board):
        self.board = board

    def check_evolution(self, new):
        if self.board == new:
            return 0
        return 1

    def next_move(self):
        with open('data/last_board', mode='w') as f:
            for row in range(1, len(self.board) - 1):
                for col in range(1, len(self.board[row]) - 1):
                    if self.board[row][col] == 0:
                        f.write('0')
                    else:
                        f.write('1')
                f.write('\n')
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
        if self.check_evolution(board_copy) == 0:
            pygame.display.flip()
            clock.tick(1)
            end_screen()
        else:
            return board_copy


class Cells(pygame.sprite.Sprite):
    image = load_image('animal_cell.png')

    def __init__(self, pos, cell_size):
        super().__init__(cells_group, all_sprites)
        self.cell_size = cell_size
        Cells.image = pygame.transform.scale(Cells.image, (self.cell_size, self.cell_size))
        self.image = Cells.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


screen_rect = (0, 0, width, height)


def create_particles(position):
    particle_count = 10
    numbers = range(-7, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Particle(pygame.sprite.Sprite):
    fire = [load_image("particle.png")]
    for scale in (5, 7, 10, 12, 15, 20, 25):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(particles_group, all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    cells_group = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()

    board = Board(30, 30)
    board.set_view(30, 30, 20)
    new = Life(board.give_board())

    start_screen()
    main_cycle()
