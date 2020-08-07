from photo_downloader import logger
import os

DIVIDER = min(80, int(os.popen('stty size', 'r').read().split()[1])) * "#"


def confirm_validity() -> bool:
    while True:
        choice = input("Is this correct? [Y/n]: ") or "y"
        if choice.lower().startswith("y"):
            return True
        elif choice.lower().startswith("n"):
            return False


def numerical_choice(*, min_value: int, max_value: int, prompt: str) -> int:
    while True:
        try:
            choice: int = int(input(f"{prompt.strip()} "))
        except ValueError:
            logger.error("Invalid choice, try again")
            continue
        else:
            if min_value <= choice <= max_value:
                return choice
            else:
                logger.error("Invalid choice, try again")
