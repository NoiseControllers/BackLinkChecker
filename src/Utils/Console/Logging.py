from colorama import Fore, Style


def good(msg: str) -> None:
    print(Fore.GREEN + "[✓] " + msg + Style.RESET_ALL)


def bad(msg: str) -> None:
    print(Fore.RED + "[✗] " + msg + Style.RESET_ALL)


def info(msg: str) -> None:
    print(Fore.YELLOW + "[✓] " + msg + Style.RESET_ALL)
