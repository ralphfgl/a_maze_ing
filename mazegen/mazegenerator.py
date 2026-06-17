from Parser import parse_config, ConfigFile
from abc import ABC, abstractmethod
from typing import List, Optional
import sys
import random


class Cellule:
    """Structure with cell data"""

    def __init__(
        self,
        visited: bool = False,
        wall: int = 15,
        enter: bool = False,
        passdir: str = "",
        static: bool = False,
        greenline: bool = False,
        line: bool = False,
        vis: bool = False,
    ) -> None:
        self.visited: bool = visited
        self.wall: int = wall
        self.enter: bool = enter
        self.passdir: str = passdir
        self.static: bool = static
        self.greenline = greenline
        self.line = line
        self.vis = vis


class MazeGeneration(ABC):
    """Interface for maze generation algorithm"""

    @abstractmethod
    def generate(self, conf: ConfigFile, themaze: List[List[Cellule]]) -> None:
        pass


class DFS(MazeGeneration):
    """Depth First Search algorithm"""

    def direc(self, pos: List, themaze: List[List[Cellule]]) -> str | bool:
        """Pick randomly an unvisited direction

        Args:
            pos: actual position on the grid
            themaze: array of Cellule
        """
        direction = ["N", "W", "E", "S"]
        if pos[1] == 0 or themaze[pos[1] - 1][pos[0]].visited is True:
            direction.remove("N")
        if pos[0] == 0 or themaze[pos[1]][pos[0] - 1].visited is True:
            direction.remove("W")
        if pos[0] == pos[2] - 1 or themaze[pos[1]][pos[0] + 1].visited is True:
            direction.remove("E")
        if pos[1] == pos[3] - 1 or themaze[pos[1] + 1][pos[0]].visited is True:
            direction.remove("S")
        if not direction:
            return False
        return random.choice(direction)

    def dor_gen_exit(self, pos: List, themaze: List[List[Cellule]]) -> None:
        """Open the wall in the cell that is entered

        Args:
            pos: actual position on the grid
            themaze: array of Cellule
        """

        if themaze[pos[1]][pos[0]].passdir == "N":
            themaze[pos[1]][pos[0]].wall &= 0b1011
        elif themaze[pos[1]][pos[0]].passdir == "W":
            themaze[pos[1]][pos[0]].wall &= 0b1101
        elif themaze[pos[1]][pos[0]].passdir == "E":
            themaze[pos[1]][pos[0]].wall &= 0b0111
        elif themaze[pos[1]][pos[0]].passdir == "S":
            themaze[pos[1]][pos[0]].wall &= 0b1110
        else:
            themaze[pos[1]][pos[0]].wall &= 0b1111

    def dor_gen_enter(self, pos: List, themaze: List[List[Cellule]]) -> None:
        """Open the wall in the cell that is entered

        Args:
            pos: actual position on the grid
            themaze: array of Cellule
        """

        if themaze[pos[1]][pos[0]].passdir == "N":
            themaze[pos[1]][pos[0]].wall &= 0b1110
        elif themaze[pos[1]][pos[0]].passdir == "W":
            themaze[pos[1]][pos[0]].wall &= 0b0111
        elif themaze[pos[1]][pos[0]].passdir == "E":
            themaze[pos[1]][pos[0]].wall &= 0b1101
        elif themaze[pos[1]][pos[0]].passdir == "S":
            themaze[pos[1]][pos[0]].wall &= 0b1011
        else:
            themaze[pos[1]][pos[0]].wall &= 0b1111

    def backtrack(self, pos: list, themaze: List[List[Cellule]]) -> None:
        """Recurse throught the grid to generate the maze

        Args:
            pos: starting position on the grid
            themaze: array of Cellule, modified in place by the algorithm
        """
        if themaze[pos[1]][pos[0]].visited is False:
            self.dor_gen_exit(pos, themaze)
            themaze[pos[1]][pos[0]].visited = True

        direction = self.direc(pos, themaze)
        while direction:
            if direction == "N":
                themaze[pos[1]][pos[0]].passdir = "N"
                self.dor_gen_enter(pos, themaze)
                pos[1] -= 1
                themaze[pos[1]][pos[0]].passdir = "N"
                self.backtrack(pos, themaze)
                pos[1] += 1
                direction = self.direc(pos, themaze)
            elif direction == "W":
                themaze[pos[1]][pos[0]].passdir = "W"
                self.dor_gen_enter(pos, themaze)
                pos[0] -= 1
                themaze[pos[1]][pos[0]].passdir = "W"
                self.backtrack(pos, themaze)
                pos[0] += 1
                direction = self.direc(pos, themaze)
            elif direction == "E":
                themaze[pos[1]][pos[0]].passdir = "E"
                self.dor_gen_enter(pos, themaze)
                pos[0] += 1
                themaze[pos[1]][pos[0]].passdir = "E"
                self.backtrack(pos, themaze)
                pos[0] -= 1
                direction = self.direc(pos, themaze)
            elif direction == "S":
                themaze[pos[1]][pos[0]].passdir = "S"
                self.dor_gen_enter(pos, themaze)
                pos[1] += 1
                themaze[pos[1]][pos[0]].passdir = "S"
                self.backtrack(pos, themaze)
                pos[1] -= 1
                direction = self.direc(pos, themaze)
        return

    def generate(self, conf: ConfigFile, themaze: List[List[Cellule]]) -> None:
        """Start the generation algorithm

        Args:
            conf: parameters extracted from the config.txt file
            themaze: array of Cellule
        """
        pos = [
            random.randint(0, conf.width - 1),
            random.randint(0, conf.height - 1),
            conf.width,
            conf.height,
        ]
        self.backtrack(pos, themaze)


class MazeSolver(ABC):
    """Interface for maze generation algorithm"""

    @abstractmethod
    def solve(
        self, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[str]:
        pass


class BFS(MazeSolver):
    """Breadth First Search algorithm"""

    def open_gate(self, room: int, way: str) -> bool:
        """Open wall of both cell of an edge"""

        if way == "N":
            if room & 0b1:
                return False
        elif way == "W":
            if (room >> 3) & 0b1:
                return False
        elif way == "E":
            if (room >> 1) & 0b1:
                return False
        elif way == "S":
            if (room >> 2) & 0b1:
                return False
        return True

    def direc(self, pos: List, themaze: List[List[Cellule]]) -> str | bool:
        """Pick randomly an unvisited direction, not obstructed by a wall

        Args:
            pos: actual position on the grid
            themaze: array of Cellule

        Returns:
            A direction (N, W, E, S) or False if no valid option
        """

        direction = ["N", "W", "E", "S"]
        if pos[1] == 0 or themaze[pos[1] - 1][pos[0]].enter is True:
            direction.remove("N")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "N") is False:
            direction.remove("N")
        if pos[0] == 0 or themaze[pos[1]][pos[0] - 1].enter is True:
            direction.remove("W")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "W") is False:
            direction.remove("W")
        if pos[0] == pos[2] - 1 or themaze[pos[1]][pos[0] + 1].enter is True:
            direction.remove("E")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "E") is False:
            direction.remove("E")
        if pos[1] == pos[3] - 1 or themaze[pos[1] + 1][pos[0]].enter is True:
            direction.remove("S")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "S") is False:
            direction.remove("S")
        if not direction:
            return False
        return random.choice(direction)

    def backtrack_line(
        self, pos: List, themaze: List[List], greenline: list, pos_exit: List
    ) -> None:
        if themaze[pos[1]][pos[0]].enter is False:
            themaze[pos[1]][pos[0]].enter = True
            if pos[0] == pos_exit[0] and pos[1] == pos_exit[1]:
                self.result = greenline.copy()
                pos[4] = True
        direction = self.direc(pos, themaze)
        while direction:
            if pos[4] is True:
                return
            greenline.append(direction)
            themaze[pos[1]][pos[0]].line = True
            if direction == "N":
                pos[1] -= 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[1] += 1
                direction = self.direc(pos, themaze)
            elif direction == "W":
                pos[0] -= 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[0] += 1
                direction = self.direc(pos, themaze)
            elif direction == "E":
                pos[0] += 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[0] -= 1
                direction = self.direc(pos, themaze)
            elif direction == "S":
                pos[1] += 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[1] -= 1
                direction = self.direc(pos, themaze)
            greenline.pop()
            themaze[pos[1]][pos[0]].line = False
        return

    def solve(
        self, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[str]:
        """Start the solving algorithm

        Args:
            conf: parameters extracted from the config.txt file
            themaze: array of Cellule
            greenline: solution path list
        """
        pos = [conf.entry[0], conf.entry[1], conf.width, conf.height, False]
        pos_exit = [conf.exit_[0], conf.exit_[1]]
        greenline = []
        self.result = []
        self.backtrack_line(pos, themaze, greenline, pos_exit)
        x, y = conf.entry[0], conf.entry[1]
        for direction in self.result:
            if direction == "N":
                y -= 1
            elif direction == "S":
                y += 1
            elif direction == "W":
                x -= 1
            elif direction == "E":
                x += 1
            themaze[y][x].line = True
        return self.result


class A_star:
    """A* solving algorithm.

    Use an heuristic function to guess the right direction."""

    def open_gate(self, room: int, way: str) -> bool:
        """Open wall of both cell of an edge"""
        if way == "N":
            if room & 0b1:
                return False
        elif way == "W":
            if (room >> 3) & 0b1:
                return False
        elif way == "E":
            if (room >> 1) & 0b1:
                return False
        elif way == "S":
            if (room >> 2) & 0b1:
                return False
        return True

    def direc(
        self, pos: List, themaze: List[List[Cellule]], direction: List
    ) -> List | bool:
        """Pick randomly an unvisited direction, not obstructed by a wall

        Args:
            pos: actual position on the grid
            themaze: array of Cellule

        Returns:
            A direction (N, W, E, S) or False if no valid option
        """
        if pos[1] == 0 or themaze[pos[1] - 1][pos[0]].enter is True:
            direction.remove("N")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "N") is False:
            direction.remove("N")
        if pos[0] == 0 or themaze[pos[1]][pos[0] - 1].enter is True:
            direction.remove("W")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "W") is False:
            direction.remove("W")
        if pos[0] == pos[2] - 1 or themaze[pos[1]][pos[0] + 1].enter is True:
            direction.remove("E")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "E") is False:
            direction.remove("E")
        if pos[1] == pos[3] - 1 or themaze[pos[1] + 1][pos[0]].enter is True:
            direction.remove("S")
        elif self.open_gate(themaze[pos[1]][pos[0]].wall, "S") is False:
            direction.remove("S")
        if not direction:
            return direction
        return direction[0]

    def faster(
        self, direction: List[str], pos: List, pos_exit: List
    ) -> List[str]:
        direction = ["N", "S", "E", "W"]
        long = pos[0] - pos_exit[0]
        height = pos[1] - pos_exit[1]
        if long > 0:
            direction[2] = "W"
            direction[3] = "E"
        if height > 0:
            direction[0] = "S"
            direction[1] = "N"
        if height == 0:
            temp = direction[0]
            direction[0] = direction[2]
            direction[2] = temp
            temp = direction[1]
            direction[1] = direction[3]
            direction[3] = temp
        return direction

    def backtrack_line(
        self,
        pos: List,
        themaze: List[List[Cellule]],
        greenline: List,
        pos_exit: List,
    ) -> None:
        if themaze[pos[1]][pos[0]].enter is False:
            themaze[pos[1]][pos[0]].enter = True
            if pos[0] == pos_exit[0] and pos[1] == pos_exit[1]:
                self.result = greenline.copy()
                pos[4] = True
        direction = self.faster(themaze, pos, pos_exit)
        direction = self.direc(pos, themaze, direction)
        while direction:
            if pos[4] is True:
                return
            greenline.append(direction)
            themaze[pos[1]][pos[0]].line = True
            if direction == "N":
                pos[1] -= 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[1] += 1
                direction = self.faster(direction, pos, pos_exit)
                direction = self.direc(pos, themaze, direction)
            elif direction == "W":
                pos[0] -= 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[0] += 1
                direction = self.faster(direction, pos, pos_exit)
                direction = self.direc(pos, themaze, direction)
            elif direction == "E":
                pos[0] += 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[0] -= 1
                direction = self.faster(direction, pos, pos_exit)
                direction = self.direc(pos, themaze, direction)
            elif direction == "S":
                pos[1] += 1
                self.backtrack_line(pos, themaze, greenline, pos_exit)
                pos[1] -= 1
                direction = self.faster(direction, pos, pos_exit)
                direction = self.direc(pos, themaze, direction)
            greenline.pop()
            themaze[pos[1]][pos[0]].line = False
        return

    def solve(
        self, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[str]:
        """Start the solving algorithm

        Args:
            conf: parameters extracted from the config.txt file
            themaze: array of Cellule
            greenline: solution path list
        """
        pos = [conf.entry[0], conf.entry[1], conf.width, conf.height, False]
        pos_exit = [conf.exit_[0], conf.exit_[1]]
        greenline = []
        self.result = []
        self.backtrack_line(pos, themaze, greenline, pos_exit)
        x, y = conf.entry[0], conf.entry[1]
        for direction in self.result:
            if direction == "N":
                y -= 1
            elif direction == "S":
                y += 1
            elif direction == "W":
                x -= 1
            elif direction == "E":
                x += 1
            themaze[y][x].line = True
        return self.result


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
                elif x == self.conf.exit_[0] and y == self.conf.exit_[1]:
                    middle += f"{left} 2 {right}"
                elif x == self.conf.entry[0] and y == self.conf.entry[1]:
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
