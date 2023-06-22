import colorama


def highlight_foreground(text, color):
    return f"{color}{text}{colorama.Fore.RESET}"


def highlight_good(text):
    return highlight_foreground(text, colorama.Fore.LIGHTGREEN_EX)


def highlight_bad(text):
    return highlight_foreground(text, colorama.Fore.BLUE)


def highlight_warning(text):
    return highlight_foreground(text, colorama.Fore.CYAN)
