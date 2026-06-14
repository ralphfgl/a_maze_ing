from Parser import parse_config
from abc import ABC, abstractmethod
from typing import List
import sys
import random


class MazeContext:
    def __init__(self, filename: str) -> None:
        self.conf = parse_config(filename)
        self.maze: List[List[int]] = self.init_maze()
        if self.conf.seed == None:
            self.conf.seed = random.randint(0, 9999999)

    def init_maze(self) -> List[List[int]]:
        pass

    def render(self):
        pass


class MazeGeneration(ABC):
    @abstractmethod
    def generate():
        pass


class MazeSolver(ABC):
    @abstractmethod
    def solve():
        pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 Maze.py config.txt")
        exit(1)

    maze = MazeContext(sys.argv[1])
    print(f"{maze.conf}")
