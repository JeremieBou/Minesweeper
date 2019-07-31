from random import random
import datetime

DIRECTIONS = [
    (-1, 0),   #up
    (1, 0),    #down
    (0, -1),   #left
    (0, 1),    #right
    (1, 1),    #bottom right
    (-1, -1),  #top left
    (1, -1),   #bottom left
    (-1, 1),   #top right
]

DEFAULT_GAME_VAL = "H"


class Board:
    board = []
    width = 0
    height = 0

    def get_value(self, col, row):
        if 0 <= col < self.width and 0 <= row < self.height:
            return self.board[row][col]
        else:
            return None

    def set_value(self, col, row, value):
        if 0 <= col < self.width and 0 <= row < self.height:
            self.board[row][col] = value
        else:
            raise Exception("Invalid coordinates")

    def make_blank_board(self, width, height, default_value = "0"):
        self.width = width
        self.height = height
        self.board = [[default_value] * width for _ in range(height)]

    def pad_spaces(self, string, desired_length):
        string += " " * (desired_length - len(string))
        return string

    def __repr__(self):
        output_builder = []


        header_row = ["     "]

        for i in range(len(self.board[0])):
            col_name = self.pad_spaces(str(i + 1), 3)

            header_row.append(col_name)
        row_separator = "-"*(len(header_row)*4)
        output_builder.append(" ".join(header_row))
        output_builder.append(row_separator)


        for i in range(len(self.board)):
            row_name = self.pad_spaces(str(i + 1), 3) + "| "

            row_builder = [row_name]
            for j in range(len(self.board[i])):
                cell_value = self.pad_spaces(str(self.board[i][j]), 3)
                row_builder.append(cell_value)

            output_builder.append((" ".join(row_builder)))
            output_builder.append(row_separator)

        return "\n".join(output_builder)

class GameBoard(Board):
    mine_board = []

    def __init__(self, mine_board):
        #we'll derive the game board from the mine board
        if not isinstance(mine_board, MineBoard):
            raise Exception("Must use a valid MineBoard as custructor parameter")

        self.mine_board = mine_board
        self.make_blank_board(mine_board.width, mine_board.height,
                              default_value=DEFAULT_GAME_VAL)

    def reveal_mines(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.mine_board.get_value(i, j) == 'm':
                    self.set_value(i, j, "X")

    def reveal_area(self, col, row):
        stack = [(col, row)]

        while stack:
            pcol, prow = stack.pop()

            val = self.mine_board.get_value(pcol, prow)

            if val != 'm' and val != None:
                self.set_value(pcol, prow, val)

            if val == "0":
                for direction in DIRECTIONS:
                    new_col = pcol + direction[0]
                    new_row = prow + direction[1]

                    if self.get_value(new_col, new_row) == DEFAULT_GAME_VAL:
                        stack.append((new_col, new_row))


    def check_finished(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.get_value(i, j) == "H" \
                    and self.mine_board.get_value(i, j) != 'm':
                    return False

        return True


    def check_value(self, col, row):
        value = self.mine_board.get_value(col, row)

        if value == None:
            raise Exception("invalid col/row combination")
        elif value == 'm':
            self.reveal_mines()
            return False
        elif value == "0":
            self.reveal_area(col, row)
            return True
        else:
            self.set_value(col, row, value)
            return True



class MineBoard(Board):
    def __init__(self, width, height, density):
        if not isinstance(width, int) or width <= 0:
            raise Exception("Width must be an integer bigger than 0")

        if not isinstance(height, int) or height <= 0:
            raise Exception("Height must be an integer bigger than 0")

        if not isinstance(density, float) or density < 0 or density > 1:
            raise Exception("Density must be float and a probability")

        self.generate_board(width, height, density)


    def populate_mines(self, density):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                r = random()

                if r >= (1 - density):
                    self.set_value(i, j, 'm')


    def populate_hints(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                mines = 0

                if self.get_value(i, j) == 'm':
                    continue

                for direction in DIRECTIONS:
                    dir_mines = self.get_value(i + direction[0], j + direction[1])
                    if dir_mines == 'm':
                        mines += 1

                self.set_value(i, j, str(mines))



    def generate_board(self, width, height, density):
        self.make_blank_board(width, height)
        self.populate_mines(density)
        self.populate_hints()


def do_setup():
    print("Welcome to mine sweeper!")
    print("Available difficulties:")
    print("(b) - baby mode")
    print("(e) - easy")
    print("(m) - medium")
    print("(h) - hard")
    print("(x) - extreme")
    print("(g) - good luck")
    print("(i) - impossible")
    difficulty = input("Please pick a difficulty (b/e/m/h/x/g/i): ")

    if difficulty == 'b':
        return MineBoard(5, 5, 0.1)
    elif difficulty == 'e':
        return MineBoard(10, 10, 0.1)
    elif difficulty == "m":
        return MineBoard(20, 20, 0.13)
    elif difficulty == "h":
        return MineBoard(25, 25, 0.2)
    elif difficulty == "x":
        return MineBoard(30, 25, 0.4)
    elif difficulty == "g":
        return MineBoard(40, 25, 0.7)
    elif difficulty == "i":
        return MineBoard(50, 25, 0.99)
    else:
        print("Invalid difficulty")
        return do_setup()



def do_turn():
    col = input("Input column: ")
    row = input("Input row: ")

    try:
        state = game_board.check_value(int(col) - 1, int(row) - 1)
        print(game_board)
        print("\n\n")

        if state and game_board.check_finished():
            return 2
        else:
            return 1 if state else 0
    except:
        print("Invalid column/row pair")
        return do_turn()


if __name__ == "__main__":
    mine_board = do_setup()
    game_board = GameBoard(mine_board)
    state = 1

    start_time = datetime.datetime.now()

    print(game_board)

    while state == 1:
        state = do_turn()

    if state == 0:
        print("Game Over, please try again")
    elif state == 2:
        end_time = datetime.datetime.now()


        print("You won! Your final time is {}".format(end_time - start_time))
