# adventOfCode 2021 day 9 part a
# https://adventofcode.com/2021/day/9


class HeightMap:
    def __init__(self):
        input_filename='input.txt'
        self.height_map = []

        with open(input_filename) as f:
            # pull in each line from the input file
            for in_string in f:
                # print([int(x) for x in in_string.rstrip()])
                self.height_map.append([int(x) for x in in_string.rstrip()])
        # print(self.height_map)

    def sum_low_points(self):
        ret_val = 0
        for i,i_list in enumerate(self.height_map):
            for j, j_list in enumerate(i_list):
                ret_val += self.risk_level(i,j)
                # print(str(i) + ', ' + str(j), end=': total_risk = ')
                # print(ret_val)
        return ret_val

    def risk_level(self,i,j):
        up = self.height_map[i][j-1] if j>0 else 10
        down = self.height_map[i][j+1] if j<len(self.height_map[0])-1 else 10
        left = self.height_map[i-1][j] if i>0 else 10
        right = self.height_map[i+1][j] if i<len(self.height_map)-1 else 10

        # up = self.height_map[i][j-1]
        # down = self.height_map[i][j+1]
        # left = self.height_map[i-1][j]
        # right = self.height_map[i+1][j]

        # # if over the edge then treat other value as 10 .... guaranteed to be larger than (i,j)
        # if i < 0:
        #     left = 10
        # if i > len(self.height_map):
        #     right = 10
        # if j < 0:
        #     up = 10
        # if j > len(self.height_map[0]):
        #     down = 10

        # if this point is a low point, then return risk level
        if self.height_map[i][j] < min([left, right, up, down]):
            return self.height_map[i][j]+1
        
        # since it's not a low point, return 0              
        return 0

the_height_map = HeightMap()
print()
print('The solution to part a is ', end='')
print(the_height_map.sum_low_points())
print()
