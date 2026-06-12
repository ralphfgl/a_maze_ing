import random

def aleagen() -> str:


def backtrack(pos: list, themaze: list[list], count: int) -> None:
    if count == 0:
        return

    if themaze[pos[0]][pos[1]] == 0:
        themaze[pos[0]][pos[1]] = aleagen()
        count -= 1
    
    direction = ['N','W','E','S']
    if themaze[pos[0] - 1][pos[1]] == 1 or pos[0] == 0:
        direction.remove('N')
    if themaze[pos[0]][pos[1] - 1] == 1 or pos[1] == 0:
        direction.remove('W')
    if themaze[pos[0]][pos[1] + 1] == 1 or pos[1] == pos[3]:
        direction.remove('E')
    if themaze[pos[0] + 1][pos[1]] == 1 or pos[0] == pos[2]:
        direction.remove('S')
    direction = random.choice(direction)
    if direction == 'N':
        pos[0] -= 1
        backtrack(pos, themaze, count)
    elif direction == 'W':
        pos[1] -= 1
        backtrack(pos, themaze, count)
    elif direction == 'E':
        pos[1] += 1
        backtrack(pos, themaze, count)
    elif direction == 'S':
        pos[0] += 1
        backtrack(pos, themaze, count)
    else:
        return


def genlitmaz(width: int, height: int) -> list[list]:
    themaze = []
    for i in range(height + 1):
        for j in range(width + 1):
            themaze[i][j] = 0
    return themaze

def genbigmaz(width: int, height: int) -> list[list]:
    for i in height:
        j = 0
        for j in width:
            themaze = [i][j] = 0
            j += 1
        i += 1
    return themaze

def maze(width: int, height: int) -> list[list]:
    if width <= 7 or height <= 8:
        print("the labrint is too small to display 42")
        themaze = genlitmaz(width, height)
    else:
        count = -18
        themaze = genbigmaz(width, height)
    count += width * height
    pos = [random.randint(0, width), random.randint(0, height), height, width]
    tabmaze = backtrack(pos, themaze, count)
    return tabmaze
