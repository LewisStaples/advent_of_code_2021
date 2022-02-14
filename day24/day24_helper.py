# adventOfCode 2021 day 24 helper
# https://adventofcode.com/2021/day/24/helper.py

max_val = float('-inf')
min_val = float('inf')

# The code below shows that all combinations lead to a fxn of zero

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


print('For part A:')
# If the seven inputs that impact the final z were all 9, several of the other inputs would not be in the range 1-9
# See below where this is the case.  Therefore, smaller inputs will be needed for some of those.

i0 = i1 = i2 = i3 = i4 = i5 = i6 = i7 = i8 = i9 = i10 = i11 = i12 = i13 = None

poss_input = [1,2,3,4,5,6,7,8,9]

for i0 in range(9,0,-1):
    for i1 in range(9,0,-1):
        for i2 in range(9,0,-1):
            for i3 in range(9,0,-1):
                z3 = 26^3*i0 + 26^3*5 + 26^2*i1 + 26^2*14 + 26*i2 + 26*15 + i3 + 16
                i4 = z3%26 - 16

                z4 = z3//26
                i5 = z4%26 - 11

                z5 = z4//26
                i6 = z5%26 - 6

                if (i4 in poss_input) and (i5 in poss_input) and (i6 in poss_input):
                    break
            

# z4 = z3//26
# input_5 = z4%26 - 11

# z5 = z4//26
# input_6 = z5%26 - 6

z8 = 26**2*9 + 26**2*5 + 26*9 + 26*14 + 9 + 15 + 9//26 + 16//26 + 26*9 + 26*13 + 9 + 16
input_9 = z8%26 - 10

z9 = z8//26
input_10 = z9%26 - 8

z10 = z9//26
input_11 = z10%26 - 11

z12 = 9 + 5 + 9//26 + 14//26 + 9//26**2 + 15//26**2 + 9//26**3 + 16//26**3 + 9//26 + 13//26 + 9//26**2 + 16//26**2 + 9 + 11
input_13 = z12%26 - 15

dummy = 123

