import random


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
        themaze[pos[1]][pos[0]].wall &= 1011
    if themaze[pos[1]][pos[0]].passdir == 'W':
        themaze[pos[1]][pos[0]].wall &= 1101
    if themaze[pos[1]][pos[0]].passdir == 'E':
        themaze[pos[1]][pos[0]].wall &= 111
    if themaze[pos[1]][pos[0]].passdir == 'S':
        themaze[pos[1]][pos[0]].wall &= 1110
    else:
        themaze[pos[1]][pos[0]].wall &= 1111


def dor_gen_enter(pos: list, themaze: list[list]):
    if themaze[pos[1]][pos[0]].passdir == 'N':
        themaze[pos[1]][pos[0]].wall &= 1101
    if themaze[pos[1]][pos[0]].passdir == 'W':
        themaze[pos[1]][pos[0]].wall &= 1011
    if themaze[pos[1]][pos[0]].passdir == 'E':
        themaze[pos[1]][pos[0]].wall &= 1110
    if themaze[pos[1]][pos[0]].passdir == 'S':
        themaze[pos[1]][pos[0]].wall &= 111
    else:
        themaze[pos[1]][pos[0]].wall &= 1111


def backtrack(pos: list, themaze: list[list]) -> None:
    if themaze[pos[1]][pos[0]].visited is False:
        dor_gen_exit(pos, themaze)
        themaze[pos[1]][pos[0]].visited = True

    direction = direc(pos, themaze)
    while direction:
        if direction == 'N':
            pos[1] -= 1
            themaze[pos[1]][pos[0]].passdir = 'N'
            dor_gen_enter(pos, themaze)
            backtrack(pos, themaze)
            pos[1] += 1
            direction = direc(pos, themaze)
        elif direction == 'W':
            pos[0] -= 1
            themaze[pos[1]][pos[0]].passdir = 'W'
            dor_gen_enter(pos, themaze)
            backtrack(pos, themaze)
            pos[0] += 1
            direction = direc(pos, themaze)
        elif direction == 'E':
            pos[0] += 1
            themaze[pos[1]][pos[0]].passdir = 'E'
            dor_gen_enter(pos, themaze)
            backtrack(pos, themaze)
            pos[0] -= 1
            direction = direc(pos, themaze)
        elif direction == 'S':
            pos[1] += 1
            themaze[pos[1]][pos[0]].passdir = 'S'
            dor_gen_enter(pos, themaze)
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


def genbigmaz(width: int, height: int) -> list[list]:
    themaze = []
    for j in range(height):
        linge = []
        for i in range(width):
            if forty_two(width, height, [j, i]) is True:
                linge.append(Cellule(visited=True))
            else:
                linge.append(Cellule())
        themaze.append(linge)
    return themaze


def maze(width: int, height: int) -> list[list]:
    if width <= 8 or height <= 5:
        print("the labrint is too small to display 42")
        themaze = genlitmaz(width, height)
        pos = [random.randint(0, width - 1), random.randint(0, height - 1), width, height]
    else:
        themaze = genbigmaz(width, height)
    pos = [random.randint(0, width - 1), random.randint(0, height - 1), width, height]
    while forty_two(width, height, [pos[0], pos[1]]) is False:
        pos = [random.randint(0, width - 1), random.randint(0, height - 1), width, height]
    backtrack(pos, themaze)
    return themaze


if __name__ == "__main__":
    maze(9, 9)
