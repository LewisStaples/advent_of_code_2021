# adventOfCode 2021 day 12, part b
# https://adventofcode.com/2021/day/12

class CaveMap:
    def __init__(self):
        # self.edges is a dict with index string (one node),
        # and value a list of strings (various nodes that index can go to)
        # every edge gets added twice in the dict, 
        # every node gets added once as an index,
        # and 1 or more times within the lists in the value
        self.edges = {}

    # this adds a one-way edge
    # (this is designed to not be called externally,
    # but instead only to be called internally by add_edge)
    def add_edge_1way(self, left, right):
        if left in self.edges:
            self.edges[left].append(right)
        else:
            self.edges[left] = [right]

    # this adds a two-way edge
    # (this is designed to be called externally,
    # and then to work with two internal calls to add_edge_1way)
    def add_edge(self, left, right):
        self.add_edge_1way(left, right)
        self.add_edge_1way(right, left)

    # this function is for part b only:
    # this looks for any small caves that appear
    # more than once in the path
    # (it looks for lower case substrings that appear twice)
    def any_repeat_small_caves(self, curr_path):
        for cave in curr_path.split('-'):
            # print(cave)
            if cave.islower():
                if curr_path.count(cave) > 1:
                    return True
        return False

    # this function calls itself recursively along a path
    # (designed to only be called by traverse_map)
    def recur_path(self, index_in_path):
        ret_val = 0
        curr_path = self.paths[index_in_path]
        curr_node = curr_path.split('-')[-1]
        self.paths.remove(curr_path)

        # explore all possible caves(nodes) that can be reached 
        # from the current cave/node
        for next_node in self.edges[curr_node]:
            if next_node == 'end':
                # uncommenting the below line lists all paths
                print(curr_path.replace('-',',') + ',end')

                # a successful path has been found to exit, therefore count it
                ret_val += 1
                continue

            # visiting start after starting is forbidden
            # (this code wasn't needed for part a, because this was enforced
            # by the one-time visit to small cave rule)
            if next_node == 'start':
                continue

            # if next node is lowercase, already in curr_path,
            # and if there are any repeated small caves,
            #   skip this iteration of the for loop
            if next_node in curr_path:
                if next_node.islower():
                    if self.any_repeat_small_caves(curr_path):
                        continue

            # if the code reaches this point, then the next cave will be visited
            this_path = curr_path + '-' + next_node
            self.paths.append(this_path)
            ret_val += self.recur_path(self.paths.index(this_path))
        # returns the total number of paths found by this function call,
        # as well as all recursive calls
        return ret_val

    # this function starts the traversal of a path through the caves
    # this function is designed to be called externally
    def traverse_map(self, beginning='start'):
        self.paths = []
        ret_val = 0
        for next_node in self.edges[beginning]:
            this_path = beginning + '-' + next_node
            self.paths.append(this_path)
            ret_val += self.recur_path(self.paths.index(this_path))

        return ret_val

cavemap = CaveMap()

# reading input from the input file
input_filename='input_sample0.txt'
with open(input_filename) as f:
    # pull in each line from the input file
    for in_string in f:
        [left, right] = in_string.rstrip().split('-')
        cavemap.add_edge(left, right)

path_count = cavemap.traverse_map('start')

print(path_count)
