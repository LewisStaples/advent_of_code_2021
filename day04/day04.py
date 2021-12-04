# adventOfCode 2021 day 4, parts 1
# https://adventofcode.com/2021/day/4

import sys
# this handles one specific Bingo board
class Bingo:
    def __init__(self):
        # this is a list of lists for the grid
        # at this time no rows imported yet from input file
        self.numbers = [] 

        # this is a list of 2-tuples of coordinates that are marked
        # at this time no numbers have been drawn yet, so none are marked
        self.marked = [] 

    def __str__(self):
        return str(self.numbers)

    def add_row(self, row_string):
        self.numbers.append([int(i) for i in row_string.rstrip().split()])

    def sum_unmarked(self):
        # first calculate total sum (marked and unmarked numbers)
        sum_unmarked=sum([sum(x) for x in self.numbers])

        # subtract all marked numbers
        for marked_coords in self.marked:
            # print(marked_coords, end=': ')
            # print(self.numbers)
            # print()
            # print(self.numbers[marked_coords[0]][marked_coords[1]])
            sum_unmarked -= self.numbers[marked_coords[0]][marked_coords[1]]
        
        # the result is the sum of all unmarked numbers
        return sum_unmarked

    def draw_number(self, drawn_number):
        for i_row, row in enumerate(self.numbers):
            for j_column, number in enumerate(row):
                if drawn_number == number:
                    self.marked.append((i_row, j_column))
                    # see if this new draw completes a win
                    winning_board = {'row': True, 'column': True}
                    for index in range(5):
                        if (i_row, index) not in self.marked:
                            winning_board['row'] = False
                        if (index, j_column) not in self.marked:
                            winning_board['column'] = False
                    if True in winning_board.values():
                        print('This board has won!')
                        print(self)
                        print()
                        print('winning drawn number: ', end='')
                        print(drawn_number)
                        print()
                        
                        sum_unmarked = self.sum_unmarked()

                        print('sum of undrawn numbers: ', end='')
                        print(sum_unmarked)

                        print('final score (answer to part a): ', end='')
                        print(sum_unmarked*drawn_number)
                        sys.exit()

        # print(self.marked)

class BingoBoardSet:
    def __init__(self):
        self.board_set = []
    
    def __str__(self):
        ret_str = 'START OF SET\n'
        for board in self.board_set:
            ret_str += str(board) + '\n'
        ret_str += 'END OF SET'
        return ret_str
        # return str(self.board_set)

    def add(self, new_board):
        self.board_set.append(new_board)

    def draw_number(self, drawn_number):
        for board in self.board_set:
            board.draw_number(drawn_number)
        # print()

# Task 1:  Input data

input_filename='input.txt'
number_draws = None
# bingo_board_set = set()
bingo_board_set = BingoBoardSet()

with open(input_filename) as f:
    number_draws = [int(i) for i in f.readline().rstrip().split(',')]
    bingo_board_being_created = None
    for line_num, in_string in enumerate(f):
        # print(line_num, end=': ')
        # print(in_string.rstrip())

    

        if line_num % 6 == 0:
        #     # start a new blank bingo board
            bingo_board_being_created = Bingo()
            # print()
        else:
        #     # add line to bingo 
            bingo_board_being_created.add_row(in_string)
        
        if line_num % 6 == 5:
            bingo_board_set.add(bingo_board_being_created)
            print(bingo_board_being_created)

print()
print(number_draws)
print()

# note that set does not retain any order
print(bingo_board_set)

for num_draw in number_draws:
    # print('Number drawn: ', end='')
    # print(num_draw)

    bingo_board_set.draw_number(num_draw)
    

