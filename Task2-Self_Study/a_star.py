import math

def heuristic(a: tuple, b: tuple ) -> int :
    # Manhattan Distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_lowest(open_list: list):
    # Manually find the node with the lowest f cost
    lowest_index = 0
    for i in range(1, len(open_list)):
        if open_list[i][0] < open_list[lowest_index][0]:
            lowest_index = i
    return open_list.pop(lowest_index)

def astar(grid, start, end):
    """
    A* Pathfinding Algorithm
    grid  : 2D list — 0 = space, 1 = wall
    start : (row, col) starting position
    end  : (row, col) target position

    e.g.
    grid = [
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,1,0,0,0],
        [0,1,0,0,1],
        [0,0,0,0,0]
    ]
    """

    # open_list: [ (f, g, current, path), ... ]
    open_list = [(heuristic(start, end), 0, start, [start])]
    visited   = set()

    while open_list:
        f, g, current, path = get_lowest(open_list)

        # Skip if already visited
        if current in visited:
            continue
        visited.add(current)

        # end reached
        if current == end:
            return path

        r, c = current
        # Explore 4 neighbours: Up, Down, Left, Right
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc    = r + dr, c + dc
            neighbour = (nr, nc)

            # Check bounds, not a wall, not visited
            if (0 <= nr < len(grid) and
                0 <= nc < len(grid[0]) and
                grid[nr][nc] == 0 and
                neighbour not in visited):

                new_g = g + 1
                new_f = new_g + heuristic(neighbour, end)
                open_list.append((new_f, new_g, neighbour, path + [neighbour]))

    return None  # No path found