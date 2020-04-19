import random

OUTPUT_FUNC = print
INPUT_FUNC = input


class Board(object):
    def __init__(self):
        self.board = ['' for i in range(24)]

    def get_board(self):
        return self.board

    def start_board(self, obj1, obj2):
        self.board[0] = 2 * obj1
        self.board[5] = 5 * obj2
        self.board[7] = 3 * obj2
        self.board[11] = 5 * obj1
        self.board[12] = 5 * obj2
        self.board[16] = 3 * obj1
        self.board[18] = 5 * obj1
        self.board[23] = 2 * obj2

    def change_board(self, index1, steps, obj):
        a = change_val_in_board(self.board, index1, steps, obj)
        if a is False:
            return False
        self.board = a


class Player(object):
    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def get_obj(self):
        return self.obj

    def get_name(self):
        return self.name


class Game(object):
    def __init__(self, player1, player2, board):
        self.p1 = player1
        self.p2 = player2
        self.board = board
        self.i = -1
        self.val_cube = 0

    def player_now(self):
        self.i = self.i + 1
        if self.i % 2 == 0:
            return "player1"
        return "player2"

    def get_val_cubes(self):
        self.val_cube = rolling_the_cubes()
        return self.val_cube

    def check_user_step(self, user_step):
        return check_steps(self.val_cube, user_step)

    def user_move(self, index_now, steps, obj):
        val_func = change_val_in_board(self.board, index_now, steps, obj)
        if val_func is False:
            return False  # cant make this move
        self.board = val_func
        return True  # The move was approved. The board has changed


class Field(Game):
    def __init__(self):
       pass ##To be continued

def rolling_the_cubes():
    num1 = random.randint(1, 6)
    num2 = random.randint(1, 6)
    return num1, num2


def change_val_in_board(board, index_now, steps, obj):
    if (obj in board[index_now] and (board[index_now + steps] == '' or obj in (board[index_now + steps]))):
        board[index_now] = board[index_now][:-1]
        board[index_now + steps] = board[index_now + steps] + obj
    else:
        return False
    return board


def check_steps(val_cubes, step):
    if val_cubes[0] != val_cubes[1]:  # if is not double
        if step == val_cubes[0]:
            val_cubes = val_cubes[1:]
        elif step == val_cubes[1]:
            val_cubes = val_cubes[:-1]
        elif step == sum(val_cubes):
            val_cubes = ()
        else:
            return False
    else:
        val_cubes = 2 * val_cubes
        k = val_cubes[0]
        v = sum(val_cubes) / val_cubes[0]
        if step == k and v > 0:
            val_cubes = val_cubes[:-1]
        elif step == 2 * k and v > 1:
            val_cubes = val_cubes[:-2]
        elif step == 3 * k and v > 2:
            val_cubes = val_cubes[:-3]
        elif step == 4 * k and v > 3:
            val_cubes = val_cubes[:-4]
        else:
            return False
    return val_cubes




def print_str_board(board):
    print(board)
    asterisk_arr = ['*' for i in range(26)]
    print(*asterisk_arr[:13])
    print_first_half_board(board[:12])
    print_second_half_board(board[12:])
    print(*asterisk_arr[13:])


def get_len(arr):
    max_l = len(arr[0])
    for i in arr[1:]:
        max_l = max(len(i), max_l)
    return max_l


def print_first_half_board(board):
    len_max = get_len(board)
    for j in range(len_max):
        print(" ", end=" ")
        for i in range(len(board)):
            if i == 6: print('|', end=" ")
            try:
                print(board[i][j], end=" ")
            except:
                print(" ", end=" ")
        print("\n")


def print_second_half_board(board):
    len_max = get_len(board)
    for j in range(len_max, -1, -1):
        for i in range(len(board), -1, -1):
            if i == 5: print('|', end=" ")
            try:
                print(board[i][j], end=" ")
            except:
                print(" ", end=" ")
        print("\n")


if __name__ == '__main__':
    b = Board()
    b.start_board("@", "#")
    # print(b.change_board(0, 11, "#"))
    # print(b.get_board())
    # a = input_from_user()
