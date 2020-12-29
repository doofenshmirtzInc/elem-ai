##### Part 1
##### Lead: jamcshan

This program utilizes search algorithm #3 from the lectures to implement A*
This prog ram utilizes search algorithm #3 from the lectures to implement A*
search. The implementation of A*, using search algorithm #3, requires two
conditions be met:
    1. The evaluation function includes a consistent heuristic function (i.e.
@@ -97,3 +97,12 @@ the fringe and considered by the algorithm.

#### Part 2
#### Lead - purama
####

-> Precompute Distance of Each city from Starting City, Similarly Precompute Distance of Each city from Final/Destination City (Based on Latitude and Longitude).
-> Successor Function:
    - From Current City, Identify all the Freeway connecting to the current city.
    - Identify next city in each freeway connecting to city.
    - If the Next City is 'Final City', Then we have reached the goal, Exit the program.
    - Add Next city (Which is next state) to Fringe along with cost function like 'Distance'/'Count of Road segment'/'Time (Distance * Miles per Hr)'/'Less Probability for accident'
    - Also add city and Freeway information to another list 'Visited List', Which will be used to avoid adding same city to fringe again.
-> From the Priority Queue pick the city (State) which contains less cost (If cost is distance, Pick the city with less distance to Goal state (Distance to Goal state is precomputed independently from every city) ).
-> Explore the state/city which we got from above priority queue by going to step2 (Successor function).

- Currently Program is running for few Start and Final City and not running for many cities.
- Sometime program is not finding all the successor cities, Hence some of the freeway are going unexplored. Might need another couple of days to debug and fix same.

Approach Tried and Failed:

-> In Successor function,  To identify next city, I have sorted tried Latitude/Longitude coordinates and tried to pick immediate next city compared to current city/State/
    Above approach has not worked, So i have pre computed Distance of each city from Start city to identify immediate next city or Successor city.

## Part 3
##### Lead: samize

This program starts off by checking whether the input is valid. If valid, it proceeds to search for optimal groupings.

If the file is run normally, it will call main() which will loop through and evaluate random groupings.

To evaluate, it calls the evaluate function which both calculates the heuristic of that state as well as determines the string representation of that set of groups. If it beats the previous total time for graders, it is printed out as a result. It iterates through a max of N! times, where N is the number of students.
