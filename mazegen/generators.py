import random
from abc import ABC, abstractmethod
from typing import List
from .parser import ConfigFile
from .cellule import Cellule


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
