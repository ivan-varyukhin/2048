import random
import copy

SIZE = 4


# получить номер элемента по индексам
def get_number_from_index(i, j):
    return i*SIZE + j + 1


# получить индекс элемента по его номеру
def get_index_from_number(num):
    num -= 1
    return num // SIZE, num % SIZE


# вставить 2 или 4 случайным образом
# на конкретное место в массиве
def insert_2_or_4(mas, x, y):
    if random.random() <= 0.75:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


# получить список номеров пустых ячеек массива
def get_empty_list(mas):
    empty = []
    for i in range(SIZE):
        for j in range(SIZE):
            if mas[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


# проверить наличие пустых ячеек в массиве
def is_zero_in_mas(mas):
    for row in mas:
        if 0 in row:
            return 1
    return 0


# сдвигаем влево
def move_left(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != SIZE:
            row.append(0)
    for i in range(SIZE):
        for j in range(SIZE-1):
            if mas[i][j] == mas[i][j+1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j+1)
                mas[i].append(0)
    return mas, delta, not origin == mas


# сдвигаем вправо
def move_right(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != SIZE:
            row.insert(0, 0)
    for i in range(SIZE):
        for j in range(SIZE-1, 0, -1):
            if mas[i][j] == mas[i][j-1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j-1)
                mas[i].insert(0, 0)
    return mas, delta, not origin == mas


# сдвигаем вверх
def move_up(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for j in range(SIZE):
        column = []
        for i in range(SIZE):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != SIZE:
            column.append(0)
        for i in range(SIZE-1):
            if column[i] == column[i+1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i+1)
                column.append(0)
        for i in range(SIZE):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


# сдвигаем вниз
def move_down(mas):
    origin = copy.deepcopy(mas)
    delta = 0
    for j in range(SIZE):
        column = []
        for i in range(SIZE):
            if mas[i][j] != 0:
                column.append(mas[i][j])
        while len(column) != SIZE:
            column.insert(0, 0)
        for i in range(SIZE-1, 0, -1):
            if column[i] == column[i-1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i-1)
                column.insert(0, 0)
        for i in range(SIZE):
            mas[i][j] = column[i]
    return mas, delta, not origin == mas


# проверяем возможность хода
def can_move(mas):
    for i in range(SIZE-1):
        for j in range(SIZE-1):
            if mas[i][j] == mas[i][j+1] or mas[i][j] == mas[i+1][j]:
                return True
    for i in range(1, SIZE):
        for j in range(1, SIZE):
            if mas[i][j] == mas[i-1][j] or mas[i][j] == mas[i][j-1]:
                return True
    return False
