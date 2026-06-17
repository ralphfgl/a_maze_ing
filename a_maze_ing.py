import random
import os
import sys

from mazegen import MazeContext, Cellule


def print_help():
    """Print available command"""
    print("\n" + "=" * 50 + "\n")
    print("COMMANDS:")
    print("  r     -> Recreate a new maze")
    print("  s     -> Show/hide solution path")
    print("  a     -> Change solving algorithm (BFS/A*)")
    print("  w     -> Change wall color")
    print("  p     -> Change path color")
    print("  h     -> Show this help")
    print("  q     -> Quit")
    print("=" * 50 + "\n")


def print_colors():
    """Print available colors"""
    print("\nAvailable colors:")
    print("  1=Red      2=Green    3=Yellow   4=Blue")
    print("  5=Magenta  6=Cyan     7=White")
    print("  (enter the code number)\n")


def main() -> None:
    """a_maze_ing main function"""

    if len(sys.argv) != 2:
        print(f"Usage: python3 a_maze_ing.py <config.txt>")
        sys.exit(1)
    maze = MazeContext(sys.argv[1])
    maze.render()
    maze.save_to_file(maze.conf.output_file)
    print(f"Maze saved to {maze.conf.output_file} with seed {maze.conf.seed}")

    show_solution = False
    running = True
    algorithms = ["BFS", "A_star"]
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
        print(f"Algorithm: {maze.solver_algo}")
        print("=" * 50)
        print()

        if show_solution:
            maze.render(show_solution=True)
        else:
            maze.render(show_solution=False)

        print(
            "\nCommands: [r]ecreate [s]olution [a]lgorithm [w]all_color [p]attern_color [h]elp [q]uit"
        )
        cmd = input("Enter command: ").strip().lower()
        if cmd == "r" or cmd == "recreate":
            new_seed = random.randint(0, 999999)
            maze.recreate(new_seed)
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

        elif cmd == "a" or cmd == "algorithm":
            algo_index = (algo_index + 1) % len(algorithms)
            maze.set_algo(algorithms[algo_index])
            maze.find_solution()
            print(f"\nSolving algorithm change to {maze.solver_algo}")
            input("\nPress Enter to continue...")

        elif cmd == "w" or cmd == "wall_color":
            print_colors()
            color = input("Enter wall color code: ").strip()
            maze.change_wall_color(color)
            input("\nPress Enter to continue...")

        elif cmd == "p" or cmd == "pattern_color":
            print_colors()
            color = input("Enter pattern color code: ").strip()
            maze.change_pattern_color(color)
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
