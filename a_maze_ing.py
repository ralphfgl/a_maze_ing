import random
import os
import sys

from mazegen import mazegenerator
from mazegen import DFS, BFS, A_star
from mazegen import Parser


def print_help():
    """Print available command"""
    print("\n" + "=" * 50 + "\n")
    print("COMMANDS:")
    print("  r     - Recreate a new maze")
    print("  s     - Show/hide solution path")
    print("  a     - Change solving algorithm (BFS/A*)")
    print("  c     - Change wall color")
    print("  h     - Show this help")
    print("  q     - Quit")
    print("=" * 50 + "\n")


def main() -> None:
    """a_maze_ing main function"""

    if len(sys.argv) != 2:
        print(f"Usage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)
    maze = MazeContext(sys.argv[1])
    maze.create_maze()
    maze.save_to_file(maze.conf.outputfile)
    print(f"Maze saved to {maze.conf.output_file} with seed {maze.conf.seed}")

    show_solution = False
    wall_colors = ["█", "▓", "▒", "░", "▄", "▀", "■", "□"]
    color_index = 0
    running = True
    algorithms = ["BFS", "A*"]
    algo_index = 0

    while running:
        os.system("clear")

        print("=" * 50)
        print("Maze Generator")
        print("=" * 50)
        print(f"Size: {maze.conf.width}x{maze.conf.height}")
        print(f"Seed: {maze.conf.seed}")
        print(f"Perfect: {maze.conf.perfect}")
        print(f"Output: {maze.conf.output_file}")
        print(f"Solution: {'SHOWN' if show_solution else 'HIDDEN'}")
        print(f"Algorithm: {maze.solver_algorithm}")
        print(f"Wall color: '{wall_colors[color_index]}'")
        print("=" * 50)
        print()

        if show_solution:
            maze.render(show_solution=True)
        else:
            maze.render(show_solution=False)

        print("\nCommands: [r]ecreate [s]olution [c]olor [h]elp [q]uit")
        cmd = input("Enter command: ").strip().lower()
        if cmd == "r" or cmd == "recreate":
            new_seed = random.randint(0, 999999)
            maze.regenerate(new_seed)
            maze.find_solution()
            maze.save_to_file(maze.conf.output_file)
            show_solution = False
            print(f"\n New maze generated with seed {new_seed}")
            input("\nPress Enter to continue...")

        elif cmd == "s" or cmd == "solution":
            show_solution = not show_solution
            if show_solution and not maze.solution_path:
                maze.find_solution()
            status = "shown" if show_solution else "hidden"
            print(f"\nSolution {status}")

        elif cmd == "c" or cmd == "color":
            color_index = (color_index + 1) % len(wall_colors)
            maze.change_wall_color(wall_colors[color_index])
            print(f"\nColor changed to '{wall_colors[color_index]}")
            input("\nPress Enter to continue...")

        elif cmd == "a" or cmd == "algorithm":
            algo_index = (algo_index + 1) % len(algorithms)
            maze.set_algorithm(algorithms[algo_index])
            maze.find_solution()
            print(f"\nSolving algorithm change to {maze.solver_algorithm}")
            input("\nPress Enter to continue...")

        elif cmd == "h" or cmd == help:
            print_help()
            input("Press Enter to continue...")

        elif cmd == "q" or cmd == "quit" or cmd == exit:
            print("Program terminated.")
            running = False

        else:
            print(f"\nUnknown command : '{cmd}'")
            print("Type 'h' for help")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
