from maze_solver import Maze, MazeGenerator


def test_maze_accepts_square_and_rectangular_sizes() -> None:
    square = Maze(5)
    rectangle = Maze((3, 7))

    assert square.size == (5, 5)
    assert rectangle.size == (3, 7)
    assert square.start == (0, 0)
    assert square.goal == (4, 4)


def test_maze_neighbors_only_include_walkable_cells() -> None:
    walls = [
        [False, False, True],
        [True, False, False],
        [False, False, False],
    ]
    maze = Maze((3, 3), walls, start=(0, 0), goal=(2, 2))

    assert set(maze.neighbors((0, 0))) == {(0, 1)}
    assert set(maze.neighbors((1, 1))) == {(0, 1), (1, 2), (2, 1)}


def test_generator_is_reproducible_and_has_valid_endpoints() -> None:
    first = MazeGenerator((11, 15), seed=42).generate()
    second = MazeGenerator((11, 15), seed=42).generate()

    assert first.render() == second.render()
    assert first.is_walkable(first.start)
    assert first.is_walkable(first.goal)
