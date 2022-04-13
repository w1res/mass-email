from rich import print


def ascii() -> str:
    """Print ASCII on screen"""

    file_path: str = "src/interface/ascii.txt"

    with open(file_path) as ascii_file:
        content_ascii = ascii_file.read()

        print(f"[magenta][b]{content_ascii}[/][/]")
