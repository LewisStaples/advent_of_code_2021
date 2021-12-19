# adventOfCode 2021 day 18
# https://adventofcode.com/2021/day/18

# class SFN_Pair:

import sys

class Node:
    def __init__(self, parentNode):
        self.values = []
        if parentNode is not None:
            self.parent = parentNode
            self.parent.child = self

    def get_magnitude(self):
        mult_factor = [3,2]
        ret_val = 0
        for index in range(0,2):
            element = self.values[index]
            ret_val += mult_factor[index] * (element if isinstance(element, int) else element.get_magnitude())
        return ret_val

    def explode(self, levels=1):
        ret_val = 0
        if levels == 4:
            for i, value in enumerate(self.values):
                if value is Node:
                    i_change = (i + 1) % 2
                    self.values[i_change] += value.values[i_change]
                    value = 0
                    return 1

        for value in self.values:
            if value is Node:
                ret_val += value.explode(levels+1)
        return ret_val

    def split(self):
        ret_val = 0
        for value in self.values:
            if isinstance(value, int):
                if value > 9:
                    # do something neat-o !!!!!!!!!!!!!!!!!!!!
                    return 1
            elif value is Node:
                ret_val += self.split()

        return ret_val
# end of class Node

class SnailfishNumber:
    def __init__(self, snnum_string):
        print(snnum_string)
        print()
        self.root = Node(None)
        pointer = self.root
        for char in snnum_string[1:-1]:
            if char == '[':
                pointer.values.append(Node(pointer))
                pointer = pointer.values[-1]
            elif char == ']':
                pointer = pointer.parent
            elif char.isdigit():
                if len(pointer.values) > 1:
                    sys.exit('Error!  Putting more than two values in a pair')
                pointer.values.append(int(char))
            
    def add(self, other_node):
        left_node = self.root
        self.root = Node(None)
        self.root.values.append(left_node)
        self.root.values.append(other_node)

    def get_magnitude(self):
        return self.root.get_magnitude()

    def explode(self):
        return self.root.explode()

    def split(self):
        return self.root.split()

    def reduce(self):
        while True:
            sum_ops = 0
            sum_ops += self.explode()
            sum_ops += self.split()
            if sum_ops == 0:
                break

# end of definition of Class SnailfishNumber

list_snailfish_number_strings = []

# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        # print(in_string.rstrip())
        list_snailfish_number_strings.append(in_string.rstrip())


# for sn_str in list_snailfish_number_strings:
#     print(sn_str)

# sfnum = SnailfishNumber(list_snailfish_number_strings[0])

# sfnum = SnailfishNumber('[[[[5,0],[7,4]],[5,5]],[6,6]]')
sfnum = SnailfishNumber('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]')
# sfnum = SnailfishNumber('')
# sfnum = SnailfishNumber('')
# sfnum = SnailfishNumber('')

# sfnum = SnailfishNumber('[[[[3,0],[5,3]],[4,4]],[5,5]]')

sfnum.reduce()
print(sfnum.get_magnitude())


