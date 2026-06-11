from io import open
from typing import List

# from readline import readline
import os
import sys


class Render:
    maze: List[List[int]] = []
    with open("output_maze.txt", "r") as f:
        for lines in f.readlines():
            maze.append([int(l, 16) for l in lines if l != "\n"])
    for y in range(len(maze)):
        row = maze[y]
        left: str = ""
        right: str = ""
        up: str = ""
        down: str = ""

        for x in range(len(row)):
            wall = row[x]
            if wall & 1:
                up += "/////"
            else:
                up += "/   /"
            if wall & 8:
                left = "/"
            else:
                left = " "
            if wall & 2:
                right = "/"
            else:
                right = " "
            if wall == 15:
                down += "/////"
            else:
                down += f"{left}   {right}"
        print(f"{up}")
        print(f"{down}")
    print("/////" * len(row))
