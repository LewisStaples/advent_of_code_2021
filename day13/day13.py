# adventOfCode 2021 day 13
# https://adventofcode.com/2021/day/13

class Paper_Dots:
    def __init__(self):
        # this will be a set of 2-member tuples of integers, showing the coordinates
        self.dot_set = set()  # []

        # this will be a list of 2-member lists containing a str and an int
        self.fold_instructions = []

    def input(self, input_filename):
        # reading input from the input file
        with open(input_filename) as f:
            # pull in each line from the input fil
            for in_string in f:
                # print(in_string.rstrip())
                if ',' in in_string:
                    self.dot_set.add((
                        # [int(x) for x in in_string.split(',')]
                        int(in_string.split(',')[0]),
                        int(in_string.split(',')[1])
                        ))
                if '=' in in_string:
                    in_string = in_string.replace('fold along','')
                    [left, right] = in_string.split('=')
                    self.fold_instructions.append([left.strip(), int(right)])
    
    def display_lists(self):
        for i in self.dot_set:
            print(i)
        for i in self.fold_instructions:
            print(i)

    # this can only be run with small grids, like input_sample0.txt !
    def display(self):
        dot_count = 0

        # initialize conversion of data to array
        array_to_display = []
        for j in range(6):
            line = []
            for i in range(39):
                line.append('.')
            array_to_display.append(line)

        # copy dot_set's data to the array
        for [j,i] in self.dot_set:
            array_to_display[i][j] = '#'
            dot_count += 1

        # do the display from the array
        print('Dot Count = ', end='')
        print(dot_count)
        for line in array_to_display:
            for ch in line:
                print(ch, end='')
            print()
        print()
        print()

    def do_folds(self):
        for [axis,value] in self.fold_instructions:
            # [axis,value] = self.fold_instructions[0]

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

    def print_ranges(self):
        x_max = 0
        y_max = 0
        for pair in self.dot_set:
            x_max = max(x_max, pair[0])
            y_max = max(y_max, pair[1])
        print('Ranges: ', end='')
        print(x_max, end='')
        print(', ', end='')
        print(y_max, end='')
        print()

input_filename='input.txt'
paper_dots = Paper_Dots()
paper_dots.input(input_filename)
paper_dots.print_ranges()
# paper_dots.display()

paper_dots.do_folds()
paper_dots.print_ranges()
print()
paper_dots.display()
