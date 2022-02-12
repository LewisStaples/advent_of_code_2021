# adventOfCode 2021 day 24 helper
# https://adventofcode.com/2021/day/24/helper.py

# z_13 = input_0/26 + input_1/26^2 + input_2/26^3 + input_3/26^4 + 97750/26^5 + input_7/26^2 + 13/26^2 + input_8/26^3 + 16/26^3 + input_12/16 + 11/16



for i0 in range(9,0,-1):
    for i1 in range(9,0,-1):
        for i2 in range(9,0,-1):
            for i3 in range(9,0,-1):
                for i7 in range(9,0,-1):
                    for i8 in range(9,0,-1):
                        for i12 in range(9,0,-1):
                            fxn = i0/26 + i1/26**2 + i2/26**3 + i3/26**4 + 97750/26**5 + i7/26**2 + 13/26**2 + i8/26**3 + 16/26**3 + i12/16 + 11/16
                            if fxn < 0.02:
                                dummy = 123

    