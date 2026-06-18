*This activity has been created as part of the 42 curriculum by rfeghali, sboucard.*

# A-MAZE-ING

## Description

A-MAZE-ING is a Python project that generates, solves, visualizes, and exports mazes. The project combines a reusable maze generation package (`mazegen`) with an interactive command-line application allowing users to generate new mazes, visualize solutions, change display colors, and export generated mazes.

The project was designed with reusability in mind. The maze generation logic is implemented as a standalone Python package that can be reused in future projects and installed independently.

### Goals

* Generate random mazes of customizable dimensions.
* Support reproducible generation through random seeds.
* Generate both perfect and cyclic mazes.
* Solve mazes using different pathfinding algorithms.
* Export generated mazes into a compact hexadecimal representation.
* Provide a reusable Python package for future projects.

---

# Features

## Maze Generation

* Random maze generation using the **Depth-First Search (DFS) Recursive Backtracking** algorithm.
* Configurable maze dimensions.
* Optional random seed for reproducible generation.
* Support for:

  * Perfect mazes (single unique path between any two cells).
  * Imperfect mazes with cycles.

## Maze Solving

Two solving algorithms are available:

* Breadth-First Search (BFS)
* A* (A-Star)

The solution path can be displayed directly inside the terminal rendering.

## Visualization

* ASCII rendering in terminal.
* Colored walls.
* Colored 42 pattern.
* Optional display of solution path.

## Export

Generated mazes can be exported into a hexadecimal wall representation containing:

* Maze structure
* Entry coordinates
* Exit coordinates
* Solution path

---

# Instructions

## Requirements

* Python 3.10+
* pip

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd a_maze_ing
```

Install the package:

```bash
make install
```

## Running the Application

Using the provided configuration file:

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

---

# Configuration File Format

The application uses a text configuration file.

Example:

```txt
WIDTH=24
HEIGHT=18
ENTRY=0,0
EXIT=22,15
OUTPUT_FILE=maze.txt
PERFECT=True

#SEED=42
#CYCLE_PROBABILITY=0.3
```

## Parameters

| Parameter         | Description                    |
| ----------------- | ------------------------------ |
| WIDTH             | Maze width                     |
| HEIGHT            | Maze height                    |
| ENTRY             | Entry coordinates (x,y)        |
| EXIT              | Exit coordinates (x,y)         |
| OUTPUT_FILE       | Output filename                |
| PERFECT           | True for perfect maze          |
| SEED              | Optional random seed           |
| CYCLE_PROBABILITY | Probability of creating cycles |

---

# Reusable Package: mazegen

The reusable part of the project is the `mazegen` package.

It contains:

* Maze generation logic
* Maze solving algorithms
* Configuration parsing and validation
* Maze data structures

The package can be installed independently and reused in future projects.

## Package Structure

```text
mazegen/
├── __init__.py
├── cellule.py
├── context.py
├── generators.py
├── parser.py
└── solvers.py
```

---

# Using MazeGenerator

## Basic Example

```python
from mazegen import MazeGenerator

maze = MazeGenerator("config.txt")

maze.render()
```

## Generating a New Maze

```python
maze.recreate()
```

Using a specific seed:

```python
maze.recreate(new_seed=42)
```

## Finding a Solution

```python
path = maze.find_solution()

print(path)
```

Example output:

```python
['E', 'E', 'S', 'S', 'W']
```

## Displaying the Solution

```python
maze.render(show_solution=True)
```

## Saving to a File

```python
maze.save_to_file("maze.txt")
```

---

# Accessing the Maze Structure

The generated maze is stored in:

```python
maze.themaze
```

This is a 2D list containing `Cellule` objects.

Example:

```python
cell = maze.themaze[0][0]

print(cell.wall)
print(cell.visited)
```

Each cell contains:

```python
wall
visited
enter
passdir
static
greenline
line
vis
```

---

# Accessing the Solution

The computed solution path is stored in:

```python
maze.solution_path
```

Example:

```python
print(maze.solution_path)
```

Output:

```python
['E', 'E', 'S', 'S', 'W']
```

---

# Maze Generation Algorithm

## Chosen Algorithm

Depth-First Search (DFS) Recursive Backtracking.

### Principle

1. Start from a random cell.
2. Mark the cell as visited.
3. Randomly choose an unvisited neighbour.
4. Remove the wall between both cells.
5. Continue recursively.
6. Backtrack when no unvisited neighbour remains.

### Advantages

* Simple implementation.
* Produces aesthetically pleasing mazes (long corridors).
* Generates perfect mazes naturally.
* Low memory consumption.
* Fast execution even on large grids.

### Why We Chose It

DFS Recursive Backtracking offers an excellent balance between implementation simplicity and maze quality. It produces long corridors and interesting exploration patterns while remaining efficient and easy to maintain.

---

# Solving Algorithms

## BFS

Breadth-First Search explores the maze layer by layer and guarantees finding a shortest path.

### Advantages

* Finds shortest path.
* Easy to understand.

## A*

A* uses a heuristic to prioritize cells closer to the exit.

### Advantages

* Usually faster than BFS.
* Reduces explored nodes.

---

# Packaging

The reusable package is distributed as:

```text
mazegen-1.0.0.tar.gz
```

and

```text
mazegen-1.0.0-py3-none-any.whl
```

The repository includes all required files for rebuilding the package:

---

# Team & Project Management

## Team Members

### rfeghali

* Design
* Parsing
* Packaging
* User interface
* Documentation

### sboucard

* Generation algorithm
* Solving algorithms (BFS, A*)
* Makefile

## Initial Planning

### Phase 1

* Maze data structure
* Configuration parser

### Phase 2

* DFS generation

### Phase 3

* Solvers

### Phase 4

* Interface and export

### Phase 5

* Packaging and documentation

## What Worked Well

* Clear separation between generation and solving.
* Modular architecture whith interface.

## What Could Be Improved

* Additional generation algorithms.
* Unit tests.
* Better rendering (using MLX or other python lib).

## Tools Used

* Git
* Python
* Pydantic
* Flake8
* MyPy
* Make

---

# Resources

## Maze Generation

* https://en.wikipedia.org/wiki/Maze_generation_algorithm
* https://en.wikipedia.org/wiki/Depth-first_search

## Pathfinding

* https://en.wikipedia.org/wiki/A*_search_algorithm
* https://en.wikipedia.org/wiki/Breadth-first_search

## Packaging

* https://packaging.python.org

## AI Usage

AI tools were used during the project for:

* Documentation drafting.
* Python packaging guidance.

All architecture decisions, algorithm implementations were performed by the project authors.

