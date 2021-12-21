# adventOfCode 2021 day 18
# https://adventofcode.com/2021/day/18

import sys
import math  # for floor, ceil, prod functions
# import re

class SnailfishNumber:
    def __init__(self, in_str):
        self.sfnum = in_str

    def display(self):
        print(self.sfnum)

    def add(self, other_sfnum):
        # safety check
        # if other_sfnum is not SnailfishNumber:
        if not isinstance(other_sfnum, SnailfishNumber):
            sys.exit('cannot add other objects to a S.F.Number')
        self.sfnum = '[' + self.sfnum + ',' + other_sfnum.sfnum + ']'

# (element if isinstance(element, int) else element.get_magnitude())

    def get_magnitude(self):
        return 0

    # This function explodes a pair that starts at index i
    # This assumes that the string starting at i will be
    # opening bracket number 1, comma, number 2, closing bracket
    def do_explosion(self, i, j):
        # get numbers in the pair that will be exploded
        [n1, n2] = self.sfnum[i+1:j].split(',')
        [n1, n2] = [int(n1), int(n2)]
        left_string = self.sfnum[:i]
        right_string = self.sfnum[j+1:]

        # seek last number in left_string (if found, add n1)
        for index_last in range(i-1,-1,-1):
            if left_string[index_last].isdigit():
                for index_first in range(index_last,-1,-1):
                    if not left_string[index_first].isdigit():
                        old_value = int(left_string[index_first+1:index_last+1])
                        left_string = left_string[0:index_first+1] + \
                        str(old_value + n1) + left_string[index_last+1:]
                        break # break out of inner for loop
                break # break out of outer for loop

        # seek first number in right string (if found add n2)
        for index_first in range(0,len(right_string)):
            if right_string[index_first].isdigit():
                for index_last in range(index_first,len(right_string)):
                    if not right_string[index_last].isdigit():
                        old_value = int(right_string[index_first:index_last])
                        right_string = right_string[0:index_first] + \
                        str(old_value + n2) + right_string[index_last:]
                        break
                break
        
        # assemble the pieces together
        self.sfnum = left_string + '0' + right_string
        # end of method do_explosion

    # This function looks if an explosion is needed
    # If one is needed, it calls do_explosion
    # It assumes that the pair to be exploded is 
    # opening bracket number 1, comma, number 2, closing bracket
    def seek_explosion(self):
        level = 0
        for i, ch in enumerate(self.sfnum):                
            if ch == '[':
                level += 1
                if level == 5:
                    j = self.sfnum.find(']', i)
                    self.do_explosion(i,j)
                    return True
            elif ch == ']':
                level -= 1
        return False

    def split(self):
        # search for a pair of adjacent digits
        for i in range(len(self.sfnum)-1):
            if self.sfnum[i].isdigit() and self.sfnum[i+1].isdigit():
                # pair of digits found .... fail hard if there is a third out there 
                # (the next char should either be a comma or a close bracket)
                if i+2 >= len(self.sfnum) or self.sfnum[i+2].isdigit():
                    sys.exit('bad char after two digit number!')

                # determine the three pieces to assemble when the split is complete
                left_str = self.sfnum[:i]
                # determine new mid_str ...
                old_int = int(self.sfnum[i]+self.sfnum[i+1])
                mid_str = '[' + str(math.floor(old_int/2)) + ',' + str(math.ceil(old_int/2)) + ']'
                right_str = self.sfnum[i+2:]
                self.sfnum = left_str + mid_str + right_str
                # inform calling program that a split occured
                return True
        # inform calling program that no split occured
        return False

    def reduce(self):
        while True:
            if self.seek_explosion():
                continue # explosion occured, so repeat this function
            if self.split():
                continue # a split occured, so repeat this function
            return # finished reduction

    # this assumes that the number has been reduced
    # (therefore all numbers are single digit integers)
    def get_magnitude(self):
        ret_val = 0
        multiplier_list = []
        for ch in self.sfnum:
            if ch == '[':
                multiplier_list.append(3)
            elif ch == ',':
                multiplier_list.pop()
                multiplier_list.append(2)
            elif ch == ']':
                multiplier_list.pop()
            elif ch.isdigit():
                ret_val += int(ch) * math.prod(multiplier_list)
        
        # debug only
        # print('for snail number ', end='')
        # print(self.sfnum, end=' ... ')
        # print(ret_val)
        
        return ret_val

# end of definition of Class SnailfishNumber


# reading input from the input file
input_filename='input.txt'
with open(input_filename) as f:

    # read the first line into a sf number
    n1 = SnailfishNumber(f.readline().rstrip())

    print()
    print()

    # read each subsequent line into sf numbers:
    for in_string in f:
        # print(in_string.rstrip())
        n2 = SnailfishNumber(in_string.rstrip())
        n1.add(n2)
        n1.reduce()

print('The final snailfish number is: ', end='')
n1.display()    

print('The magnitude of the final snailfish number is: ', end='')
print(n1.get_magnitude())
print()



# n1 = SnailfishNumber('[1,2]')
# n2 = SnailfishNumber('[[3,4],5]')
# n1.add(n2)
# n1.display()


# sn = SnailfishNumber('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
# sn.display()
# sn.seek_explosion()
# sn.display()

# sn = SnailfishNumber('[10,1]')
# sn.split()
# sn.display()

# sn1 = SnailfishNumber('[[[[4,3],4],4],[7,[[8,4],9]]]')
# sn2 = SnailfishNumber('[1,1]')
# sn1.add(sn2)
# sn1.reduce()
# sn1.display()

# print( SnailfishNumber('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').get_magnitude() )

# print(SnailfishNumber([]).get_magnitude())
# print(SnailfishNumber([]).get_magnitude())
# print(SnailfishNumber([]).get_magnitude())
# print(SnailfishNumber([]).get_magnitude())
# print(SnailfishNumber([]).get_magnitude())
# print(SnailfishNumber([]).get_magnitude())
