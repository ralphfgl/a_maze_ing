import random

def aleagen() -> str:
    pass


def backtrack(pos: list, themaze: list[list], count: int) -> None:
    if count == 0:
        return

    for a in themaze:
        print(a)
    print("\n")
    if themaze[pos[0]][pos[1]] == 0:
        themaze[pos[0]][pos[1]] = 1
        count -= 1

    direction = ['N', 'W', 'E', 'S']
    if themaze[pos[0]][pos[1] - 1] == 1 or pos[1] == 0:
        direction.remove('N')
        print('N')
    if themaze[pos[0] - 1][pos[1]] == 1 or pos[0] == 0:
        direction.remove('W')
        print('W')
    if themaze[pos[0] + 1][pos[1]] == 1 or pos[0] == pos[2] - 1:
        direction.remove('E')
        print('E')
    if themaze[pos[0]][pos[1] + 1] == 1 or pos[1] == pos[3] - 1:
        direction.remove('S')
        print('S')
    direction = random.choice(direction)
    if direction == 'N':
        pos[1] -= 1
        backtrack(pos, themaze, count)
    elif direction == 'W':
        pos[0] -= 1
        backtrack(pos, themaze, count)
    elif direction == 'E':
        pos[0] += 1
        backtrack(pos, themaze, count)
    elif direction == 'S':
        pos[1] += 1
        backtrack(pos, themaze, count)
    else:
        return


def genlitmaz(width: int, height: int) -> list[list]:
    themaze = []
    for j in range(height):
        linge = []
        for i in range(width):
            linge.append(0)
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
                linge.append(1)
            else:
                linge.append(0)
        themaze.append(linge)
    return themaze


def maze(width: int, height: int) -> list[list]:
    count = 0
    if width <= 7 or height <= 8:
        print("the labrint is too small to display 42")
        themaze = genlitmaz(width, height)
    else:
        count = -18
        themaze = genbigmaz(width, height)
    count += width * height
    pos = [random.randint(0, width - 1), random.randint(0, height - 1), width, height]
    tabmaze = backtrack(pos, themaze, count)
    return tabmaze


if __name__ == "__main__":
    maze(2, 10)
