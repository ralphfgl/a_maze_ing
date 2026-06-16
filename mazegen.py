import random
from typing import List


def render(themaze):
    row: List = []
    wc = "█"
    for y in range(len(themaze)):
        row = themaze[y]
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


class Cellule:
    def __init__(self, visited=False, wall=15, enter=False, passdir=''):
        self.visited = visited
        self.wall = wall
        self.enter = enter
        self.passdir = passdir


def direc(pos, themaze):
    direction = ['N', 'W', 'E', 'S']
    if pos[1] == 0 or themaze[pos[1] - 1][pos[0]].visited is True:
        direction.remove('N')
    if pos[0] == 0 or themaze[pos[1]][pos[0] - 1].visited is True:
        direction.remove('W')
    if pos[0] == pos[2] - 1 or themaze[pos[1]][pos[0] + 1].visited is True:
        direction.remove('E')
    if pos[1] == pos[3] - 1 or themaze[pos[1] + 1][pos[0]].visited is True:
        direction.remove('S')
    if not direction:
        return False
    return random.choice(direction)


def dor_gen_exit(pos: list, themaze: list[list]):
    if themaze[pos[1]][pos[0]].passdir == 'N':
        themaze[pos[1]][pos[0]].wall &= 0b1011
    elif themaze[pos[1]][pos[0]].passdir == 'W':
        themaze[pos[1]][pos[0]].wall &= 0b1101
    elif themaze[pos[1]][pos[0]].passdir == 'E':
        themaze[pos[1]][pos[0]].wall &= 0b0111
    elif themaze[pos[1]][pos[0]].passdir == 'S':
        themaze[pos[1]][pos[0]].wall &= 0b1110
    else:
        themaze[pos[1]][pos[0]].wall &= 0b1111


def dor_gen_enter(pos: list, themaze: list[list]):
    if themaze[pos[1]][pos[0]].passdir == 'N':
        themaze[pos[1]][pos[0]].wall &= 0b1110
    elif themaze[pos[1]][pos[0]].passdir == 'W':
        themaze[pos[1]][pos[0]].wall &= 0b0111
    elif themaze[pos[1]][pos[0]].passdir == 'E':
        themaze[pos[1]][pos[0]].wall &= 0b1101
    elif themaze[pos[1]][pos[0]].passdir == 'S':
        themaze[pos[1]][pos[0]].wall &= 0b1011
    else:
        themaze[pos[1]][pos[0]].wall &= 0b1111


def backtrack(pos: list, themaze: list[list]) -> None:
    if themaze[pos[1]][pos[0]].visited is False:
        dor_gen_exit(pos, themaze)
        themaze[pos[1]][pos[0]].visited = True

    direction = direc(pos, themaze)
    while direction:
        if direction == 'N':
            themaze[pos[1]][pos[0]].passdir = 'N'
            dor_gen_enter(pos, themaze)
            pos[1] -= 1
            themaze[pos[1]][pos[0]].passdir = 'N'
            backtrack(pos, themaze)
            pos[1] += 1
            direction = direc(pos, themaze)
        elif direction == 'W':
            themaze[pos[1]][pos[0]].passdir = 'W'
            dor_gen_enter(pos, themaze)
            pos[0] -= 1
            themaze[pos[1]][pos[0]].passdir = 'W'
            backtrack(pos, themaze)
            pos[0] += 1
            direction = direc(pos, themaze)
        elif direction == 'E':
            themaze[pos[1]][pos[0]].passdir = 'E'
            dor_gen_enter(pos, themaze)
            pos[0] += 1
            themaze[pos[1]][pos[0]].passdir = 'E'
            backtrack(pos, themaze)
            pos[0] -= 1
            direction = direc(pos, themaze)
        elif direction == 'S':
            themaze[pos[1]][pos[0]].passdir = 'S'
            dor_gen_enter(pos, themaze)
            pos[1] += 1
            themaze[pos[1]][pos[0]].passdir = 'S'
            backtrack(pos, themaze)
            pos[1] -= 1
            direction = direc(pos, themaze)
    return


def genlitmaz(width: int, height: int) -> list[list]:
    themaze = []
    for j in range(height):
        linge = []
        for i in range(width):
            linge.append(Cellule())
        themaze.append(linge)
    return themaze


def forty_two(width: int, height: int, pos: list) -> list[list]:
    verif = False
    off_y = height // 2
    off_x = width // 2
    if pos[1] <= off_y + 2 and pos[1] >= off_y - 2:
        if pos[0] <= off_x + 3 and pos[0] >= off_x - 3 and pos[0] != off_x:
            verif = True
    if pos[1] <= off_y + 2 and pos[1] >= off_y + 1:
        if pos[0] >= off_x - 3 and pos[0] <= off_x - 2:
            verif = False
    if pos[1] == off_y + 1:
        if pos[0] <= off_x + 3 and pos[0] >= off_x + 2:
            verif = False
    if pos[1] == off_y - 1:
        if pos[0] == off_x + 2 or pos[0] == off_x + 1:
            verif = False
    if pos[1] == off_y - 1 or pos[1] == off_y - 2:
        if pos[0] == off_x - 2 or pos[0] == off_x - 1:
            verif = False
    return verif


def genbigmaz(width: int, height: int) -> list[list]:
    themaze = []
    for j in range(height):
        linge = []
        for i in range(width):
            if forty_two(width, height, [i, j]) is True:
                linge.append(Cellule(visited=True))
            else:
                linge.append(Cellule())
        themaze.append(linge)
    return themaze


def maze(width: int, height: int) -> list[list]:
    if width <= 8 or height <= 5:
        print("the labrint is too small to display 42")
        themaze = genlitmaz(width, height)
        pos = ([random.randint(0, width - 1), random.randint(0, height - 1),
                width, height])
    else:
        themaze = genbigmaz(width, height)
    pos = ([random.randint(0, width - 1), random.randint(0, height - 1),
            width, height])
    while forty_two(width, height, [pos[0], pos[1]]) is True:
        pos = ([random.randint(0, width - 1), random.randint(0, height - 1),
                width, height])
    backtrack(pos, themaze)
    return themaze


if __name__ == "__main__":
    s = maze(50, 50)
    render(s)
