from .parser import parse_config
from .generators import DFS
from .solvers import BFS, A_star
from .cellule import Cellule
from typing import List, Optional
import sys
import random


class MazeGenerator:
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

        self.wall_color = "\033[37m"  # white
        self.pattern_color = "\033[32m"  # green
        self.reset_color = "\033[0m"
        self.colors = {
            "1": ("\033[31m", "Red"),
            "2": ("\033[32m", "Green"),
            "3": ("\033[33m", "Yellow"),
            "4": ("\033[34m", "Blue"),
            "5": ("\033[35m", "Magenta"),
            "6": ("\033[36m", "Cyan"),
            "7": ("\033[37m", "White"),
        }
        self.find_solution()

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
        wc = f"{self.wall_color}█{self.reset_color}"
        sc = "•"

        pattern_ch = f"{self.pattern_color}█{self.reset_color}"
        for y in range(len(self.themaze)):
            row = self.themaze[y]
            left: str = ""
            right: str = ""
            up: str = ""
            middle: str = ""

            for x in range(len(self.themaze[0])):
                cell = self.themaze[y][x]
                is_on_path = cell.line if show_solution else False
                is_pattern = cell.static
                if is_pattern:
                    wd = pattern_ch
                else:
                    wd = wc
                rc = sc if is_on_path else " "
                if cell.wall & 1:
                    up += f"{wd}{wd}{wd}{wd}{wd}"
                else:
                    up += f"{wd}   {wd}"
                left = f"{wd}" if (cell.wall & 8) else " "
                right = f"{wd}" if (cell.wall & 2) else " "
                if cell.wall == 15:
                    middle += f"{wd}{wd}{wd}{wd}{wd}"
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
                elif show_solution:
                    middle += f"{left} {rc} {right}"
                else:
                    middle += f"{left}   {right}"
            print(f"{up}")
            print(f"{middle}")
        print(f"{wd}{wd}{wd}{wd}{wd}" * len(row))

    def change_wall_color(self, color_code: str) -> None:
        """Change wall color with ANSI code"""

        if color_code in self.colors:
            self.wall_color = self.colors[color_code][0]
            print(f"Wall color changed to {self.colors[color_code][1]}")
        else:
            print(
                f"Invalid color code. Available: {', '.join(self.colors.keys())}"
            )

    def change_pattern_color(self, color_code: str) -> None:
        """Change color of solution path."""

        if color_code in self.colors:
            self.pattern_color = self.colors[color_code][0]
            print(f"Pattern color changed to {self.colors[color_code][1]}")
        else:
            print(
                f"Invalid color code. Available: {', '.join(self.colors.keys())}"
            )

    def to_hex_wall(self) -> str:
        """Convert maze to hexadecimal wall representation"""

        hex_lines = []
        for y in range(len(self.themaze)):
            line = ""
            for x in range(len(self.themaze[y])):
                hex_char = format(self.themaze[y][x].wall, "X")
                line += hex_char
            hex_lines.append(line + "\n")

        hex_lines.append("\n")
        hex_lines.append(f"{self.conf.entry[0]},{self.conf.entry[1]}\n")
        hex_lines.append(f"{self.conf.exit_[0]},{self.conf.exit_[1]}\n")
        if self.solution_path:
            path_str = "".join(self.solution_path)
        else:
            self.find_solution()
            print(self.solution_path)
            path_str = (
                "".join(self.solution_path) if self.solution_path else ""
            )
        hex_lines.append(path_str + "\n")

        return "".join(hex_lines)

    def save_to_file(self, filename: str) -> None:
        """Save maze to file in hexa wall representation"""
        if not self.solution_path:
            self.solution_path
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

        for y in range(len(self.themaze)):
            for x in range(len(self.themaze[y])):
                self.themaze[y][x].line = False
                self.themaze[y][x].enter = False

        if self.solver_algo == "A_star":
            solver = A_star()
        else:
            solver = BFS()
        self.solution_path = solver.solve(self.conf, self.themaze)
        return self.solution_path

    def set_algo(self, algo: str) -> None:
        """Change the solving algorithm"""

        if algo in ["BFS", "A_star"]:
            self.solver_algo = algo
            self.solution_path = None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 Maze.py config.txt")
        exit(1)

    maze = MazeContext(sys.argv[1])
    maze.render()
