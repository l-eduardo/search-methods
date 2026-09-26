"""Data models for a generated grid maze.

The public API is intentionally small so that it can be used directly from a
Jupyter notebook::

    maze = MazeGenerator(15, seed=7).generate()
    print(maze)

Both square sizes (``15``) and rectangular sizes (``(rows, columns)``) are
accepted by :class:`MazeGenerator`.
"""

from __future__ import annotations

from random import Random
from typing import Iterable, Optional, Sequence


Position = tuple[int, int]


def _normalise_size(size: int | Sequence[int]) -> tuple[int, int]:
    """Return ``(rows, columns)`` after validating a maze size."""

    if isinstance(size, bool):
        raise TypeError("size must be an integer or a pair of integers")

    if isinstance(size, int):
        rows = columns = size
    else:
        values = tuple(size)
        if len(values) != 2:
            raise ValueError("a rectangular size must be (rows, columns)")
        rows, columns = values

    if isinstance(rows, bool) or isinstance(columns, bool):
        raise TypeError("rows and columns must be integers")
    if not isinstance(rows, int) or not isinstance(columns, int):
        raise TypeError("rows and columns must be integers")
    if rows < 2 or columns < 2:
        raise ValueError("a maze needs at least 2 rows and 2 columns")

    return rows, columns


class Maze:
    """A rectangular grid maze.

    ``True`` in ``walls`` means that a cell is blocked. Coordinates are
    represented as ``(row, column)`` tuples, with ``(0, 0)`` at the top-left.
    """

    WALL = "#"
    OPEN = " "
    START = "S"
    GOAL = "G"
    PATH = "·"

    def __init__(
        self,
        size: int | Sequence[int],
        walls: Optional[Sequence[Sequence[bool]]] = None,
        start: Optional[Position] = None,
        goal: Optional[Position] = None,
    ) -> None:
        self.rows, self.columns = _normalise_size(size)

        if walls is None:
            self.walls = [
                [False for _ in range(self.columns)] for _ in range(self.rows)
            ]
        else:
            if len(walls) != self.rows or any(
                len(row) != self.columns for row in walls
            ):
                raise ValueError("walls must have the same dimensions as size")
            self.walls = [[bool(cell) for cell in row] for row in walls]

        self.start = start if start is not None else (0, 0)
        self.goal = goal if goal is not None else (
            self.rows - 1,
            self.columns - 1,
        )
        self._validate_position(self.start, "start")
        self._validate_position(self.goal, "goal")
        if self.is_wall(self.start) or self.is_wall(self.goal):
            raise ValueError("start and goal must be walkable cells")

    @property
    def size(self) -> tuple[int, int]:
        """Return the maze dimensions as ``(rows, columns)``."""

        return self.rows, self.columns

    def _validate_position(self, position: Position, label: str = "position") -> None:
        if (
            not isinstance(position, tuple)
            or len(position) != 2
            or not all(isinstance(value, int) for value in position)
        ):
            raise TypeError(f"{label} must be a (row, column) tuple")
        row, column = position
        if not (0 <= row < self.rows and 0 <= column < self.columns):
            raise ValueError(f"{label} {position} is outside the maze")

    def is_wall(self, position: Position) -> bool:
        """Return whether a position is blocked."""

        self._validate_position(position)
        row, column = position
        return self.walls[row][column]

    def is_walkable(self, position: Position) -> bool:
        """Return whether a position is inside the grid and not blocked."""

        row, column = position
        return (
            0 <= row < self.rows
            and 0 <= column < self.columns
            and not self.walls[row][column]
        )

    def neighbors(self, position: Position) -> Iterable[Position]:
        """Yield walkable four-directional neighbors of ``position``."""

        row, column = position
        for next_position in (
            (row - 1, column),
            (row, column + 1),
            (row + 1, column),
            (row, column - 1),
        ):
            if self.is_walkable(next_position):
                yield next_position

    def render(self, path: Optional[Iterable[Position]] = None) -> str:
        """Return a printable representation, optionally overlaying a path."""

        path_cells = set(path or ())
        lines: list[str] = []
        for row in range(self.rows):
            symbols: list[str] = []
            for column in range(self.columns):
                position = (row, column)
                if position == self.start:
                    symbol = self.START
                elif position == self.goal:
                    symbol = self.GOAL
                elif self.walls[row][column]:
                    symbol = self.WALL
                elif position in path_cells:
                    symbol = self.PATH
                else:
                    symbol = self.OPEN
                symbols.append(symbol)
            lines.append("".join(symbols))
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.render()

    @classmethod
    def from_lines(cls, lines: Sequence[str], *, wall: str = "#") -> "Maze":
        """Build a maze from text containing ``#``, ``S`` and ``G``.

        Any character different from ``wall`` is considered walkable. This
        makes it possible to paste a maze using either spaces or dots.
        """

        if not lines or not all(isinstance(line, str) for line in lines):
            raise ValueError("lines must contain at least one string row")
        rows = len(lines)
        columns = len(lines[0])
        if columns == 0 or any(len(line) != columns for line in lines):
            raise ValueError("all maze rows must have the same non-zero width")

        starts = [
            (row, column)
            for row, line in enumerate(lines)
            for column, symbol in enumerate(line)
            if symbol == cls.START
        ]
        goals = [
            (row, column)
            for row, line in enumerate(lines)
            for column, symbol in enumerate(line)
            if symbol == cls.GOAL
        ]
        if len(starts) != 1 or len(goals) != 1:
            raise ValueError("the maze must contain exactly one S and one G")

        walls = [[symbol == wall for symbol in line] for line in lines]
        walls[starts[0][0]][starts[0][1]] = False
        walls[goals[0][0]][goals[0][1]] = False
        return cls((rows, columns), walls, starts[0], goals[0])


class MazeGenerator:
    """Generate a connected, randomized maze for a requested matrix size.

    The recursive-backtracker algorithm creates a connected maze. A local
    ``Random`` instance is used, so passing ``seed`` makes the result
    reproducible without changing Python's global random state.
    """

    def __init__(
        self,
        size: int | Sequence[int],
        *,
        seed: Optional[int] = None,
        loop_probability: float = 0.0,
    ) -> None:
        self.rows, self.columns = _normalise_size(size)
        if not 0.0 <= loop_probability <= 1.0:
            raise ValueError("loop_probability must be between 0 and 1")
        self.loop_probability = loop_probability
        self.random = Random(seed)

    def generate(self) -> Maze:
        """Create and return a new maze."""

        # Very small rectangles do not have enough room for an inner maze
        # lattice. Keeping them open is clearer and still gives A* a useful
        # input.
        if self.rows < 3 or self.columns < 3:
            walls = [
                [False for _ in range(self.columns)] for _ in range(self.rows)
            ]
            return Maze(
                (self.rows, self.columns),
                walls,
                (0, 0),
                (self.rows - 1, self.columns - 1),
            )

        walls = [[True for _ in range(self.columns)] for _ in range(self.rows)]
        lattice = [
            (row, column)
            for row in range(1, self.rows - 1, 2)
            for column in range(1, self.columns - 1, 2)
        ]

        # A 3x3 (or similarly narrow) matrix has a single lattice cell. In
        # that case an open matrix is the most useful generated maze.
        if len(lattice) < 2:
            walls = [
                [False for _ in range(self.columns)] for _ in range(self.rows)
            ]
            return Maze(
                (self.rows, self.columns),
                walls,
                (0, 0),
                (self.rows - 1, self.columns - 1),
            )

        start = self.random.choice(lattice)
        carved = {start}
        stack = [start]
        walls[start[0]][start[1]] = False

        while stack:
            current = stack[-1]
            row, column = current
            candidates = [
                (row - 2, column),
                (row, column + 2),
                (row + 2, column),
                (row, column - 2),
            ]
            candidates = [
                position
                for position in candidates
                if position in lattice and position not in carved
            ]
            if not candidates:
                stack.pop()
                continue

            next_position = self.random.choice(candidates)
            between = (
                (current[0] + next_position[0]) // 2,
                (current[1] + next_position[1]) // 2,
            )
            walls[between[0]][between[1]] = False
            walls[next_position[0]][next_position[1]] = False
            carved.add(next_position)
            stack.append(next_position)

        if self.loop_probability:
            self._add_loops(walls)

        open_cells = [
            (row, column)
            for row in range(self.rows)
            for column in range(self.columns)
            if not walls[row][column]
        ]
        start, goal = self._choose_endpoints(walls, open_cells)
        return Maze((self.rows, self.columns), walls, start, goal)

    def _add_loops(self, walls: list[list[bool]]) -> None:
        """Remove selected walls while retaining the generated structure."""

        for row in range(1, self.rows - 1):
            for column in range(1, self.columns - 1):
                if not walls[row][column] or self.random.random() > self.loop_probability:
                    continue
                adjacent_open = sum(
                    0 <= next_row < self.rows
                    and 0 <= next_column < self.columns
                    and not walls[next_row][next_column]
                    for next_row, next_column in (
                        (row - 1, column),
                        (row + 1, column),
                        (row, column - 1),
                        (row, column + 1),
                    )
                )
                # Opening a wall next to two corridors creates a loop without
                # making the maze almost completely open.
                if adjacent_open >= 2:
                    walls[row][column] = False

    @staticmethod
    def _choose_endpoints(
        walls: list[list[bool]], open_cells: list[Position]
    ) -> tuple[Position, Position]:
        """Choose connected endpoints that are far apart in the maze."""

        first = open_cells[0]
        farthest_from_first = MazeGenerator._farthest_cell(walls, first)[0]
        farthest_from_start = MazeGenerator._farthest_cell(
            walls, farthest_from_first
        )[0]
        return farthest_from_first, farthest_from_start

    @staticmethod
    def _farthest_cell(
        walls: list[list[bool]], start: Position
    ) -> tuple[Position, int]:
        distances = {start: 0}
        queue = [start]
        for position in queue:
            row, column = position
            for neighbor in (
                (row - 1, column),
                (row, column + 1),
                (row + 1, column),
                (row, column - 1),
            ):
                next_row, next_column = neighbor
                if (
                    0 <= next_row < len(walls)
                    and 0 <= next_column < len(walls[0])
                    and not walls[next_row][next_column]
                    and neighbor not in distances
                ):
                    distances[neighbor] = distances[position] + 1
                    queue.append(neighbor)

        return max(distances.items(), key=lambda item: item[1])
