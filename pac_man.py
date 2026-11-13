
if __name__ == "__main__":
    try:
        import sys
        import logging
        from src.cli import command_line
        from src.config import load_config
        from src.app import App
        logging.basicConfig(
            level=logging.INFO, 
            format="%(levelname)s: %(message)s")
        config_content = command_line()
        config = load_config(config_content)
        api = App(config)
        api.run()
    except OSError as e:
        print(e, file=sys.stderr)
    except ValueError as e:
        print(e, file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
