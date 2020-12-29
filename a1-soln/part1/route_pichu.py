#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Jack McShane (jamcshan)
#
# Based on skeleton code provided in CSCI B551, Fall 2020.

import sys
import json

# Parse the map from a given filename
# returns 2D list of chars
def parse_map(filename):
    with open(filename, "r") as f:
            return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Check if a row,col index pair is on the map
# returns: boolean
# can chain comparison operators in python which is nuts
def valid_index(pos, n, m):
    return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the next moves from position (row, col)
# returns list of tuples which serve as coordinates
def moves(map, row, col):
    moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

    # Return only moves that are within the board and legal (i.e. go through open space ".")
    return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

def get_dir(start, end):
    dir_dict = {(1,0):'S', (-1,0):'N', (0,1):'E', (0,-1):'W'}
    moved = (end[0] - start[0], end[1] - start[1])
    return dir_dict[moved]


# Perform search on the map
def search1(house_map):
        # Find pichu start position
        pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]


        #fringe is a list of tuples
        #code has fringe implemented as a stack, which means the search algorithm being used is depth-first search
        fringe=[(pichu_loc,0, '')]
        #a list of node already visited which can be used to prevent revisiting a given node
        visited = []
        curr_depth = 0

        while fringe:
            #a temp structure to hold possible successor nodes to the current node
            next_moves = []
            #used for keeping the algorithm at a particular depth such that DFS now becomes IDS
            while fringe and (curr_depth - fringe[-1][1]) == 0:
                (curr_move, curr_dist, dir_str)=fringe.pop()
                visited.append(curr_move)
                for move in moves(house_map, *curr_move):
                    #check if goal state
                    if house_map[move[0]][move[1]]=="@":
                        return [curr_dist+1, dir_str+get_dir(curr_move, move)]
                    else:
                        # as long as 'move' has not been visited
                        if visited.count(move) == 0:
                            #add to list of possible next moves
                            next_moves.append((move, curr_dist + 1, dir_str + get_dir(curr_move, move)))
            #now that each node at the current depth has been checked, add all possible successor nodes to the fringe stack
            [fringe.append(move) for move in next_moves]
            curr_depth += 1
        #return INF is no soln
        return 'Inf'
#search alg 1
# if goal(init-state) return init-state

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search1(house_map)
        print("Here's the solution I found:")
        print(f'{solution[0]} {solution[1]}')

