import sys
import os
import pygame
import pygame_menu
import json

from logics import *
from database import get_best, cur, insert_result


GAMERS_DB = get_best()

USERNAME = None
mas = None
score = None


def init_const():
    global score, mas
    score = 0
    mas = [[0] * SIZE for _ in range(SIZE)]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    insert_2_or_4(mas, x2, y2)


def draw_top_gamers():
    font_top = pygame.font.SysFont('stxingkai', 30)
    font_gamer = pygame.font.SysFont('stxingkai', 24)
    text_head = font_top.render('Best tries: ', True, COLOR_TEXT)
    text_head_rect = text_head.get_rect()
    text_head_x = (width // 2) + 50
    screen.blit(text_head, (text_head_x, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index+1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, COLOR_TEXT)
        text_gamer_rect = text_gamer.get_rect()
        screen.blit(text_gamer, (5 + text_head_x, 15 +
                    text_head_rect.height + (text_gamer_rect.height + 5)*index))


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont('stxingkai', 70)
    font_score = pygame.font.SysFont('stxingkai', 48)
    font_delta = pygame.font.SysFont('stxingkai', 32)
    text_score = font_score.render('Score: ', True, COLOR_TEXT)
    text_score_value = font_score.render(f'{score}', True, COLOR_TEXT)
    text_score_rect = text_score.get_rect()
    text_score_value_rect = text_score_value.get_rect()
    text_score_y = (TITLE_SIZE - text_score_rect.height) // 2
    text_score_value_y = (TITLE_SIZE - text_score_value_rect.height) // 2
    screen.blit(text_score, (20, text_score_y))
    screen.blit(text_score_value,
                (text_score_rect.width + 35, text_score_value_y))
    if delta > 0:
        text_delta = font_delta.render(f' (+{delta})', True, COLOR_TEXT)
        screen.blit(text_delta, (text_score_rect.width +
                    text_score_value_rect.width + 35, text_score_value_y))
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * BLOCK_SIZE + MARGIN * (column + 1)
            h = row * BLOCK_SIZE + MARGIN * (row + 1) + TITLE_SIZE
            pygame.draw.rect(
                screen, COLORS[value], (w, h, BLOCK_SIZE, BLOCK_SIZE))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (BLOCK_SIZE - font_w) / 2
                text_y = h + (BLOCK_SIZE - font_h) / 2
                screen.blit(text, (text_x, text_y))


def draw_intro():
    img2048 = pygame.image.load('2048logo.png')
    font = pygame.font.SysFont('stxingkai', 70)
    text_welcome = font.render('Welcome!', True, WHITE)
    text_welcome_rect = text_welcome.get_rect()
    text_welcome_x = ((width - LOGO_SIZE - 20) // 2 -
                      text_welcome_rect.width // 2) + LOGO_SIZE + 20
    text_welcome_y = (LOGO_SIZE + 10 - text_welcome_rect.height) // 2
    name = 'Введите имя'
    is_find_name = False
    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Введите имя':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) >= 2 and name != 'Введите имя':
                        global USERNAME
                        USERNAME = name
                        is_find_name = True
                        break
        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(
            img2048, [LOGO_SIZE, LOGO_SIZE]), [10, 10])
        screen.blit(text_welcome, (text_welcome_x, text_welcome_y))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)


def draw_game_over():
    global USERNAME, GAMERS_DB

    img2048 = pygame.image.load('2048logo.png')

    font = pygame.font.SysFont('stxingkai', 65)

    text_game_over = font.render('Game over!', True, WHITE)
    text_game_over_rect = text_game_over.get_rect()
    text_game_over_x = ((width - LOGO_SIZE - 20) // 2 -
                        text_game_over_rect.width // 2) + LOGO_SIZE + 20
    text_game_over_y = (LOGO_SIZE + 10 - text_game_over_rect.height) // 2

    text_score = font.render(f'Вы набрали: {score}', True, WHITE)
    rect_score = text_score.get_rect()
    rect_score.center = screen.get_rect().center

    best_score = GAMERS_DB[0][1]
    if score > best_score:
        text = 'Вы побили рекорд!'
    else:
        text = f'Рекорд: {best_score}'

    font_record = pygame.font.SysFont('stxingkai', 45)
    text_record = font_record.render(text, True, WHITE)
    rect_record = text_score.get_rect()
    text_record_x = screen.get_rect().center[0] - rect_record.width // 2
    text_record_y = screen.get_rect().center[1] + rect_score.height

    insert_result(USERNAME, score)
    GAMERS_DB = get_best()

    make_decision = False
    while not make_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # restart game with name
                    make_decision = True
                    init_const()
                elif event.key == pygame.K_RETURN:
                    # restart game without name
                    USERNAME = None
                    make_decision = True
                    init_const()
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(
            img2048, [LOGO_SIZE, LOGO_SIZE]), [10, 10])
        screen.blit(text_game_over, (text_game_over_x, text_game_over_y))
        screen.blit(text_score, rect_score)
        screen.blit(text_record, (text_record_x, text_record_y))
        pygame.display.update()
    screen.fill(BLACK)


def save_game():
    data = {
        'user': USERNAME,
        'score': score,
        'mas': mas,
    }
    with open('save.json', 'w') as outfile:
        json.dump(data, outfile)
    pygame.quit()
    sys.exit()


def exit_menu():
    menu = pygame_menu.Menu('Сохранить?', width, height,
                            theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Да', save_game)
    menu.add.button('Нет', pygame_menu.events.EXIT)

    menu.mainloop(screen)


def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # save_game()
                exit_menu()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                score += delta
                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    insert_2_or_4(mas, x, y)
                    is_mas_move = False
                draw_interface(score, delta)
                pygame.display.update()


COLOR_TEXT = (255, 127, 0)
COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 230, 255),
    256: (255, 230, 128),
    512: (255, 230, 0),
    1024: (255, 200, 255),
    2048: (255, 200, 128),
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)

BLOCKS = SIZE
BLOCK_SIZE = 110
MARGIN = 10
TITLE_SIZE = 110

LOGO_SIZE = 200

width = BLOCKS*BLOCK_SIZE + MARGIN*(BLOCKS + 1)
height = width + TITLE_SIZE

TITLE_REC = pygame.Rect(0, 0, width, TITLE_SIZE)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048')

path = os.getcwd()
if 'save.json' in os.listdir(path):
    with open('save.json') as file:
        data = json.load(file)
        USERNAME = data['user']
        mas = data['mas']
        score = data['score']
    full_path = os.path.join(path, 'save.json')
    os.remove(full_path)
else:
    init_const()

while True:
    if USERNAME is None:
        draw_intro()
    game_loop()
    draw_game_over()
