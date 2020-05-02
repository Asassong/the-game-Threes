import random
import pygame
import sys

# threes python版 v1.0
"""
待更新： 预览，自动判断结束，下一个数显示，生成新数概率修正
未知可否更新： 背景图片，动画
"""


running = True
stage = 0
text = 0
board = [[-3 for i in range(4)]for j in range(4)]
screen = pygame.display.set_mode((500, 500))


def main():
    pygame.init()
    pygame.display.set_caption('Threes')
    screen.fill((240, 240, 206))
    rectangle = pygame.Rect(50, 50, 400, 400)
    pygame.draw.rect(screen, (161, 210, 212), rectangle)
    pygame.display.update()
    for i in range(9):
        get_next_num()
        add_tile("any")
    output()
    run()


def run():
    while running:
        key_control()


def output():
    render()
    get_next_num()
    print("下一个数是:" + turn(stage))


def turn(num):
    if num == -3:
        result = ""
    elif num < 0:
        result = str(-num)
    else:
        result = str(2 ** num * 3)
    return result


def get_empty_spaces():
    empty = []
    for i, array in enumerate(board):
        for j, tile in enumerate(array):
            if tile == -3:
                empty.append([i, j])
    return empty


def judge_max_number(tiles):
    return max(map(max, tiles))


def add_tile(situation):
    if situation == "any":
        empty = get_empty_spaces()
    else:
        empty = situation
    chosen = random.choice(empty)
    board[chosen[0]][chosen[1]] = stage


def get_next_num():
    global stage
    if judge_max_number(board) > 3:
        r_num = random.randrange(1, 5)
    else:
        r_num = random.randrange(1, 4)
    if r_num == 1:
        stage = -1
    elif r_num == 2:
        stage = -2
    elif r_num == 3:
        stage = 0  # -1对应1，-2对应2，0对应3
    else:
        new_stage = judge_max_number(board) - 3
        if new_stage < 3:
            stage = random.randrange(1, 1 + new_stage)  # 当stage为4或5，只能产生6或6，12
        else:
            new_stage -= 2  # 当stage大于等于6，可能产生多组3个数，先从中挑一组
            stage = random.randrange(1, 1 + new_stage)
            stage += random.randrange(0, 3)


def move_left():
    empty = []
    num = []
    is_moved = False
    for i in range(0, 4):   # 1，2合成3，相同合成更高一级
        for j in range(1, 4):
            if is_wall(i, j, "left"):
                if board[i][j] + board[i][j - 1] == -3 and board[i][j] * board[i][j - 1] > 0:
                    board[i][j - 1] = 0
                    board[i][j] = -3
                    num.append(i)
                elif board[i][j] == board[i][j - 1] and board[i][j] >= 0:
                    board[i][j - 1] = board[i][j - 1] + 1
                    board[i][j] = -3
                    num.append(i)
    for i in range(0, 4):
        for j in range(0, 3):
            if board[i][j] == -3:
                board[i][j] = board[i][j + 1]
                board[i][j + 1] = -3
            if board[i][j] != -3:
                is_moved = True
    for i in range(4):
        if board[i][3] == -3:
            if i in num:
                for a in range(9):
                    empty.append([i, 3])
            else:
                empty.append([i, 3])
    if is_moved:
        add_tile(empty)
        output()


def move_down():
    empty = []
    num = []
    is_moved = False
    for i in range(3, 0, -1):   # 1，2合成3，相同合成更高一级
        for j in range(0, 4):
            if is_wall(i, j, "down"):
                if board[i][j] + board[i-1][j] == -3 and board[i][j] * board[i-1][j] > 0:
                    board[i][j] = 0
                    board[i-1][j] = -3
                    num.append(j)
                elif board[i][j] == board[i-1][j] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i-1][j] = -3
                    num.append(j)
    for i in range(2, -1, -1):
        for j in range(0, 4):
            if board[i+1][j] == -3:
                board[i+1][j] = board[i][j]
                board[i][j] = -3
            if board[i+1][j] != -3:
                is_moved = True
    for j in range(4):
        if board[0][j] == -3:
            if j in num:
                for a in range(9):
                    empty.append([0, j])
            else:
                empty.append([0, j])
    if is_moved:
        add_tile(empty)
        output()


def move_right():
    empty = []
    num = []
    is_moved = False
    for i in range(0, 4):   # 1，2合成3，相同合成更高一级
        for j in range(3, 0, -1):
            if is_wall(i, j, "right"):
                if board[i][j] + board[i][j-1] == -3 and board[i][j] * board[i][j-1] > 0:
                    board[i][j] = 0
                    board[i][j-1] = -3
                    num.append(i)
                elif board[i][j] == board[i][j-1] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i][j-1] = -3
                    num.append(i)
    for i in range(0, 4):
        for j in range(2, -1, -1):
            if board[i][j+1] == -3:
                board[i][j+1] = board[i][j]
                board[i][j] = -3
            if board[i][j + 1] != -3:
                is_moved = True
    for i in range(4):
        if board[i][0] == -3:
            if i in num:
                for a in range(9):
                    empty.append([i, 0])
            else:
                empty.append([i, 0])
    if is_moved:
        add_tile(empty)
        output()


def move_up():
    empty = []
    num = []
    is_moved = False
    for i in range(0, 3):   # 1，2合成3，相同合成更高一级
        for j in range(0, 4):
            if is_wall(i, j, "up"):
                if board[i][j] + board[i+1][j] == -3 and board[i+1][j] * board[i][j] > 0:
                    board[i][j] = 0
                    board[i+1][j] = -3
                    num.append(j)
                elif board[i][j] == board[i+1][j] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i+1][j] = -3
                    num.append(j)
    for i in range(1, 4):
        for j in range(0, 4):
            if board[i-1][j] == -3:
                board[i-1][j] = board[i][j]
                board[i][j] = -3
            if board[i - 1][j] != -3:
                is_moved = True
    for j in range(4):
        if board[3][j] == -3:
            if j in num:
                for a in range(9):
                    empty.append([3, j])
            else:
                empty.append([3, j])
    if is_moved:
        add_tile(empty)
        output()


def key_control():
    global running
    for event in pygame.event.get():    # 玄学错误 列表二维坐标颠倒
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_up()
            if event.key == pygame.K_d:
                move_down()
            if event.key == pygame.K_w:
                move_left()
            if event.key == pygame.K_s:
                move_right()


def is_wall(i, j, direction):
    if direction == "left":
        if j == 1:
            return True
        elif j > 1 and board[i][j-1] != -3:
            return True
        else:
            return False
    elif direction == "down":
        if i == 3:
            return True
        elif i < 3 and board[i+1][j] != -3:
            return True
        else:
            return False
    elif direction == "right":
        if j == 3:
            return True
        elif j < 3 and board[i][j+1] != -3:
            return True
        else:
            return False
    elif direction == "up":
        if i == 0:
            return True
        elif i > 0 and board[i-1][j] != -3:
            return True
        else:
            return False


def render():
    global text     # 非全局变量时 weak warning 运行正常
    font = pygame.font.SysFont('comicsans', 61)
    for i, array in enumerate(board):  # i 序号 array 数组
        for j, tile in enumerate(array):  # j 序号 tile 元素
            if tile == -3:
                color = (131, 162, 163)
            elif tile == -2:
                color = (225, 105, 133)  # 1蓝底，2红底，3以上白底
            elif tile == -1:
                color = (52, 180, 235)
            else:
                color = (245, 240, 255)
            rectangle = pygame.Rect(60 + i * 87 + 10 * i, 60 + j * 87 + 10 * j, 87, 87)
            pygame.draw.rect(screen, color, rectangle)
            if tile != -3:
                if -3 < tile <= -1:
                    text = font.render(str(-tile), 2, (250, 248, 239))  # 1，2白字，3以上黑字
                elif tile > -1:
                    text = font.render(str(2 ** tile * 3), 2, (5, 7, 16))
                x = 60 + i * 87 + 10 * i
                y = 60 + j * 87 + 10 * j
                screen.blit(text, (x + (87 / 2 - text.get_width() / 2), y + (87 / 2 - text.get_height() / 2)))
            pygame.display.update()


if __name__ == "__main__":
    main()
