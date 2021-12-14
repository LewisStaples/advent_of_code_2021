# adventOfCode 2021 day 13
# https://adventofcode.com/2021/day/13

class Paper_Dots:
    def __init__(self):
        # this will be a set of 2-member tuples of integers, showing the coordinates
        self.dot_set = set()  # []

        # this will be a list of 2-member lists containing a str and an int
        self.fold_instructions = []

    # this function reads input from the file named in the function parameter
    def input(self, input_filename):
        # reading input from the input file
        with open(input_filename) as f:
            # pull in each line from the input file
            for in_string in f:
                # input a pair of numbers into self.dot_set
                if ',' in in_string:
                    self.dot_set.add((
                        int(in_string.split(',')[0]),
                        int(in_string.split(',')[1])
                        ))
                # input a character and a number into self.fold_instructions
                if '=' in in_string:
                    in_string = in_string.replace('fold along','')
                    [left, right] = in_string.split('=')
                    self.fold_instructions.append([left.strip(), int(right)])
    
    # this function (for testing) displays the contents of the list of dots
    # and the list of folding instructions
    def display_lists(self):
        for i in self.dot_set:
            print(i)
        for i in self.fold_instructions:
            print(i)

    # this function performs a single fold
    # it also prints the number of dots
    def do_fold(self):

        [axis,value] = self.fold_instructions[0]

        old_dot_set =  self.dot_set
        new_dot_set = set()
        # go through the old set of dots, one dot at a time
        for [x,y] in old_dot_set:
            # create a new set: new_dot_set
            if axis == 'y':
                if y > value:
                    y = 2 * value - y
            if axis == 'x':
                if x > value:
                    x = 2 * value - x
            
            new_dot_set.add((x,y))

        self.dot_set = new_dot_set

        print('Number of dots is: ', end='')
        print(len(self.dot_set))

input_filename='input.txt'
paper_dots = Paper_Dots()
paper_dots.input(input_filename)

paper_dots.do_fold()
