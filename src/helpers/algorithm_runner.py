import math
import params

from a_star import Cell, a_star


def euc_distance(point_a, point_b):
    """Calculates the euclidean distance between the given points."""
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def _convert_map(map_, goal):
    """Converts the given (world) map to an appropriate graph for A* algorithm."""
    h = euc_distance
    return [
        [None if tile == 'B' else Cell(i, j, h((i, j), goal)) for j, tile in enumerate(row)]
        for i, row in enumerate(map_)
    ]


def _distance(cell_1, cell_2):
    """Calculates distance between two instances of Cell."""
    return euc_distance((cell_1.i, cell_1.j), (cell_2.i, cell_2.j))


def _get_neighbors(graph, cell):
    """Gets neighbor cells for given one."""
    neighbors = []
    if cell.i - 1 >= 0:
        n = graph[cell.i - 1][cell.j]
        if n:
            neighbors.append(n)
    if cell.i + 1 < params.ROW_COUNT:
        n = graph[cell.i + 1][cell.j]
        if n:
            neighbors.append(n)
    if cell.j - 1 >= 0:
        n = graph[cell.i][cell.j - 1]
        if n:
            neighbors.append(n)
    if cell.j + 1 < params.COL_COUNT:
        n = graph[cell.i][cell.j + 1]
        if n:
            neighbors.append(n)

    return neighbors


def run_a_star(map_, start, goal):
    """Runs the A* algorithm."""
    graph = _convert_map(map_, goal)

    start_cell = graph[start[0]][start[1]]
    end_cell = graph[goal[0]][goal[1]]

    res = a_star(start_cell, end_cell, lambda x: _get_neighbors(graph, x), _distance)
    path = []
    if res is not None:
        for cell in res:
            path.append((cell.i, cell.j))

    return path
