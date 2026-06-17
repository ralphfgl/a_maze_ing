from io import open
from typing import List

# from readline import readline
import os
import sys


class Render:
    maze: List[List[int]] = []
    wc: str = "█"
    try:
        with open("maze.txt", "r") as f:
            for lines in f.readlines():
                maze.append([int(l, 16) for l in lines if l != "\n"])
    except FileNotFoundError:
        print("File do not exist")
        exit(1)
    except PermissionError:
        print("Permission denied")
        exit(1)
    row: List = []
    for y in range(len(maze)):
        row = maze[y]
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
