
if __name__ == "__main__":
    try:
        import sys
        import logging
        from src.maze.maze_loader import process_maze
        from src.cli import command_line
        from src.config import load_config
        from src.app import App
        logging.basicConfig(
            level=logging.INFO, 
            format="%(levelname)s: %(message)s")
        # config_content = command_line()
        # config = load_config(config_content)
        # grid = process_maze(
        #     config.levels[0].width,
        #     config.levels[0].height,
        #     config.seed)
        # # for row in grid.cells:
        # #     for cell in row:
        # #         print(f"{cell.walls} ", end="")
        # #     print()
        api = App()
        api.run()
    except OSError as e:
        print(e, file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)