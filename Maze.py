from Parser import parse_config
from abc import ABC, abstractmethod
from typing import List
import sys
import random


class Cellule:
    def __init__(self, visited=False, wall=15, enter=False):
        self.visited = visited
        self.wall = wall
        self.enter = enter

class MazeGeneration(ABC):
    @abstractmethod
    def generate(self, width: int, height: int) -> List[List[Cellule]]:
        pass


class Depth_first_search(MazeGeneration):

    def direc(self, pos, themaze):
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

    def aleagen(self) -> str:
        pass

    def backtrack(self, pos: list, themaze: list[list], count: int) -> None:
        for b in themaze:
            for c in b:
                print(c.visited, end="")
            print()
        print()
        if themaze[pos[1]][pos[0]].visited is False:
            themaze[pos[1]][pos[0]].visited = True

        direction = self.direc(pos, themaze)
        while direction:
            if direction == "N":
                pos[1] -= 1
                self.backtrack(pos, themaze, count)
                pos[1] += 1
                direction = self.direc(pos, themaze)
            elif direction == "W":
                pos[0] -= 1
                self.backtrack(pos, themaze, count)
                pos[0] += 1
                direction = self.direc(pos, themaze)
            elif direction == "E":
                pos[0] += 1
                self.backtrack(pos, themaze, count)
                pos[0] -= 1
                direction = self.direc(pos, themaze)
            elif direction == "S":
                pos[1] += 1
                self.backtrack(pos, themaze, count)
                pos[1] -= 1
                direction = self.direc(pos, themaze)
        return

    def generate(self) -> List[List[Cellule]]:
        if width <= 8 or height <= 5:
        else:
            themaze = self.genbigmaz(self, width, height, count = 18)
        count += width * height
        pos = [
            random.randint(0, width - 1),
            random.randint(0, height - 1),
            width,
            height,
        ]
        self.backtrack(pos, themaze, count)
        return themaze


class MazeSolver(ABC):
    @abstractmethod
    def solve():
        pass


class MazeContext:
    def __init__(self, filename: str) -> None:
        self.conf = parse_config(filename)
        if self.conf.width <= 8 or self.conf.height <= 5:
            print("the labrint is too small to display 42")
            themaze = self.genlitmaz(self.conf.width, self.conf.height)
        else:
            themaze = self.genbigmaz(self.conf.width, self.conf.height)
        if self.conf.seed == None:
            self.conf.seed = random.randint(0, 9999999)
        algo = Depth_first_search()

    def genlitmaz(self, width: int, height: int) -> List[List[Cellule]]:
        themaze2 = [[Cellule() for _ in range(width)] for _ in range(height)]
        """
        themaze = []
        for _ in range(height):
            linge = []
            for _ in range(width):
                linge.append(Cellule())
            themaze.append(linge)
        return themaze
        """
        return themaze2

    def forty_two(self, width: int, height: int, pos: list) -> bool:
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
        wc: str = "█"
        row: List = []
        for y in range(len(self.themaze)):
            row = self.themaze[y]
            left: str = ""
            right: str = ""
            up: str = ""
            middle: str = ""

            for x in range(len(row)):
                wall = row[x]
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



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 Maze.py config.txt")
        exit(1)

    maze = MazeContext(sys.argv[1])
    print(f"{maze.conf}")

    a = maze(9, 9)
    for b in a:
        for c in b:
            print(c.visited, end="")
        print()
