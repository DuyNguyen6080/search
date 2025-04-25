impliment a uniform cost search and DFS for a vacum robot in a dirty world
to run: python planner.py [uniform-cost|depth-first] [path-to-world-file]

Program Usage
Your program should be run from the command line with two arguments:
python3 planner.py [algorithm] [world− file]
• [algorithm] should be either uniform-cost or depth-first
• [world-file] should be the path to a .txt file as described above

world file: .txt
- first line indicate columns
- second line indicate rows
- the rest represent the map
  
Each character represents a cell:
• = empty cell
• # = blocked cell
• * = dirty cell
• @ = robot starting location
Example:
python3 planner.py uniform−costtiny−1.txt

Output Format
Your program print:
  1. One action per line: N, S, E, W, or V
  2. One line with the number of nodes generated
  3. One line with the number of nodes expanded

Example output:
E
V
W
N
N
V
E
E
S
V
85 nodes generated
39 nodes expanded
