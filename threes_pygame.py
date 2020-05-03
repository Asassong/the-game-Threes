import random
import pygame
import sys

# threes python版 v1.0.9
"""
待更新： 预览
未知可否更新： 背景图片，动画
"""


running = True
stage = 0
text = 0
board = [[-3 for i in range(4)]for j in range(4)]
stage_array = []
screen = pygame.display.set_mode((500, 600))


def main():
    pygame.init()
    pygame.display.set_caption('Threes')
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
    font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 40)
    next_text = font.render("下一个", 2, (150, 150, 150))
    screen.blit(next_text, (250 - next_text.get_width()/2, 500 - next_text.get_height() / 2))
    if stage <= 0:
        next_text = font.render(turn(stage), 2, (150, 150, 150))
    else:
        s_stage_array = [turn(string) for string in stage_array]
        next_text = font.render(" ".join(s_stage_array), 2, (150, 150, 150))
    screen.blit(next_text, (250 - next_text.get_width()/2, 550 - next_text.get_height() / 2))
    pygame.display.update()


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
    global stage, stage_array
    stage_array = []
    if judge_max_number(board) > 3:
        r_num = random.randrange(330)
    else:
        r_num = random.randrange(315)
    if r_num < 105:
        stage_array.append(-1)
        rate_control()
    elif r_num < 210:
        stage_array.append(-2)
        rate_control()
    elif r_num < 315:
        stage_array.append(0)  # -1对应1，-2对应2，0对应3
    else:
        new_stage = judge_max_number(board) - 3
        if new_stage == 1:
            stage_array.append(1)
        elif new_stage == 2:
            stage_array.extend([1, 2])
        else:
            new_stage -= 2  # 当stage大于等于6，可能产生多组3个数，先从中挑一组
            r_stage = random.randrange(new_stage)
            stage_array.extend([r_stage + 1, r_stage + 2, r_stage + 3])
    stage = random.choice(stage_array)


def rate_control():
    minus_one = 0
    minus_two = 0
    for i in board:
        for j in i:
            if j == -1:
                minus_one += 1
            elif j == -2:
                minus_two += 1
    if minus_two > minus_one:
        stage_array.extend([-1]*(minus_two - minus_one))
    else:
        stage_array.extend([-2]*(minus_one - minus_two))


def move_left():
    empty = []
    num = []
    is_moved = False
    for i, array in enumerate(board):
        for j, tile in enumerate(array):
            if j < 3:
                if tile == -3 and board[i][j+1] != -3:
                    board[i][j] = board[i][j+1]
                    board[i][j+1] = -3
                    is_moved = True
                else:
                    if board[i][j] + board[i][j+1] == -3 and board[i][j] * board[i][j+1] > 0:
                        board[i][j] = 0
                        board[i][j+1] = -3
                        num.append(i)
                        is_moved = True
                    elif board[i][j] == board[i][j+1] and board[i][j] >= 0:
                        board[i][j] = board[i][j] + 1
                        board[i][j+1] = -3
                        num.append(i)
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
    end_game()


def move_down():
    empty = []
    num = []
    is_moved = False
    for i in range(3, 0, -1):
        for j, tile in enumerate(board[i]):
            if tile == -3 and board[i-1][j] != -3:
                board[i][j] = board[i-1][j]
                board[i-1][j] = -3
                is_moved = True
            else:
                if board[i][j] + board[i-1][j] == -3 and board[i][j] * board[i-1][j] > 0:
                    board[i][j] = 0
                    board[i-1][j] = -3
                    num.append(j)
                    is_moved = True
                elif board[i][j] == board[i-1][j] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i-1][j] = -3
                    num.append(j)
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
    end_game()


def move_right():
    empty = []
    num = []
    is_moved = False
    for i in range(0, 4):   # 1，2合成3，相同合成更高一级
        for j in range(3, 0, -1):
            if board[i][j] == -3 and board[i][j-1] != -3:
                board[i][j], board[i][j-1] = board[i][j-1], board[i][j]
                is_moved = True
            else:
                if board[i][j] + board[i][j-1] == -3 and board[i][j] * board[i][j-1] > 0:
                    board[i][j] = 0
                    board[i][j-1] = -3
                    num.append(i)
                    is_moved = True
                elif board[i][j] == board[i][j-1] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i][j-1] = -3
                    num.append(i)
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
    end_game()


def move_up():
    empty = []
    num = []
    is_moved = False
    for i in range(0, 3):   # 1，2合成3，相同合成更高一级
        for j in range(0, 4):
            if board[i][j] == -3 and board[i+1][j] != -3:
                board[i][j], board[i+1][j] = board[i+1][j], board[i][j]
                is_moved = True
            else:
                if board[i][j] + board[i+1][j] == -3 and board[i+1][j] * board[i][j] > 0:
                    board[i][j] = 0
                    board[i+1][j] = -3
                    num.append(j)
                    is_moved = True
                elif board[i][j] == board[i+1][j] and board[i][j] >= 0:
                    board[i][j] = board[i][j] + 1
                    board[i+1][j] = -3
                    num.append(j)
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
    end_game()


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


def render():
    global text     # 非全局变量时 weak warning 运行正常
    font = pygame.font.SysFont('comicsans', 61)
    screen.fill((240, 240, 206))
    rectangle = pygame.Rect(50, 50, 400, 400)
    pygame.draw.rect(screen, (161, 210, 212), rectangle)
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


def is_end():
    flag = False
    for i in board:
        for j in i:
            if j == -3:
                flag = True
    if flag:
        return False
    else:
        for i in range(3):
            for j in range(4):
                if board[i][j] == board[i+1][j] and board[i][j] > -1:
                    return False
                else:
                    if board[i][j] + board[i + 1][j] == -3 and board[i + 1][j] * board[i][j] > 0:
                        return False
        for i in range(4):
            for j in range(3):
                if board[i][j] == board[i][j+1] and board[i][j] > -1:
                    return False
                else:
                    if board[i][j] + board[i][j+1] == -3 and board[i][j+1] * board[i][j] > 0:
                        return False
        return True


def score():
    sum_score = 0
    for i in board:
        for j in i:
            if j >= 0:
                sum_score += 3 ** (j + 1)
    font = pygame.font.SysFont('comicsans', 50)
    next_text = font.render("score:" + str(sum_score), 2, (150, 150, 150))
    screen.blit(next_text, (250 - next_text.get_width()/2, 500 - next_text.get_height() / 2))
    pygame.display.update()


def end_game():
    if is_end():
        render()
        font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 40)
        next_text = font.render("动不了了", 2, (150, 150, 150))
        screen.blit(next_text, (250 - next_text.get_width()/2, 550 - next_text.get_height() / 2))
        pygame.display.update()
        score()


if __name__ == "__main__":
    main()
