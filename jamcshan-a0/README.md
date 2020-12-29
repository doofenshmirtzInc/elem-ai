# a0

ROUTE_PICHU.PY

1. what is the search abstraction used in the original code?  

The search abstraction implemented in the original code is search algorithm #1.
Within the code for the search algorithm, the fringe data structure (formally a
list of tuples) is implemented in the fashion of a stack making the search
method depth-first search.

INITIAL STATE 
....XXX 
.XXX...  
....X..  
.X.X...  
.X.X.X.  
pX...X@

STATE SPACE 
The state space is all configurations of the board such that the
pichu resides in a tile that contained a '.'

SUCCESSOR FUNCTION 
Returns any tile either North, South, East or West of the
current pichu position that does not contain an 'X'

COST FUNCTION 
f(s) = f(s) + 1, i.e. every move has a uniform cost of one.

GOAL STATE 
That the pichu reaches the tile containing a '@'

2. Why does the program often fail to find a solution? Explain what you did to
   fix it.

   The program fails to find a solution because it get stuck searching (in the
   case of the original map) in locations (2,2) and (2,3). The algorithm gets
   stuck continually searching from the same two nodes as they keep appearing at
   the top to the stack. The simplest solution may be adding a VISITED data structure to the algorithm to avoid revisiting nodes
   that have already been added to the stack.

   Implementing the VISITED structure has "fixed" the search algorithm in that
   the depth-first search now works as it should. However, as it is not
   implemented as iterative deepening, it does not always find the optimal
   solution.

   A fix for this might be converting the search method from DFS to IDS.

3. Explain what you did to finish the overall implementation of the program
   (providing the rest of the necessary features).

4. Explain the abstraction you used to implement the solution -- what is the
   state space, initial state, goal state, successor func, and cost func?

   For the final implementation, I continued to use search Algorithm #1. What I
   did change is the algorithm that was used to traverse tha map.  Originally it
   had been DFS which is neither a complete nor an optimal search algorithm.  I
   modified it slightly so that it functioned as IDS (a complete and optimal
   algorithm).

   STATE SPACE
   All nodes in the graph that do not contain an 'X'

   INITIAL STATE
   The node which contains a 'p'. In the case of the original map, it was (5,
   0).

   GOAL STATE
   Reaching the node containing a '@'

   SUCCESSOR FUNCTION
   The abstracted successor function for this maze solving algorithm returns
   all nodes in a cardinal direction from the current node that does not contain
   an 'X' and has not yet been visited.

   COST FUNCTION
   The cost function for this graph is uniform (i.e. each move has a cost of 1).









ARRANGE_PICHUS.PY

1. Explain the search abstraction you used.

I used the same graph traversal method that was present in the original code
(DFS).

The search abstraction that I used only varied slightly from the abstraction
used in the original code. All I had to do to get this implementation of the
code working was tweak the SUCESSOR() function such that it took into account
sightline conflicts between the different pichus on a given map (something the
original successor fuction did not do). This in turn affected the state space
for the problem.

Abstraction used in my implementation:

STATE SPACE

All boards such that there were less than or equal to 'K' pichus on the board
and there were no sightline conflicts (i.e. there were no pichus in the same row
or column that did not have a wall or video recorder between them).

INIT STATE

A board containing one of 'K' pichus

GOAL STATE

A board containing 'K' pichus without any sightline conflicts between the
different pichus.

SUCC FUNCTION

Any board containing an additional pichu which does not contain any sightline
conflicts.

COST FUNCTION

Any change in state corresponds to a zero change in cost as in this case we are
simply looking for any solution at all. Whether it is the 'optimal' layout of
pichus is irrelavant.
