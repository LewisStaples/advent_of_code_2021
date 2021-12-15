# adventOfCode 2021 day 14, part b
# https://adventofcode.com/2021/day/14

import copy
import collections
import enum

class Type_of_return(enum.Enum):
    LIST_OF_INT = 0
    COLLECTIONS_COUNTER = 1

class Polymer:
    def __init__(self):
        # this list of characters (each is a single "element") shows the polymer
        self.polymer = []

        # this is a set of all characters that could be in the polymer
        self.polymer_characters = set()
        
        # this dict stores all insertion rules (in computer memory)
        self.insertion_rule = {}

        # this dict is for part b only
        # the index is the initial pair of polymers, stored as a list   ??? string vs. tuple ???
        # the value is another dict with counts of all polymers after 20 runs
        # agains the pair in the index
        self.pair_to_polymer_after_20_runs = {}

    def get_polymer(self):
        return self.polymer

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
    def calc_quantity(self, polymer):
        lowest_val = float('inf')
        highest_val = 0
        for char in self.polymer_characters:
            # print(char + ': ', end='')
            # print(polymer.count(char))
            count = polymer.count(char)
            if count < lowest_val:
                lowest_val = count
            if count > highest_val:
                highest_val = count
        return highest_val - lowest_val

    def get_counts(self, polymer):
        cnt = collections.Counter()
        for ch in polymer:
            cnt[ch] += 1
        return cnt

    # for part b, this function returns a ????
    # listing counts of all polymers in polymer
    # use  https://docs.python.org/3/library/collections.html#counter-objects
    def apply_n_steps_to_polymer(self, polymer, n_steps, return_type):
        for step in range(1,n_steps+1): # range needs a second parameter with total_steps + 1
            new_polymer = [polymer[0]]
            for i in range(1,len(polymer)):
                new_polymer.append(self.insertion_rule[''.join(polymer[i-1:i+1])])
                new_polymer.append(polymer[i])
            polymer = new_polymer

        if return_type == Type_of_return.LIST_OF_INT:
            return polymer
        if return_type == Type_of_return.COLLECTIONS_COUNTER:
            return self.get_counts(polymer)
        # print('the answer to part a is ', end='')
        # print(self.calc_quantity(polymer))
        # return self.calc_quantity(new_polymer)

    def solve_part_b(self):
        for pair in self.insertion_rule:
            # dummy = 123
            # print(pair)
            self.pair_to_polymer_after_20_runs[pair] = \
            self.apply_n_steps_to_polymer(pair , 20, Type_of_return.COLLECTIONS_COUNTER)

        result_from_first_20_runs = \
            self.apply_n_steps_to_polymer(polymer.get_polymer() , 20, Type_of_return.LIST_OF_INT)

        cnt = collections.Counter()

        for i in range(len(result_from_first_20_runs)-1):
            char_pair = ''.join(result_from_first_20_runs[i:i+2])
            cnt += self.pair_to_polymer_after_20_runs[char_pair]

        # the above is correct, except that all letters from index 1 through -1
        # are counted twice, therefore, 
        adjust_list = result_from_first_20_runs
        adjust_list.pop(0)
        adjust_list.pop()
        cnt -= collections.Counter(adjust_list)

        print(cnt)

        print('The solution to part b is ', end='')
        print(cnt.most_common()[0][1] - cnt.most_common()[-1][1])
        print()

        # print(self.apply_n_steps_to_polymer(polymer.get_polymer() , 10)[0][1])
        # print(self.apply_n_steps_to_polymer(polymer.get_polymer() , 10)[-1][1])
        # print('The solution to part b is ', end='')
        # print(
        # self.apply_n_steps_to_polymer(polymer.get_polymer() , 10)[0][1] -
        # self.apply_n_steps_to_polymer(polymer.get_polymer() , 10)[-1][1]
        # )

# this is a free-standing function (it's not in any class)
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

# polymer.apply_n_steps_to_polymer(polymer.get_polymer() , 20)

polymer.solve_part_b()
print()
