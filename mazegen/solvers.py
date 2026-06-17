import random
from abc import ABC, abstractmethod
from typing import List
from .parser import ConfigFile
from .cellule import Cellule


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
