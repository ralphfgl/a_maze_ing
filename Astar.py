import mazegen
import random


class Cellule:
    def __init__(self, visited=False, wall=15, enter=False, passdir='',
                 grenline=False, line=False, vis=False):
        self.visited = visited
        self.wall = wall
        self.enter = enter
        self.passdir = passdir
        self.grenline = grenline
        self.line = line
        self.vis = vis


def open_gate(room, way) -> bool:
    if way == 'N':
        if room & 0b1:
            return False
    elif way == 'W':
        if (room >> 3) & 0b1:
            return False
    elif way == 'E':
        if (room >> 1) & 0b1:
            return False
    elif way == 'S':
        if (room >> 2) & 0b1:
            return False
    return True


def direc(pos, themaze):
    direction = ['N', 'W', 'E', 'S']
    if pos[1] == 0 or themaze[pos[1] - 1][pos[0]].enter is True:
        direction.remove('N')
    elif open_gate(themaze[pos[1]][pos[0]].wall, 'N') is False:
        direction.remove('N')
    if pos[0] == 0 or themaze[pos[1]][pos[0] - 1].enter is True:
        direction.remove('W')
    elif open_gate(themaze[pos[1]][pos[0]].wall, 'W') is False:
        direction.remove('W')
    if pos[0] == pos[2] - 1 or themaze[pos[1]][pos[0] + 1].enter is True:
        direction.remove('E')
    elif open_gate(themaze[pos[1]][pos[0]].wall, 'E') is False:
        direction.remove('E')
    if pos[1] == pos[3] - 1 or themaze[pos[1] + 1][pos[0]].enter is True:
        direction.remove('S')
    elif open_gate(themaze[pos[1]][pos[0]].wall, 'S') is False:
        direction.remove('S')
    return direction


def faster(direction: list, pos: list) -> list:
    if len(direction) > 1:
        long = pos[0] - pos[5]
        if long > 0:
            if 'E' in direction and 'W' in direction:
                direction.remove('E')
        elif long < 0:
            if 'E' in direction and 'W' in direction:
                direction.remove('W')
        height = pos[1] - pos[6]
        if height > 0:
            if 'N' in direction and 'S' in direction:
                direction.remove('N')
        elif height < 0:
            if 'N' in direction and 'S' in direction:
                direction.remove('S')
        elif long == 0 and 'N' in direction or 'S' in direction:
            if 'E' in direction:
                direction.remove('E')
            if 'W' in direction:
                direction.remove('W')
        elif height == 0 and 'E' in direction or 'W' in direction:
            if 'N' in direction:
                direction.remove('N')
            if 'S' in direction:
                direction.remove('S')
        return random.choice(direction)
    return direction


def backtrack_line(pos: list, themaze: list[list],
                   greenline: list) -> None:
    if themaze[pos[1]][pos[0]].enter is False:
        themaze[pos[1]][pos[0]].enter = True
        if pos[0] == pos[5] and pos[1] == pos[6]:
            print(greenline)
            pos[4] = True
    direction = direc(pos, themaze)
    direction = faster(direction, pos)
    while direction:
        if pos[4] is True:
            return
        greenline.append(direction)
        themaze[pos[1]][pos[0]].line = True
        if direction == 'N':
            pos[1] -= 1
            backtrack_line(pos, themaze, greenline)
            pos[1] += 1
            direction = direc(pos, themaze)
            direction = faster(direction, pos)
        elif direction == 'W':
            pos[0] -= 1
            backtrack_line(pos, themaze, greenline)
            pos[0] += 1
            direction = direc(pos, themaze)
            direction = faster(direction, pos)
        elif direction == 'E':
            pos[0] += 1
            backtrack_line(pos, themaze, greenline)
            pos[0] -= 1
            direction = direc(pos, themaze)
            direction = faster(direction, pos)
        elif direction == 'S':
            pos[1] += 1
            backtrack_line(pos, themaze, greenline)
            pos[1] -= 1
            direction = direc(pos, themaze)
            direction = faster(direction, pos)
        greenline.pop()
        themaze[pos[1]][pos[0]].line = False
    return


if __name__ == "__main__":
    lon = 10
    hau = 10
    possi = [0, 0, lon, hau, False, 3, 8]
    greenline = []
    s = mazegen.maze(possi[2], possi[3])
    mazegen.render(s)
    backtrack_line(possi, s, greenline)
