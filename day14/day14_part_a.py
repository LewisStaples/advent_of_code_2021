# adventOfCode 2021 day 14, part a
# https://adventofcode.com/2021/day/14

import copy

class Polymer:
    def __init__(self):
        # this list of characters (each is a single "element") shows the polymer
        self.polymer = []

        # this is a set of all characters that could be in the polymer
        self.polymer_characters = set()
        
        # this dict stores all insertion rules (in computer memory)
        self.insertion_rule = {}

    # this imports data from file
    def input_from_file(self, input_filename):
        insertion_rule_sign = ' -> '

        with open(input_filename) as f:
            # import polymer template
            in_string = f.readline().rstrip()
            self.polymer = [ch for ch in in_string]
            self.polymer_characters = {ch for ch in in_string}

            # import polymer pair insertion rules
            for in_string in f:
                in_string = in_string.rstrip()
                if insertion_rule_sign in in_string:
                    [left, right] = in_string.split(insertion_rule_sign)
                    self.insertion_rule[left] = right
                    self.polymer_characters.add(right)

    # this function solves the quantity for the number to be submitted
    # for part a of the problem = quantity_most - quantity_least
    def calc_quantity(self):
        lowest_val = float('inf')
        highest_val = 0
        for char in self.polymer_characters:
            count = self.polymer.count(char)
            if count < lowest_val:
                lowest_val = count
            if count > highest_val:
                highest_val = count
        return highest_val - lowest_val

    # for part a, this function takes an initial polymer and runs
    # 10 steps on it.
    # the function returns the desired quantity (from calc_quantity)
    def solve_problem_a(self):
        # for each step
        for step in range(1,11): # range needs a second parameter with total_steps + 1
            # create a new polymer starting with the first char/element of the old one
            new_polymer = [self.polymer[0]]
            # alternate between insert and copying the next char/element from the old one
            for i in range(1,len(self.polymer)):
                new_polymer.append(self.insertion_rule[''.join(self.polymer[i-1:i+1])])
                new_polymer.append(self.polymer[i])
            # finally point towards the newly created polymer
            self.polymer = new_polymer

        print('the answer to part a is ', end='')
        print(self.calc_quantity())

# this function determines the string length after 10 steps
# I do this, because I want to know if the length will be
# longer than what my computer can handle
#
# not called in part a code (although whether it might come in
# handy for part b is to be determined)
def display_length_results(length):
    print('initial length:           ', end='')
    print(length)
    for i in range(1,11):
        length += (length-1)
        print('length after step  ', end='')
        print(i, end=': ')
        print(length)

polymer = Polymer()

# read input from the input file
polymer.input_from_file('input.txt')

polymer.solve_problem_a()

