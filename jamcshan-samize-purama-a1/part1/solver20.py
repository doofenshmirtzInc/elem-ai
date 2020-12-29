#!/usr/local/bin/python3
# solver20.py : 2020 Sliding tile puzzle solver
#
# Code by: [PLEASE PUT YOUR NAMES AND USER IDS HERE]
#
# Based on skeleton code by D. Crandall, September 2020
#
from queue import PriorityQueue
import sys
import time

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
COST_PER_MOVE = 5
ROWS = 4
COLS = 5

#returns boolean
def valid_index(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*COLS):(row*COLS+COLS)]
    return ( state[:(row*COLS)] + change_row[-dir:] + change_row[:-dir] + state[(row*COLS+COLS):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::COLS]
    s = list(state)
    s[col::COLS] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# return a list of possible successor states
def successors(state):
    return [ (shift_row(state, row, dir)) for dir in (-1,1) for row in range(0, ROWS) ] + \
        [ (shift_col(state, col, dir)) for dir in (-1,1) for col in range(0, COLS) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


#calc the heuristic h(s)
#sum the manhattan distances of each tile from its position in the goal state
def mdist(state):
    summed_mdist = 0
    for index in range(ROWS*COLS):
        (x_curr, y_curr) = ((index // COLS), (index % COLS))
        (x_goal, y_goal) = ((state[index] - 1)//COLS, (state[index] - 1)%COLS)
        summed_mdist += abs(x_goal - x_curr) + abs(y_goal - y_curr)
    return summed_mdist


def cost_so_far(path_so_far):
    return len(path_so_far) * COST_PER_MOVE




def solve(initial_board):
    ##############A* using consistent heuristic#########################
    ##if goal(init_state), return init_state
    if is_goal(initial_board):
        return initial_board
    ##insert(init_node, fringe)
    #fringe is implemented as priority queue using the python list structure
    fringe = [(mdist(initial_board), (initial_board, []))]
    #visited structure is implemented as a hash map; states themselves are used as the keys
    visited = {}
    ##repeat:
        ##if empty(fringe), return failure
    while len(fringe) > 0:
        ##s <- remove(fringe)
        fringe.sort(reverse=True)
        (p, (state, path_so_far)) = fringe.pop()
        ##insert(s, closed)
        visited[state] = path_so_far
        ##if goal(s) return path
        if is_goal(state):
            return path_so_far
        ##for s' in SUCC(s):
        for (succ, move) in successors(state):
            ##if s' in closed, discard s'
            if visited.get(succ) is not None:
                continue
            ##if s' not in fringe, insert(s', fringe)
            fringe.append((mdist(succ) + cost_so_far(path_so_far + [move,]), (succ, path_so_far + [move,])))
    return False




if __name__ == "__main__":
    start_time = time.time()
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
    print(f'runtime: {time.time() - start_time}')

