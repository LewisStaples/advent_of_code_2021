# adventOfCode 2021 day 14, part b
# https://adventofcode.com/2021/day/14

import copy
import collections
import enum

# this is used with function apply_n_steps_to_polymer
# it is used to choose the return type
# (either get a list of all characters, or get a collection of counts of character frequency)
class Type_of_return(enum.Enum):
    LIST_OF_CHAR = 0
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

    # this returns the list of characters (the polymer's structure)
    def get_polymer(self):
        return self.polymer

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

    # this gets counts of each character in the polymer list
    def get_counts(self, polymer):
        cnt = collections.Counter()
        for ch in polymer:
            cnt[ch] += 1
        return cnt

    # for part b, this function takes an initial polymer and runs
    # n_steps steps on it.
    # the function return_type indicates what will be returned
    # either the list of i
    # listing counts of all polymers in polymer
    def apply_n_steps_to_polymer(self, polymer, n_steps, return_type):
        # for each step
        for step in range(1,n_steps+1):
            # create a new polymer starting with the first char/element of the old one
            new_polymer = [polymer[0]]
            # alternate between insert and copying the next char/element from the old one
            for i in range(1,len(polymer)):
                new_polymer.append(self.insertion_rule[''.join(polymer[i-1:i+1])])
                new_polymer.append(polymer[i])
            # finally point towards the newly created polymer
            polymer = new_polymer

        if return_type == Type_of_return.LIST_OF_CHAR:
            return polymer
        if return_type == Type_of_return.COLLECTIONS_COUNTER:
            return self.get_counts(polymer)

    # this function starts the processing to solve part b
    def solve_part_b(self):
        # go through all pairs of elements given as starting points in the insertion rules and develop 
        # the polymer after 20 steps ... only keep the character (element) counts
        for pair in self.insertion_rule:
            self.pair_to_polymer_after_20_runs[pair] = \
            self.apply_n_steps_to_polymer(pair , 20, Type_of_return.COLLECTIONS_COUNTER)

        # use the given input and determine what happens after 20 steps
        result_from_first_20_runs = \
            self.apply_n_steps_to_polymer(polymer.get_polymer() , 20, Type_of_return.LIST_OF_CHAR)

        # go through all pairs from the output from running 20 steps on the input
        # for each pair, add counts from the insertion rule counts
        cnt = collections.Counter()
        for i in range(len(result_from_first_20_runs)-1):
            char_pair = ''.join(result_from_first_20_runs[i:i+2])
            cnt += self.pair_to_polymer_after_20_runs[char_pair]

        # the above is correct, except that all letters (except first and last)
        # are counted twice, therefore remove those from the counts
        adjust_list = result_from_first_20_runs
        adjust_list.pop(0)
        adjust_list.pop()
        cnt -= collections.Counter(adjust_list)

        print('The solution to part b is ', end='')
        print(cnt.most_common()[0][1] - cnt.most_common()[-1][1])
        print()

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

polymer.solve_part_b()
print()
