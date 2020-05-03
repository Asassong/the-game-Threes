import keyboard
import random


# threes 控制台版 v1.0

running = True
stage = 0
stage_array = []


def main():
    for i in range(9):
        get_next_num()
        add_tile("any")
    output()
    run()


def run():
    while running:
        key_control()


board = [[-3 for i in range(4)]for j in range(4)]


def output():
    print("\n" * 3)
    for i, array in enumerate(board):
        for j, tile in enumerate(array):
            print("%4s" % turn(tile), end="    ")
        print("\n")
        get_next_num()
    if stage <= 0:
        print("下一个数是:" + turn(stage))
    else:
        print("下一个数是:" + " ".join(turn(k)for k in stage_array))


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


def end_game():
    if is_end():
        print("动不了了")
        score()


def score():
    sum_score = 0
    for i in board:
        for j in i:
            if j >= 0:
                sum_score += 3 ** (j + 1)
    print("您的得分:" + str(sum_score))


def key_control():
    global running
    keyboard.add_hotkey(30, move_left)
    keyboard.add_hotkey(31, move_down)
    keyboard.add_hotkey(32, move_right)
    keyboard.add_hotkey(17, move_up)
    keyboard.wait()


if __name__ == "__main__":
    main()
