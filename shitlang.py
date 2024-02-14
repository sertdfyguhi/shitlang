from colorama import Fore, Style
import shitlang
import sys
import os

# bold ansi
BOLD = "\033[1m"

STDIN_FN = "<stdin>"
HELP = f"""\
{Fore.CYAN}shitlang interpreter
{Fore.YELLOW}made in python{Style.RESET_ALL}

{Fore.LIGHTGREEN_EX}usage:{Style.RESET_ALL}
    {BOLD}{Fore.CYAN}python3 {Fore.YELLOW}{os.path.basename(__file__)} {Fore.LIGHTGREEN_EX}[file]{Style.RESET_ALL}

    run without arguments to get stdin interpreter"""


def run_file():
    path = sys.argv[1]

    if not os.path.exists(path):
        print("error: file does not exist")
        exit(1)

    with open(path, "r") as f:
        ret = shitlang.run_file(path)
        if shitlang.is_SLerr(ret):
            print(ret)


def run_stdin():
    variables = shitlang.Variables(STDIN_FN)

    print(f"{Fore.CYAN}shitlang interpreter{Style.RESET_ALL}")

    while True:
        try:
            code = input(f"{BOLD}>>{Style.RESET_ALL} ")
        except KeyboardInterrupt:
            # ignore control + c exit
            exit(0)

        ret = shitlang.run(code, STDIN_FN, vars_=variables)
        if ret:
            print(ret)
        # if shitlang.is_SLerr(ret):
        #     print(ret)


if len(sys.argv) == 1:
    run_stdin()
elif sys.argv[1] in ["-h", "--help"]:
    print(HELP)
    exit(0)
else:
    run_file()
