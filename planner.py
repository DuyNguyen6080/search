import sys
from collections import deque, defaultdict
import heapq
import time

class WorldState:
    def __init__(self, robot_pos, dirty_cells, grid, parent=None, action=None, cost=0):
        self.robot_pos = robot_pos
        self.dirty_cells = dirty_cells
        self.grid = grid
        self.parent = parent
        self.action = action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        if not isinstance(other, WorldState):
            return False
        return (self.robot_pos == other.robot_pos and 
                self.dirty_cells == other.dirty_cells)

    def __hash__(self):
        return hash((self.robot_pos[0], self.robot_pos[1], frozenset(self.dirty_cells)))
    
    

def read_world_file(filename):
    with open(filename, 'r') as f:
        cols = int(f.readline().strip())
        rows = int(f.readline().strip())
        grid = []
        robot_pos = None
        dirty_cells = set()
        
        for i in range(rows):
            line = f.readline().strip()
            row = []
            for j, char in enumerate(line):
                if char == '_':  # Convert underscore to space for empty cells
                    row.append(' ')
                else:
                    row.append(char)
                if char == '@':
                    robot_pos = [i, j]
                elif char == '*':
                    dirty_cells.add((i, j))
            grid.append(row)
        
        return grid, robot_pos, dirty_cells

def get_valid_moves(state):
    moves = []
    row, col = state.robot_pos
    rows, cols = len(state.grid), len(state.grid[0])
    
    # Check all four directions
    directions = [('N', -1, 0), ('S', 1, 0), ('E', 0, 1), ('W', 0, -1)]
    
    for action, dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (0 <= new_row < rows and 0 <= new_col < cols and 
            state.grid[new_row][new_col] != '#'):
            moves.append([action, [new_row, new_col]])
    
    # Add vacuum action if current cell is dirty
    if tuple(state.robot_pos) in state.dirty_cells:
        moves.append(['V', state.robot_pos])
    
    return moves

def get_path(state):
    path = []
    current = state
    
    while current.parent:
        path.append(current.action)
        current = current.parent
    return path[::-1]

def uniform_cost_search(initial_state):
    frontier = []
    heapq.heappush(frontier, initial_state)
    explored = set()
    nodes_generated = 1
    nodes_expanded = 0
    
    
    
    while frontier:
        #print('\n')
        #sys.stdout.write("\r Working on it")
        #sys.stdout.flush()
        
        current = heapq.heappop(frontier)
        # of the world is clean of dirt then return 
        if not current.dirty_cells:
            return get_path(current), nodes_generated, nodes_expanded
        
        if current in explored:
            continue
            
        explored.add(current)
        nodes_expanded += 1
        
        for action, new_pos in get_valid_moves(current):
            new_dirty = current.dirty_cells.copy()
            if action == 'V':
                new_dirty.remove(tuple(new_pos))
            
            new_state = WorldState(
                new_pos,
                new_dirty,
                current.grid,
                current,
                action,
                current.cost + 1
            )
           # print(" state action: " + new_state.action)
            """ print("new state: ")
            
            print("Robot Position:", new_state.robot_pos)
            print("Dirty Cells:", new_state.dirty_cells)
            print("Grid:")
            for row in new_state.grid:
                print("  ", row)
            print("Parent:", new_state.parent)
            print("Action:", new_state.action)
            print("Cost:", new_state.cost)
            print("------------------------------------------")"""
            heapq.heappush(frontier, new_state) 
            
    
    return [], nodes_generated, nodes_expanded

def depth_first_search(initial_state):
    frontier = [initial_state]
    explored = set()
    nodes_generated = 1
    nodes_expanded = 0
    
    spinner = "|/-\\"
    i = 0

    print("depth first search in action... PLEASE WAIT")
    while frontier:
        sys.stdout.write("\rWorking on it " + spinner[i % len(spinner)])
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
        current = frontier.pop()
        
        if not current.dirty_cells:
            return get_path(current), nodes_generated, nodes_expanded
        
        if current in explored:
            continue
            
        explored.add(current)
        nodes_expanded += 1
        
        # Get moves in reverse order to maintain DFS ordering
        moves = get_valid_moves(current)[::-1]
        for action, new_pos in moves:
            new_dirty = current.dirty_cells.copy()
            if action == 'V':
                new_dirty.remove(tuple(new_pos))
            
            new_state = WorldState(
                new_pos,
                new_dirty,
                current.grid,
                current,
                action,
                current.cost + 1
            )
            
            nodes_generated += 1
            frontier.append(new_state)
    
    return [], nodes_generated, nodes_expanded

def main():
    if len(sys.argv) != 3:
        print("Usage: python planner.py [algorithm] [world-file]")
        sys.exit(1)
    
    algorithm = sys.argv[1].lower()
    world_file = sys.argv[2]
    #print(world_file)
    if algorithm not in ['uniform-cost', 'depth-first']:
        print("Algorithm must be either 'uniform-cost' or 'depth-first'")
        sys.exit(1)
    
    try:
        grid, robot_pos, dirty_cells = read_world_file(world_file)
        
        initial_state = WorldState(robot_pos, dirty_cells, grid)
        
        if algorithm == 'uniform-cost':
            path, nodes_generated, nodes_expanded = uniform_cost_search(initial_state)
        else:
            path, nodes_generated, nodes_expanded = depth_first_search(initial_state)
        
        for action in path:
            print(action)
        print(f"{nodes_generated} nodes generated")
        print(f"{nodes_expanded} nodes expanded")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 