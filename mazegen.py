import random


class Cellule:
    def __init__(self, visited=False, wall=15, enter=False):
        self.visited = visited
        self.wall = wall
        self.enter = enter


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


def aleagen() -> str:
    pass


def backtrack(pos: list, themaze: list[list], count: int) -> None:
    for b in themaze:
        for c in b:
            print(c.visited, end="")
        print()
    print()
    if themaze[pos[1]][pos[0]].visited is False:
        themaze[pos[1]][pos[0]].visited = True

    direction = direc(pos, themaze)
    while direction:
        if direction == 'N':
            pos[1] -= 1
            backtrack(pos, themaze, count)
            pos[1] += 1
            direction = direc(pos, themaze)
        elif direction == 'W':
            pos[0] -= 1
            backtrack(pos, themaze, count)
            pos[0] += 1
            direction = direc(pos, themaze)
        elif direction == 'E':
            pos[0] += 1
            backtrack(pos, themaze, count)
            pos[0] -= 1
            direction = direc(pos, themaze)
        elif direction == 'S':
            pos[1] += 1
            backtrack(pos, themaze, count)
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
    count = 0
    if width <= 8 or height <= 5:
        print("the labrint is too small to display 42")
        themaze = genlitmaz(width, height)
    else:
        count = -18
        themaze = genbigmaz(width, height)
    count += width * height
    pos = [random.randint(0, width - 1), random.randint(0, height - 1), width, height]
    backtrack(pos, themaze, count)
    return themaze


if __name__ == "__main__":
    a = maze(9, 9)
    for b in a:
        for c in b:
            print(c.visited, end="")
        print()
