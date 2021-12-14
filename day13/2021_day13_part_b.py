# adventOfCode 2021 day 13
# https://adventofcode.com/2021/day/13

# this class implements behavior of the dots
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
            # pull in each line from the input fil
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

    # this function displays all dots as a grid of dots
    # this can only be run with small grids, like input_sample0.txt , 
    # or for input.txt for part b (after all of the folds)
    # the input is a tuple of the sizes of axes
    def display_dots_in_grid(self, max_axes):
        dot_count = 0

        # initialize conversion of data to array
        array_to_display = []
        # for j in range(6):
        for j in range(max_axes[1]+1):
            line = []
            # for i in range(39):
            for i in range(max_axes[0]+1):
                line.append('.')
            array_to_display.append(line)

        # copy dot_set's data to the array
        for [j,i] in self.dot_set:
            array_to_display[i][j] = '#'
            dot_count += 1

        # do the display from the array
        for line in array_to_display:
            for ch in line:
                print(ch, end='')
            print()
        print()
        print()

    # this function performs all folds
    # it also prints the number of dots
    def do_folds(self):
        for [axis,value] in self.fold_instructions:
            old_dot_set =  self.dot_set
            new_dot_set = set()
            for [x,y] in old_dot_set:
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

    # this function returns the maximum values of x and y
    # def print_ranges(self):
    def return_ranges(self):
        x_max = 0
        y_max = 0
        for pair in self.dot_set:
            x_max = max(x_max, pair[0])
            y_max = max(y_max, pair[1])
        return (x_max, y_max)

input_filename='input.txt'
paper_dots = Paper_Dots()
paper_dots.input(input_filename)

paper_dots.do_folds()

print()
paper_dots.display_dots_in_grid( paper_dots.return_ranges() )
