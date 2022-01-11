# adventOfCode 2021 day 19
# https://adventofcode.com/2021/day/19

import re
import math

class Scanner:
    def __init__(self):
        self.point_list = []
        self.edges = dict()
        self.lengths_squared = set()

    def load_point(self, point_tuple):
        self.point_list.append(point_tuple)

    def determine_edges(self):
        for p1_index in range(len(self.point_list) - 1):
            for p2_index in range(p1_index + 1, len(self.point_list)):
                length_squared = 0
                for comp_index in range(len(self.point_list[p1_index])):
                    length_squared += (self.point_list[p1_index][comp_index] - self.point_list[p2_index][comp_index])**2
                self.edges[(p1_index, p2_index)] = length_squared
                self.lengths_squared.add(length_squared)

scannerList = []

# For 12 common beacons there should be 1+2+...+11 = 66 This may be proven using recursive logic where adding a new point to a graph of n points creates n new edges. So start with n=1 point with no initial edges, then adding a second point adds a single edge (1 in total), then adding a third point yields two new edges (3 total), and so on.
REQUIRED_NUMBER_OF_EQUAL_LENGTH_EDGES = 66


# This function will handle the transform.  Parameter beacon is the index in scanner1 of a beacon that is somewhere in scanner2, because it has two edges of lengths that are in both scanners.  Parameters siedge1 and siedge2 have the scanner1 indices of the endpoints of these edges and the square of the edge length.  Parameters scannerIndex1 and scannerIndex2 are the indices of the two scanners being compared.
def handle_transform(scannerIndex1, scannerIndex2, beacon, si1edge1, si1edge2):
    # Find edges from scannerIndex2 with same length_squared as si1edge1 and si2edge2
    # Then the point from scannerIndex2 is the same as beacon (as soon from the other scanner)

    dummy = 123
    edge_set = set()

    # for vertex,length_sq in scannerList[scannerIndex2].edges:
    for edge in scannerList[scannerIndex2].edges:
        length_sq = scannerList[scannerIndex2].edges[edge]
        if length_sq in [si1edge1[1], si1edge2[1]]:
            dummy = 234
            edge_set.add(edge)

    # find vertex/beacon that is in both edges in edge_set
    # use this to calculate x difference and y difference

    # from either of the other two vertices/beacons, calculate the rotation

    # then display the coordinates of the points in scannerIndex2 and confirm that it matches what was given


    # testing only
    print(scannerList[scannerIndex1].point_list[beacon], end='                            ')  # next print the point from the other scanner

    print()
    print()
    pass

# reading input from the input file
input_filename='input_sample2.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        in_string = in_string.rstrip()
        if len(in_string) < 2:
            scannerList[-1].determine_edges()
            continue
        if re.match('--- scanner', in_string):
            scannerList.append(Scanner())
        else:
            scannerList[-1].load_point(tuple([int(x) for x in in_string.split(',')]))
    # get last line
    scannerList[-1].determine_edges()

# # testing input of points
# for index, scanner in enumerate(scannerList):
#     print('Scanner # ' + str(index))
#     # for point in scanner.point_list:
#     #     print(point)

#     # # testing calculation of edge squared lengths
#     # print(scanner.edges)

#     # printing set of lengths_squared
#     print(scanner.lengths_squared)
#     print()

# Printing intersections of pairs of sets of lengths_squared from pairs of edges
# For 12 common beacons there should be 1+2+...+11 = 66 (This is due to recursive logic where adding a new point to a graph of n points creates n new edges. So start with n=1 point with no initial edges)
# I assume that no pairs of points will have the same exact distance between them.

# Consider all possible pairs of scannerLists
for scannerIndex1 in range(len(scannerList)-1):
    for scannerIndex2 in range(scannerIndex1+1, len(scannerList)):
        # Consider only pairs of scannerLists with enough identical length edges
        lengths_squared_in_common = scannerList[scannerIndex1].lengths_squared.intersection(scannerList[scannerIndex2].lengths_squared)
        if len(lengths_squared_in_common) >= REQUIRED_NUMBER_OF_EQUAL_LENGTH_EDGES:
            # find any vertex that is the endpoint of more than one equal lengthed edge for scannerList i:
            vertex_dict = {}
            break_for_edge = False
            for edge in scannerList[scannerIndex1].edges.items():
                if edge[1] not in lengths_squared_in_common:
                    # Go to the next edge for this pair of scanners.
                    continue 
                for edge_vertex in edge[0]:
                    if edge_vertex in vertex_dict:
                        # A vertex has been found in scannerIndex1 with more than one edge whose lengths are equal to lengths in scannerIndex2.  Therefore, break out of the for edge loop by going to the next break.
                        break 
                    else:
                        vertex_dict[edge_vertex] = edge
                        # print('Adding vertex # ', end='')
                        # print(edge_vertex)
                else:
                    # Only executed if there was no break
                    continue

                # Code here is executed only if a vertex with two edges with lengths equal to two edges from another scanner is found
                # print('vertex found', end=': ')
                # print(edge_vertex)
                handle_transform(scannerIndex1, scannerIndex2, edge_vertex, edge, vertex_dict[edge_vertex])
                break # break out of the for edge loop





