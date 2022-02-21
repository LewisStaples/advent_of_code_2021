# adventOfCode 2021 day 24 helper
# https://adventofcode.com/2021/day/24/helper.py

import copy

# The code below shows that all combinations lead to a fxn of zero
# max_val = float('-inf')
# min_val = float('inf')
# for i0 in range(9,0,-1):
#     for i1 in range(9,0,-1):
#         for i2 in range(9,0,-1):
#             for i3 in range(9,0,-1):
#                 for i7 in range(9,0,-1):
#                     for i8 in range(9,0,-1):
#                         for i12 in range(9,0,-1):
#                             fxn = i0//26 + 5//26 + i1//26**2 + 14//26**2 + i2//26**3 + 15//26**3 + i3//26**4 + 16//26**4 + i7//26**2 + 13//26**2 + i8//26**3 + 16//26**3 + i12//26 + 11//26
#                             min_val = min(fxn, min_val)
#                             max_val = max(fxn, max_val)
#                             # print(fxn)
# print('Min, max values for the ending value of z:')
# print(min_val)
# print(max_val)

def solve_problem(poss_digits):
    for i0 in poss_digits:
        for i1 in poss_digits:
            for i2 in poss_digits:
                for i3 in poss_digits:
                    z0 = i0 + 5
                    z1 = 26*z0 + i1 + 14
                    z2 = 26*z1 + i2 + 15
                    z3 = 26*z2 + i3 + 16

                    i4 = z3%26 - 16

                    z4 = z3//26
                    i5 = z4%26 - 11

                    z5 = z4//26
                    i6 = z5%26 - 6

                    if (i4 not in poss_digits) \
                        or (i5 not in poss_digits) \
                        or (i6 not in poss_digits):
                        break

                    z6 = z5//26 
                    for i7 in poss_digits:
                        z7 = 26*z6 + i7 + 13
                        for i8 in poss_digits:
                            z8 = 26*z7 + i8 + 16
                            z9 = z8//26
                            i9 = z8%26 - 10
                            if i9 not in poss_digits:
                                continue

                            z10 = z9//26
                            i10 = z9%26 - 8
                            if i10 not in poss_digits:
                                continue
                            z11 = z10//26
                            i11 = z10%26 - 11
                            if i11 not in poss_digits:
                                continue
                            for i12 in poss_digits:
                                z12 = 26*z11 + i12 + 11
                                i13 = z12%26 - 15
                                if i13 not in poss_digits:
                                    continue
                                z13 = z12//26 # superfluous (since it's already known)
                                # that all combinations lead to z13 of zero)

                                # print solution to screen
                                print('The solution is: ', end='')
                                for i in range(14):
                                    print(eval('i'+str(i)), end='')

                                print()
                                return

poss_digits_forward = [1,2,3,4,5,6,7,8,9]
poss_digits_backward = copy.deepcopy(poss_digits_forward)
poss_digits_backward.reverse()

print('For part A:')
solve_problem(poss_digits_backward)
print('For part B:')
solve_problem(poss_digits_forward)

