from operator import attrgetter


class Cell:
    """Represents a graph cell (node) used in A* algorithm."""

    def __init__(self, i, j, h):
        self.i = i
        self.j = j
        self.h = h

        # None is the equivalent of Infinity
        self.g = None

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.i == other.i and self.j == other.j
        return False

    def __hash__(self) -> int:
        return hash((self.i, self.j))

    @property
    def f(self):
        return self.g + self.h if self.g is not None else None


def _construct_path(came_from, current):
    """Constructs the path to `current` by finding the preceding point of the current one."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path


def a_star(start, goal, get_neighbors, get_distance):
    """Finds the shortest path from `start` to `goal` using A* algorithm.
        See more: https://en.wikipedia.org/wiki/A*_search_algorithm.
    """
    start.g = 0
    open_set = [start]
    closed_set = []
    came_from = {}

    while len(open_set) > 0:
        current = min(open_set, key=attrgetter('f'))
        if current == goal:
            return _construct_path(came_from, current)

        open_set.remove(current)
        closed_set.append(current)
        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue
            g = current.g + get_distance(current, neighbor)
            if neighbor.g is None or g < neighbor.g:
                came_from[neighbor] = current
                neighbor.g = g
                if neighbor not in open_set:
                    open_set.append(neighbor)

    return None
