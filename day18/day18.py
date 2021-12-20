# adventOfCode 2021 day 18
# https://adventofcode.com/2021/day/18

import sys
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
        return

    def reduce(self):
        while True:
            if self.seek_explosion():
                continue # explosion occured, so repeat 
            self.split()
            return # finished reduction

# end of definition of Class SnailfishNumber

# n1 = SnailfishNumber('[1,2]')
# n2 = SnailfishNumber('[[3,4],5]')
# n1.add(n2)
# n1.display()


sn = SnailfishNumber('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
sn.display()
sn.seek_explosion()
sn.display()

# sn = SnailfishNumber('[[6,[5,[4,[3,2]]]],1]')
# sn.display()
# sn.seek_explosion()
# sn.display()


