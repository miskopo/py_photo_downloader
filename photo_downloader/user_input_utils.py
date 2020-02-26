from photo_downloader import logger


def confirm_validity() -> bool:
    while True:
        choice = input("Is this correct? [Y/n]: ") or "y"
        if choice.lower().startswith("y"):
            return True
        elif choice.lower().startswith("n"):
            return False


def numerical_choice(*, min: int, max: int, prompt: str) -> int:
    while True:
        try:
            choice: int = int(input(f"{prompt.strip()} "))
        except ValueError:
            logger.error("Invalid choice, try again")
            continue
        else:
            if min <= choice <= max:
                return choice
            else:
                logger.error("Invalid choice, try again")
