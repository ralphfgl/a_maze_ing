from .parser import parse_config, ConfigFile
from .generators import DFS
from .solvers import BFS, A_star
from .cellule import Cellule
from abc import ABC, abstractmethod
from typing import List, Optional
import sys
import random


class MazeContext:
    """Implementation of a strategy design pattern and initialization"""

    def __init__(self, filename: str) -> None:
        """Initialize maze params and launch the algos"""
        # get config and init maze
        self.conf = parse_config(filename)
        if self.conf.width <= 8 or self.conf.height <= 5:
            print("The maze is too small to display 42", file=sys.stderr)
            self.themaze = self.genlitmaz(self.conf.width, self.conf.height)
        else:
            self.themaze = self.genbigmaz(self.conf.width, self.conf.height)
        # init seed
        if self.conf.seed == None:
            self.conf.seed = random.randint(0, 9999999)
        # generate maze
        random.seed(self.conf.seed)
        self.algo = DFS()
        self.algo.generate(self.conf, self.themaze)
        if self.conf.perfect == False:
            if not self.conf.cycle_probability:
                self.conf.cycle_probability = 0.3
            self.cyclic_maze()
        self.wall_color = "█"
        self.solution_path = None
        self.solver_algo = "BFS"

    def genlitmaz(self, width: int, height: int) -> List[List[Cellule]]:
        themaze2 = [[Cellule() for _ in range(width)] for _ in range(height)]
        return themaze2

    def forty_two(self, width: int, height: int, pos: list) -> bool:
        """Check if position is in the 42 pattern

        Args:
            width, height: dimension of the grid
            pos: position checked
        Returns:
            True if the position is on the logo, False otherwise
        """
        verif = False
        ok = height // 2
        ok1 = width // 2
        if pos[0] <= ok + 2 and pos[0] >= ok - 2:
            if pos[1] <= ok1 + 3 and pos[1] >= ok1 - 3 and pos[1] != ok1:
                verif = True
        if pos[0] <= ok + 2 and pos[0] >= ok + 1:
            if pos[1] >= ok1 - 3 and pos[1] <= ok1 - 2:
                verif = False
        if pos[0] == ok + 1:
            if pos[1] <= ok1 + 3 and pos[1] >= ok1 + 2:
                verif = False
        if pos[0] == ok - 1:
            if pos[1] == ok1 + 2 or pos[1] == ok1 + 1:
                verif = False
        if pos[0] == ok - 1 or pos[0] == ok - 2:
            if pos[1] == ok1 - 2 or pos[1] == ok1 - 1:
                verif = False
        return verif

    def genbigmaz(self, width: int, height: int) -> list[list]:
        """Initialize the maze without the 42 pattern

        Args:
            width, height: x and y value of the grid

        Returns:
            Initialized maze grid, with a Cellule object instancied for each position
        """
        themaze = []
        for j in range(height):
            linge = []
            for i in range(width):
                if self.forty_two(width, height, [j, i]) is True:
                    linge.append(Cellule(visited=True, static=True))
                else:
                    linge.append(Cellule())
            themaze.append(linge)
        return themaze

    def render(self, show_solution: bool = False):
        """Render the maze with Ascii characters, optionally showing solution path"""

        row: List = []
        wc = "█"
        sc = "•"
        for y in range(len(self.themaze)):
            row = self.themaze[y]
            left: str = ""
            right: str = ""
            up: str = ""
            middle: str = ""

            for x in range(len(self.themaze[0])):
                cell = self.themaze[y][x]
                # is_on_path = cell.line if show_solution else False
                is_on_path = cell.line if True else False
                rc = sc if is_on_path else " "
                if cell.wall & 1:
                    up += f"{wc}{wc}{wc}{wc}{wc}"
                else:
                    up += f"{wc}   {wc}"
                left = f"{wc}" if (cell.wall & 8) else " "
                right = f"{wc}" if (cell.wall & 2) else " "
                if cell.wall == 15:
                    middle += f"{wc}{wc}{wc}{wc}{wc}"
                elif (
                    x == self.conf.exit_[0]
                    and y == self.conf.exit_[1]
                    and show_solution
                ):
                    middle += f"{left} 2 {right}"
                elif (
                    x == self.conf.entry[0]
                    and y == self.conf.entry[1]
                    and show_solution
                ):
                    middle += f"{left} 1 {right}"
                else:
                    middle += f"{left} {rc} {right}"
            print(f"{up}")
            print(f"{middle}")
        print(f"{wc}{wc}{wc}{wc}{wc}" * len(row))

    def to_hex_wall(self) -> str:
        """Convert maze to hexadecimal wall representation"""
        if not self.themaze:
            return ""

        hex_lines = []
        for y in range(len(self.themaze)):
            line = ""
            for x in range(len(self.themaze[y])):
                hex_char = format(self.themaze[y][x].wall, "X")
                line += hex_char
            hex_lines.append(line + "\n")

        return "".join(hex_lines)

    def save_to_file(self, filename: str) -> None:
        """Save maze to file in hexa wall representation"""
        with open(filename, "w") as f:
            f.write(self.to_hex_wall())

    def cyclic_maze(self) -> None:
        """Open wall to create cycle in the maze"""
        for y in range(len(self.themaze) - 1):
            for x in range(len(self.themaze[y])):
                if (
                    self.themaze[y][x].wall & 0b0100
                    and random.random() < self.conf.cycle_probability
                    and self.themaze[y][x].static == False
                    and self.themaze[y + 1][x].static == False
                ):
                    self.themaze[y][x].wall &= 0b1011
                    self.themaze[y + 1][x].wall &= 0b1110

        for y in range(len(self.themaze)):
            for x in range(len(self.themaze[y]) - 1):
                if (
                    self.themaze[y][x].wall & 0b0010
                    and random.random() < self.conf.cycle_probability
                    and self.themaze[y][x].static == False
                    and self.themaze[y][x + 1].static == False
                ):
                    self.themaze[y][x].wall &= 0b1101
                    self.themaze[y][x + 1].wall &= 0b0111

    def change_wall_color(self, color_char: str) -> None:
        """Change wall color for rendering."""
        self.wall_color

    def recreate(self, new_seed: Optional[int] = None) -> None:
        """Recreate a new maze from a different seed."""
        if new_seed is not None:
            self.conf.seed = new_seed
        else:
            self.conf.seed = random.randint(0, 9999999)
        if self.conf.width <= 8 or self.conf.height <= 5:
            self.themaze = self.genlitmaz(self.conf.width, self.conf.height)
        else:
            self.themaze = self.genbigmaz(self.conf.width, self.conf.height)
        self.algo = DFS()
        self.algo.generate(self.conf, self.themaze)
        if not self.conf.perfect:
            self.cycle_probability = 0.3
            self.cyclic_maze()
        self.solution_path = None

    def find_solution(self) -> List[str]:
        """Find solution path using A* or BFS algo"""

        if self.solver_algo == "A*":
            solver = A_star()
        else:
            solver = BFS()
        path = solver.solve(self.conf, self.themaze)
        return path

    def set_algo(self, algo: str) -> None:
        """Change the solving algorithm"""

        if algo in ["BFS", "AStar"]:
            self.solver_algorithm = algo
            self.solution_path = None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 Maze.py config.txt")
        exit(1)

    maze = MazeContext(sys.argv[1])
    maze.render()
