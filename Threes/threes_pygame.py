import random
import pygame
import sys
import copy

# threes python版 v1.2
"""
待更新（非近期）：动画，代码优化
W A S D键控制，shift + W A S D 键预览，ESC键退出，菜单中重试或结束后按回车键重玩，统计只是个装饰
"""


running = True
stage = 0
text = 0
board = [[-3 for i in range(4)]for j in range(4)]
stage_array = []
screen = pygame.display.set_mode((360, 720))
menu_clicked = False


def main():
    global board
    pygame.init()
    pygame.display.set_caption('Threes')
    screen.fill((250, 250, 250))
    board = [[-3 for i in range(4)] for j in range(4)]
    menu = pygame.image.load("menu.png").convert_alpha()
    screen.blit(menu, (45, 98))
    statistics = pygame.image.load("statistics.png").convert_alpha()
    screen.blit(statistics, (258, 98))
    font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 16)
    next_text = font.render("菜单", 2, (119, 126, 142))
    screen.blit(next_text, (45, 140))
    next_text = font.render("统计", 2, (119, 126, 142))
    screen.blit(next_text, (312 - next_text.get_width(), 140))
    for i in range(9):
        get_next_num()
        add_tile("any")
    output()
    run()


def run():
    while running:
        key_control()


def output():
    get_next_num()
    render(board)
    draw_next_num()


def draw_next_num():
    pygame.draw.rect(screen, (250, 250, 250), (110, 110, 130, 30))
    background = pygame.image.load("back1.png").convert_alpha()
    screen.blit(background, (154, 86))
    font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 16)
    next_text = font.render("下一个", 2, (119, 126, 142))
    screen.blit(next_text, (180 - next_text.get_width()/2, 165 - next_text.get_height() / 2))
    if stage == -1:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (165, 99))
        next_one = pygame.image.load("blue1.png").convert_alpha()
        screen.blit(next_one, (166, 100))
    if stage == -2:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (165, 99))
        next_two = pygame.image.load("red1.png").convert_alpha()
        screen.blit(next_two, (166, 100))
    if stage == 0:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (165, 99))
        next_three = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_three, (166, 100))
    if stage == 1:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (165, 99))
        next_one = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_one, (166, 100))
        next_text = font.render("6", 2, (0, 0, 0))
        screen.blit(next_text, (180 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
    if stage == 2:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (140, 99))
        next_two = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_two, (142, 100))
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (190, 99))
        next_two = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_two, (191, 99))
        next_text = font.render("6", 2, (0, 0, 0))
        screen.blit(next_text, (154 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
        next_text = font.render("12", 2, (0, 0, 0))
        screen.blit(next_text, (205 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
    if stage > 2:
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (126, 99))
        next_three = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_three, (128, 100))
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (164, 99))
        next_three = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_three, (166, 100))
        tile_back = pygame.image.load("tile_back.png").convert_alpha()
        screen.blit(tile_back, (203, 99))
        next_three = pygame.image.load("white1.png").convert_alpha()
        screen.blit(next_three, (205, 100))
        next_text = font.render(turn(stage_array[0]), 2, (0, 0, 0))
        screen.blit(next_text, (142 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
        next_text = font.render(turn(stage_array[1]), 2, (0, 0, 0))
        screen.blit(next_text, (180 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
        next_text = font.render(turn(stage_array[2]), 2, (0, 0, 0))
        screen.blit(next_text, (220 - next_text.get_width() / 2, 117 - next_text.get_height() / 2))
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
        empty = get_empty_spaces()   # 开始时随机生成，游戏中受移动方向控制
    else:
        empty = situation
    chosen = random.choice(empty)
    board[chosen[0]][chosen[1]] = stage


def get_next_num():     # 1，2，3，3以上的数概率为105:105:105:15,当最大数大于等于48时开始产生3以上的数
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
    if minus_two > minus_one:       # 1和2的数量差多少就补多少
        stage_array.extend([-1]*(minus_two - minus_one))
    else:
        stage_array.extend([-2]*(minus_one - minus_two))


def move_left(a_board):
    empty = []
    num = []
    num2 = []
    is_moved = False
    for i, array in enumerate(a_board):
        for j, tile in enumerate(array):
            if j < 3:
                if tile == -3 and a_board[i][j + 1] != -3:
                    a_board[i][j] = a_board[i][j + 1]
                    a_board[i][j + 1] = -3
                    is_moved = True
                    num2.append(i)
                else:
                    if a_board[i][j] + a_board[i][j + 1] == -3 and a_board[i][j] * a_board[i][j + 1] > 0:
                        a_board[i][j] = 0
                        a_board[i][j + 1] = -3
                        num.append(i)
                        is_moved = True
                    elif a_board[i][j] == a_board[i][j + 1] and a_board[i][j] >= 0:
                        a_board[i][j] = a_board[i][j] + 1
                        a_board[i][j + 1] = -3
                        num.append(i)
                        is_moved = True
    for i in range(4):
        if a_board[i][3] == -3:
            if i in num:
                for a in range(9):
                    empty.append([i, 3])
            elif i in num:
                for a in range(3):
                    empty.append([i, 3])
            else:
                empty.append([i, 3])
    if is_moved and a_board == board:
        add_tile(empty)
        output()
    end_game()


def move_down(a_board):
    empty = []
    num = []
    num2 = []
    is_moved = False
    for i in range(3, 0, -1):
        for j, tile in enumerate(a_board[i]):
            if tile == -3 and a_board[i - 1][j] != -3:
                a_board[i][j] = a_board[i - 1][j]
                a_board[i - 1][j] = -3
                is_moved = True
                num2.append(j)
            else:
                if a_board[i][j] + a_board[i - 1][j] == -3 and a_board[i][j] * a_board[i - 1][j] > 0:
                    a_board[i][j] = 0
                    a_board[i - 1][j] = -3
                    num.append(j)
                    is_moved = True
                elif a_board[i][j] == a_board[i - 1][j] and a_board[i][j] >= 0:
                    a_board[i][j] = a_board[i][j] + 1
                    a_board[i - 1][j] = -3
                    num.append(j)
                    is_moved = True
    for j in range(4):
        if a_board[0][j] == -3:
            if j in num:
                for a in range(9):
                    empty.append([0, j])
            elif j in num2:
                for a in range(3):
                    empty.append([0, j])
            else:
                empty.append([0, j])
    if is_moved and a_board == board:
        add_tile(empty)
        output()
    end_game()


def move_right(a_board):
    empty = []
    num = []
    num2 = []
    is_moved = False
    for i in range(0, 4):   # 1，2合成3，相同合成更高一级
        for j in range(3, 0, -1):
            if a_board[i][j] == -3 and a_board[i][j - 1] != -3:
                a_board[i][j], a_board[i][j - 1] = a_board[i][j - 1], a_board[i][j]
                is_moved = True
                num2.append(i)
            else:
                if a_board[i][j] + a_board[i][j - 1] == -3 and a_board[i][j] * a_board[i][j - 1] > 0:
                    a_board[i][j] = 0
                    a_board[i][j - 1] = -3
                    num.append(i)
                    is_moved = True
                elif a_board[i][j] == a_board[i][j - 1] and a_board[i][j] >= 0:
                    a_board[i][j] = a_board[i][j] + 1
                    a_board[i][j - 1] = -3
                    num.append(i)
                    is_moved = True
    for i in range(4):
        if a_board[i][0] == -3:
            if i in num:
                for a in range(9):
                    empty.append([i, 0])
            elif i in num:
                for a in range(3):
                    empty.append([i, 0])
            else:
                empty.append([i, 0])
    if is_moved and a_board == board:
        add_tile(empty)
        output()
    end_game()


def move_up(a_board):
    empty = []
    num = []
    num2 = []
    is_moved = False
    for i in range(0, 3):   # 1，2合成3，相同合成更高一级
        for j in range(0, 4):
            if a_board[i][j] == -3 and a_board[i + 1][j] != -3:
                a_board[i][j], a_board[i + 1][j] = a_board[i + 1][j], a_board[i][j]
                is_moved = True
                num2.append(j)
            else:
                if a_board[i][j] + a_board[i + 1][j] == -3 and a_board[i + 1][j] * a_board[i][j] > 0:
                    a_board[i][j] = 0
                    a_board[i + 1][j] = -3
                    num.append(j)
                    is_moved = True
                elif a_board[i][j] == a_board[i + 1][j] and a_board[i][j] >= 0:
                    a_board[i][j] = a_board[i][j] + 1
                    a_board[i + 1][j] = -3
                    num.append(j)
                    is_moved = True
    for j in range(4):
        if a_board[3][j] == -3:
            if j in num:
                for a in range(9):
                    empty.append([3, j])
            if j in num:
                for a in range(3):
                    empty.append([3, j])
            else:
                empty.append([3, j])
    if is_moved and a_board == board:
        add_tile(empty)
        output()
    end_game()


def key_control():
    global running, menu_clicked
    key_list = pygame.key.get_pressed()
    for event in pygame.event.get():    # 玄学错误 列表二维坐标颠倒
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            button_clicked = button(event.pos[0], event.pos[1])   # 获得鼠标点击位置
            if menu_clicked and not button_clicked[1]:  # 点击菜单按钮后点击其他地方
                menu_clicked = False
                pygame.draw.rect(screen, (250, 250, 250), (0, 0, 360, 50))
            if menu_clicked and button_clicked[1]:      # 点击菜单按钮后点击重试按钮
                menu_clicked = False
                main()
            if button_clicked[0]:                       # 点击菜单按钮
                menu_clicked = True
        if event.type == pygame.KEYDOWN:                # W A S D键移动 如果有按下shift则为预览
            if event.key == pygame.K_a:
                if not key_list[pygame.K_LSHIFT]:
                    move_up(board)
                else:
                    preview("up")
            if event.key == pygame.K_d:
                if not key_list[pygame.K_LSHIFT]:
                    move_down(board)
                else:
                    preview("down")
            if event.key == pygame.K_w:
                if not key_list[pygame.K_LSHIFT]:
                    move_left(board)
                else:
                    preview("left")
            if event.key == pygame.K_s:
                if not key_list[pygame.K_LSHIFT]:
                    move_right(board)
                else:
                    preview("right")
            if event.key == pygame.K_ESCAPE:            # ESC键退出
                running = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                if is_end():
                    main()    # 结束按enter键重开

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:        # 抬起shift键结束预览
                render(board)
                draw_next_num()


def button(left, top):
    menu = pygame.image.load("menu.png").convert_alpha()
    menu_button = False
    retry_button = False
    if 45 <= left <= menu.get_width() + 45 and 98 <= top <= menu.get_height() + 98:  # 菜单按钮的位置
        menu_window()
        menu_button = True
    if 30 <= left <= 90 and 10 <= top <= 40:    # 重试按钮的位置
        retry_button = True
    return menu_button, retry_button


def menu_window():
    rect = pygame.Surface((360, 50), pygame.SRCALPHA, 32)
    rect.fill((66, 175, 242, 50))
    screen.blit(rect, (0, 0))
    pygame.draw.rect(screen, (119, 127, 140), (30, 10, 60, 30))
    font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 16)
    next_text = font.render("重试", 2, (250, 250, 250))
    screen.blit(next_text, (60 - next_text.get_width() / 2, 25 - next_text.get_height() / 2))
    pygame.display.update()


def preview(direction):
    copy_board = copy.deepcopy(board)
    if direction == "left":
        move_left(copy_board)
    if direction == "down":
        move_down(copy_board)
    if direction == "right":
        move_right(copy_board)
    if direction == "up":
        move_up(copy_board)
    render(copy_board)
    draw_next_num()


def render(a_board):
    background = pygame.image.load("background.png").convert_alpha()
    screen.blit(background, (45, 230))
    for i, array in enumerate(a_board):
        for j, tile in enumerate(array):
            if tile == -3:
                tile_image = pygame.image.load("tile.png").convert_alpha()
                location = (57 + i * 48 + 18 * i, 254 + j * 72 + 12 * j)
                screen.blit(tile_image, location)
            else:
                tile_image = pygame.image.load(turn(tile) + "a.png").convert_alpha()
                x = 81 + i * 48 + 18 * i - tile_image.get_width()/2         # 居中对齐
                y = 254 + j * 72 + 12 * j - 72 + tile_image.get_height()    # 底对齐
                screen.blit(tile_image, (x, y))
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
    pygame.draw.rect(screen, (250, 250, 250), (0, 0, 360, 200))
    for i in board:
        for j in i:
            if j >= 0:
                sum_score += 3 ** (j + 1)
    font = pygame.font.SysFont('comicsans', 80)
    next_text = font.render(str(sum_score), 2, (0, 0, 0))
    screen.blit(next_text, (180 - next_text.get_width()/2, 100 - next_text.get_height() / 2))
    pygame.display.update()


def end_game():
    if is_end():
        render(board)
        pygame.draw.rect(screen, (250, 250, 250), (0, 0, 360, 200))
        for i, array in enumerate(board):
            for j, tile in enumerate(array):
                if tile != judge_max_number(board):
                    tile_image = pygame.image.load(turn(tile) + "b.png").convert_alpha()
                    x = 81 + i * 48 + 18 * i - tile_image.get_width() / 2     # 居中对齐
                    y = 254 + j * 72 + 12 * j - 72 + tile_image.get_height()  # 底对齐
                    screen.blit(tile_image, (x, y))
        font = pygame.font.SysFont('microsoftyaheimicrosoftyaheiui', 40)
        next_text = font.render("动不了了!", 2, (119, 126, 142))
        screen.blit(next_text, (255 - next_text.get_width()/2, 100 - next_text.get_height() / 2))
        pygame.display.update()
        pygame.time.wait(2000)
        score()


if __name__ == "__main__":
    main()
