import random
from abc import ABC, abstractmethod
from typing import List, Any
from .parser import ConfigFile
from .cellule import Cellule


class MazeSolver(ABC):
    """Interface for maze generation algorithm"""

    @abstractmethod
    def solve(
        self, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[str]:
        pass


class BFS(MazeSolver):
    """BFS implementation using a list as a queue"""

    def open_gate(self, room: int, way: str) -> bool:
        """Check if a wall is open in a given direction"""
        if way == "N":
            if room & 0b1:
                return False
        elif way == "W":
            if (room >> 3) & 0b1:
                return False
        elif way == "E":
            if (room >> 1) & 0b1:
                return False
        elif way == "S":
            if (room >> 2) & 0b1:
                return False
        return True

    def get_neighbors(
        self, x: int, y: int, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[tuple]:
        """Get all valid neighboring position (no walls, within bounds)"""
        neighbors = []
        directions = [
            ("N", 0, -1),
            ("S", 0, 1),
            ("W", -1, 0),
            ("E", 1, 0),
        ]
        for direction, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= conf.width or ny < 0 or ny <= conf.height:
                continue
            if self.open_gate(themaze[y][x].wall, direction):
                neighbors.append((nx, ny, direction))
        return neighbors

    def solve(
        self, conf: ConfigFile, themaze: List[List[Cellule]]
    ) -> List[str]:
        """True BFS using list as a queue"""
        start_x, start_y = conf.entry[0], conf.entry[1]
        exit_x, exit_y = conf.exit_[0], conf.exit_[1]

        # Queue implementation using list (FIFO)
        queue = [(start_x, start_y, [])]

        # Track visited positions
        visited = set()
        visited.add((start_x, start_y))

        # Head pointer for queue
        head = 0

        while head < len(queue):
            x, y, path = queue[head]
            head += 1

            # Check if we reached the exit
            if x == exit_x and y == exit_y:
                # Store the result path
                self.result = path

                # Mark the solution path for rendering (exactly like original solvers)
                x, y = conf.entry[0], conf.entry[1]
                for direction in self.result:
                    if direction == "N":
                        y -= 1
                    elif direction == "S":
                        y += 1
                    elif direction == "W":
                        x -= 1
                    elif direction == "E":
                        x += 1
                    themaze[y][x].line = True

                return self.result

            # Explore all neighbors
            for nx, ny, direction in self.get_neighbors(x, y, conf, themaze):
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = path + [direction]
                    queue.append((nx, ny, new_path))

        # No path found
        self.result = []
        return self.result


class A_star(MazeSolver):
    pass
