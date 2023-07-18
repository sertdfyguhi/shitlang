import shitlang
import sys
import os

STDIN_FN = "<stdin>"
HELP = f"""\
\033[1mshitlang interpreter\033[m
made in python

usage:
    python3 {os.path.basename(__file__)} [file]

    run without file to get stdin interpreter"""


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

    print("\033[1m== shitlang interpreter ==\033[m")

    while True:
        try:
            code = input(">> ")
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
