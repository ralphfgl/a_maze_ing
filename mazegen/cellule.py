class Cellule:
    """Structure with cell data"""

    def __init__(
        self,
        visited: bool = False,
        wall: int = 15,
        enter: bool = False,
        passdir: str = "",
        static: bool = False,
        greenline: bool = False,
        line: bool = False,
        vis: bool = False,
    ) -> None:
        self.visited: bool = visited
        self.wall: int = wall
        self.enter: bool = enter
        self.passdir: str = passdir
        self.static: bool = static
        self.greenline = greenline
        self.line = line
        self.vis = vis
