import mazegen

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


def direc(pos, themaze, direction):
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
    if not direction:
        return direction
    return direction[0]


def faster(direction: list, pos: list) -> list:
    direction = ['N', 'S', 'E', 'W']
    long = pos[0] - pos[5]
    height = pos[1] - pos[6]
    if long > 0:
        direction[2] = 'W'
        direction[3] = 'E'
    if height > 0:
        direction[0] = 'S'
        direction[1] = 'N'
    if long == 0:
        temp = direction[0]
        direction[0] = direction[2]
        direction[2] = temp
        temp = direction[1]
        direction[1] = direction[3]
        direction[3] = temp
    return direction


def backtrack_line(pos: list, themaze: list[list],
                   greenline: list) -> None:
    if themaze[pos[1]][pos[0]].enter is False:
        themaze[pos[1]][pos[0]].enter = True
        if pos[0] == pos[5] and pos[1] == pos[6]:
            print(greenline)
            pos[4] = True
    direction = faster(themaze, pos)
    direction = direc(pos, themaze, direction)
    while direction:
        if pos[4] is True:
            return
        greenline.append(direction)
        themaze[pos[1]][pos[0]].line = True
        if direction == 'N':
            pos[1] -= 1
            backtrack_line(pos, themaze, greenline)
            pos[1] += 1
            direction = faster(direction, pos)
            direction = direc(pos, themaze, direction)
        elif direction == 'W':
            pos[0] -= 1
            backtrack_line(pos, themaze, greenline)
            pos[0] += 1
            direction = faster(direction, pos)
            direction = direc(pos, themaze, direction)
        elif direction == 'E':
            pos[0] += 1
            backtrack_line(pos, themaze, greenline)
            pos[0] -= 1
            direction = faster(direction, pos)
            direction = direc(pos, themaze, direction)
        elif direction == 'S':
            pos[1] += 1
            backtrack_line(pos, themaze, greenline)
            pos[1] -= 1
            direction = faster(direction, pos)
            direction = direc(pos, themaze, direction)
        greenline.pop()
        themaze[pos[1]][pos[0]].line = False
    return


if __name__ == "__main__":
    lon = 10
    hau = 10
    possi = [0, 0, lon, hau, False, 1, 0]
    greenline = []
    s = mazegen.maze(possi[2], possi[3])
    mazegen.render(s)
    backtrack_line(possi, s, greenline)
