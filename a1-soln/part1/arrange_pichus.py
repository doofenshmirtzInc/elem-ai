#!/usr/local/bin/pyth/npon3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Jack McShane (jamcshan)
#
# Based on skeleton code in CSCI B551, Fall 2020
#


#automated tester used map2, map3 with 15 and 7 respectively
#have to improve the successor function: far too slow of a runtime


import sys
import numpy as np

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    #original code
    #return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' ]

    #rewritten successors() function
    true_successors = []
    for r in range(0, len(board)):
        for c in range(0, len(board[0])):
            if board[r][c] == '.':
                new_board = np.array(add_pichu(board, r, c))
                if check_row(new_board[r,:]) and check_row(new_board[:,c]):
                    true_successors.append(new_board.tolist())

    return true_successors

#checks if given board state is valid (i.e. no sightline conflicts)
def is_valid_succ(board):
    is_valid = True
    #check rows
    rows = [check_row(row) for row in board]
    #check columns
    cols = [check_row(row) for row in transpose_matrix(board)]
    for boolean in rows:
        is_valid = is_valid and boolean
    for boolean in cols:
        is_valid = is_valid and boolean

    #is_valid should only be true while no rows or cols have sightline conflicts
    return is_valid


#checks that a given 'row' does not have a sightline conflict between agents
def check_row(row):
    #if only one pichu in the row, return True
    if np.char.count(row, 'p').sum() < 2:
        return True
    #if any pichu's in a row can see each other, return False
    condensed_row = [char for char in row if char not in '.']
    for i in range(len(condensed_row) - 1):
        if condensed_row[i] == 'p' and condensed_row[i + 1] == 'p':
            return False
    #else return True
    return True



def transpose_matrix(matrix):
    #code for transposing a matrix using list comprehension:
    #result = [[x[j][i] for j in range(len(x))] for i in range(len(x[0]))]
    #credit: tutorialspoint.com
    #link: https://www.tutorialspoint.com/transpose-a-matrix-in-python
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


# check if board is a goal state
def is_goal(board):
    return count_pichus(board) == K

# Solve!
def solve(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    K = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map)
    print ("Here's what we found:")
    print (printable_board(solution) if solution else "None")
