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
            # print(char + ': ', end='')
            # print(self.polymer.count(char))
            count = self.polymer.count(char)
            if count < lowest_val:
                lowest_val = count
            if count > highest_val:
                highest_val = count
        return highest_val - lowest_val

    def solve_problem_a(self):
        # new_polymer = [self.polymer[0]]
        for step in range(1,11): # range needs a second parameter with total_steps + 1
            new_polymer = [self.polymer[0]]
            for i in range(1,len(self.polymer)):
                # dummy=1234
                # print(self.polymer[i])
                new_polymer.append(self.insertion_rule[''.join(self.polymer[i-1:i+1])])
                new_polymer.append(self.polymer[i])
                # new_polymer.a
                # print(self.polymer[i] + ', ' + self.polymer[i+1])
                # print(str(self.polymer[i:i+2]))
                # print(self.insertion_rule[''.join(self.polymer[i:i+2])])
                # self.polymer.insert(i, self.insertion_rule[''.join(self.polymer[i:i+2])])
            # print(self.polymer)
            # print(''.join(new_polymer))
            self.polymer = new_polymer

            # self.calc_quantity()

            # print()
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
polymer.input_from_file('input_sample0.txt')

polymer.solve_problem_a()


