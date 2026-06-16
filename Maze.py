from Parser import parse_config, ConfigFile
from abc import ABC, abstractmethod
from typing import List
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
    ) -> None:
        self.visited: bool = visited
        self.wall: int = wall
        self.enter: bool = enter
        self.passdir: str = passdir


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
    def solve():
        pass


class MazeContext:
    """Implementation of a strategy design pattern and initialization"""

    def __init__(self, filename: str) -> None:
        self.conf = parse_config(filename)
        if self.conf.width <= 8 or self.conf.height <= 5:
            print("The maze is too small to display 42")
            self.themaze = self.genlitmaz(self.conf.width, self.conf.height)
        else:
            self.themaze = self.genbigmaz(self.conf.width, self.conf.height)
        if self.conf.seed == None:
            self.conf.seed = random.randint(0, 9999999)
        self.algo = DFS()
        self.algo.generate(self.conf, self.themaze)

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
                    linge.append(Cellule(visited=True))
                else:
                    linge.append(Cellule())
            themaze.append(linge)
        return themaze

    def render(self):
        """Render the maze with Ascii characters"""

        row: List = []
        wc = "█"
        for y in range(len(self.themaze)):
            row = self.themaze[y]
            left: str = ""
            right: str = ""
            up: str = ""
            middle: str = ""

            for x in range(len(row)):
                wall = row[x].wall
                if wall & 1:
                    up += f"{wc}{wc}{wc}{wc}{wc}"
                else:
                    up += f"{wc}   {wc}"
                if wall & 8:
                    left = f"{wc}"
                else:
                    left = " "
                if wall & 2:
                    right = f"{wc}"
                else:
                    right = " "
                if wall == 15:
                    middle += f"{wc}{wc}{wc}{wc}{wc}"
                else:
                    middle += f"{left}   {right}"
            print(f"{up}")
            print(f"{middle}")
        print(f"{wc}{wc}{wc}{wc}{wc}" * len(row))

    def cyclic_maze(self):
        """Open wall to create cycle in the maze"""
        while i in len(self.themaze):
            while j in len(i):
                pass


"""
for each wall between adjacent cells:
    if wall exists and random() < loopChance:
        remove wall
"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 Maze.py config.txt")
        exit(1)

    maze = MazeContext(sys.argv[1])
    maze.render()
