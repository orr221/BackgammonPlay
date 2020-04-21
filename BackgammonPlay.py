import random


# -------------------------------------------------
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

    def change_board(self, index_now, steps, sign):
        try:
            if (sign in self.board[index_now] and (
                    self.board[index_now + steps] == '' or sign in (self.board[index_now + steps]))):
                self.board[index_now] = self.board[index_now][:-1]
                self.board[index_now + steps] = self.board[index_now + steps] + sign
            else:
                return False
        except IndexError:
            return False

    def change_board_level_2(self, index):
        # get valid input
        self.board[index] = self.board[index][:-1]


# ---------------------------------------

class Player(object):
    def __init__(self, sign, name):
        self.sign = sign
        self.name = name

    def get_sign(self):
        return self.sign

    def get_name(self):
        return self.name


# --------------------------------------------
class Game(object):
    def __init__(self, player1, player2, board):
        self.p1 = player1
        self.p2 = player2
        self.board = board
        self.count = -1
        self.val_cube = 0

    def player_now(self):
        self.count = self.count + 1
        if self.count % 2 == 0:
            return self.p1
        return self.p2

    def rolling_the_cubes(self):
        num1 = random.randint(1, 6)
        num2 = random.randint(1, 6)
        self.val_cube = num1, num2
        return self.val_cube

    def check_user_step(self, user_step):
        return check_steps(self.val_cube, user_step)

    def user_move(self, index_now, steps, sign):
        val_func = self.board.change_board(index_now, steps, sign)
        if val_func is False:
            return False  # cant make this move
        return True  # The move was approved. The board has changed


# ----------------------------------

class Specific_Field(Game):
    pass

    def print_board(self):
        print_str_board(self.board.get_board())

    def move(self, player_now):
        self.val_cube = self.rolling_the_cubes()
        dic_val_cubes = dict_val_cubes(self.val_cube)
        print("cubes is: {val}. \n{name} please enter your move".format(name=player.get_name(), val=self.val_cube))
        index, step = self.get_move_from_user(player, dic_val_cubes)
        self.make_move(index, step, player)

    def make_move(self, index, step, player):
        sign = player.get_sign()
        dict_cubes = dict_val_cubes(self.val_cube)
        dict_cubes = change_dict_val_cubes(dict_cubes, step)
        while (sum(list(dict_cubes.values())) > 0):
            index, step = self.get_move_from_user(player, dict_cubes)
            dict_cubes = change_dict_val_cubes(dict_cubes, step)

    def get_move_from_user(self, player, dic_val_cubes):
        sign = player.get_sign()
        while (True):
            index = input("index: ")
            step = self.legal_step(dic_val_cubes)
            if player == self.p1:  # Player 1 moves clockwise
                move = self.user_move(int(index), int(step), sign)
            else:  # Player 2 moves counterclockwise
                move = self.user_move(int(index), int(-step), sign)
            if move is False:
                print("Invalid move")
            else:
                self.print_board()
                return int(index), int(step)

    def legal_step(self, dic_val_cubes):
        while (True):
            step = int(input("step: "))
            valid_step = check_steps(dic_val_cubes, step)
            if valid_step is False:
                print("The step is not possible")
            else:
                return step

    def level(self, player_now):
        if player_now is p1:
            if (p1.get_sign() not in self.board[:-6]):
                return 2  # level 2
            return 1  # level 1
        if (p2.get_sign() not in self.board[6:]):
            return 2
        return 1

    def play_level_2(self, index, step, player_now):
        step=step-1
        if player_now is p2:
            if ((index == step and p2.get_sign() in self.board.get_board()[index]) or (
                    index < step and p2.get_sign() not in self.board.get_board()[index:6])):
                self.board.change_board_level_2(index)
                return True
            if index > step and p2.get_sign() in self.board.get_board()[index]:
                self.board.change_board(index, -(step+1), player_now.get_sign())

        elif ((abs(index - 23) == step and p1.get_sign() in self.board.get_board()[index]) or (
                (abs(index - 23) + 1) < step and p1.get_sign() not in self.board.get_board()[18:index])):
            self.board.change_board_level_2(index)
            return True
        if abs(index - 23) > step and p1.get_sign() in self.board.get_board()[index]:
            self.board.change_board(index, (step+1), p1.get_sign())
            return True

        return False


# ---------------------------------------------------


def change_dict_val_cubes(dict_cubes, step):
    if len(dict_cubes.keys()) > 1:
        try:
            dict_cubes[step]
            dict_cubes[step] = 0
        except KeyError:
            for i in list(dict_cubes.keys()):
                dict_cubes[i] = 0
    else:
        print(dict_cubes)
        val = list(dict_cubes.keys())[0]
        dict_cubes[val] = dict_cubes[val] - int(step / val)
        print(dict_cubes)
    return dict_cubes


def dict_val_cubes(val_cubes):
    if val_cubes[0] != val_cubes[1]:
        dict_cubes = {val_cubes[0]: 1, val_cubes[1]: 1}
    else:
        dict_cubes = {val_cubes[0]: 4}
    return dict_cubes


def check_steps_regular(dict_cubes, step):
    if step in dict_cubes and dict_cubes[step] != 0:
        return True
    if step == sum(dict_cubes) and sum(list(dict_cubes.values())) == 2:
        return True
    return False


def check_steps_when_double(dict_cubes, step):
    val = int(list(dict_cubes.keys())[0])
    if step == val and dict_cubes[step] != 0:
        return True
    if step % val == 0:
        n = int(step / val)
        if n in range(1, dict_cubes[val] + 1):
            return True
    return False


def check_steps(dic_val_cubes, step):
    if len(dic_val_cubes) > 1:
        return check_steps_regular(dic_val_cubes, step)
    else:
        return check_steps_when_double(dic_val_cubes, step)


def print_str_board(board):
    asterisk_arr = ['*' for i in range(26)]
    print(" ", end=" ")
    print(*asterisk_arr[:13])
    print_first_half_board(board[:12])
    print_second_half_board(board[12:])
    print(" ", end=" ")
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


# ________________________________________________________

# def play_game(s):
#     player = s.player_now()
#     while(s.level()
#


if __name__ == '__main__':
    b = Board()
    b.start_board("@", "#")
    # print(b.change_board(0, 11, "#"))
    # print(b.get_board())
    # a = input_from_user()
    p1 = Player("@", "Orr")
    p2 = Player("#", "Yohai")
    s = Specific_Field(p1, p2, b)
    # player = s.player_now()
    # while(player.get_sign in s.board):
