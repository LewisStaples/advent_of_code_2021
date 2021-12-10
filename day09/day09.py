# adventOfCode 2021 day 9
# https://adventofcode.com/2021/day/9

# class to handle height map behavior
class HeightMap:
    # (parts a and b) constructor: reads input file and populates self.height_map
    def __init__(self):
        # used in parts a and b, map storing height at various locations
        self.height_map = []

        # reading height input from the input file
        input_filename='input.txt'
        with open(input_filename) as f:
            # pull in each line from the input file
            for in_string in f:
                self.height_map.append([int(x) for x in in_string.rstrip()])

        # used in part b: indicates whether a point has been used to calculate basin size
        self.point_checked = [[False for i in range(len(self.height_map[0]))] for j in range(len(self.height_map))]

    # (part a) this returns the sum of risk levels for all low points
    def sum_low_points(self):
        ret_val = 0
        for i,i_list in enumerate(self.height_map):
            for j, j_list in enumerate(i_list):
                ret_val += self.risk_level(i,j)
        return ret_val

    # (part b) this uses recursion to calculate basin_size
    def calc_basin_size(self, basin_size, i, j):
        # check if this point is off of self.height_map
        if True in [i<0, j<0, i>=len(self.height_map), j>=len(self.height_map[0])]:
            return 0

        # check if this point was checked earlier
        if self.point_checked[i][j]:
            return 0
        
        # mark (i,j) checked so this point won't be checked again in the future
        self.point_checked[i][j] = True

        # do not count points with a height of nine
        if self.height_map[i][j] == 9:
            return 0

        # if this code is being run, then this point is in the basin
        # add the point to add to the basin_size, and then use
        # recursion to call the four points that surround it
        ret_val = 1 \
            + self.calc_basin_size(basin_size, i+1, j) \
            + self.calc_basin_size(basin_size, i-1, j) \
            + self.calc_basin_size(basin_size, i, j+1) \
            + self.calc_basin_size(basin_size, i, j-1) 
        
        # return count of this point (1), plus all points that
        # were called recursively from here
        return ret_val

    # (part b) this calculates the product of the three largest basins
    # (done by this function and by calling calc_basin_size recursively)
    def prod_three_largest_basins(self):
        # print()
        basin_list = []
        for i,i_list in enumerate(self.height_map):
            for j, j_list in enumerate(i_list):
                if self.risk_level(i,j) > 0:
                    basin_size = 0
                    basin_list.append(self.calc_basin_size(basin_size, i,j))
        basin_list.sort(reverse=True)


        return basin_list[0]*basin_list[1]*basin_list[2]

    # (parts a and b) returns risk level for the point (i,j)
    # this returns 0 if point(i,j) is not a low point
    def risk_level(self,i,j):
        # computes height for each of four surrounding points
        # (if (i,j) is up against any of the four edges, 
        # a large number is returned instead of throwing an IndexError)
        LARGE_HEIGHT = float('inf')
        up = self.height_map[i][j-1] if j>0 else LARGE_HEIGHT
        down = self.height_map[i][j+1] if j<len(self.height_map[0])-1 else LARGE_HEIGHT
        left = self.height_map[i-1][j] if i>0 else LARGE_HEIGHT
        right = self.height_map[i+1][j] if i<len(self.height_map)-1 else LARGE_HEIGHT

        # if this point is a low point, then return risk level
        if self.height_map[i][j] < min([left, right, up, down]):
            return self.height_map[i][j]+1
        
        # since it's not a low point, return 0              
        return 0

# used by parts a and b
the_height_map = HeightMap()
print()

# solve and display part a
print('The solution to part a is ', end='')
print(the_height_map.sum_low_points())
print()

# solve and display part b
print('The solution to part b is ', end='')
print(the_height_map.prod_three_largest_basins())
print()
