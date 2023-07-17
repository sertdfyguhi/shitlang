import shitlang
import sys
import os

STDIN_FN = "<stdin>"

if len(sys.argv) == 1:
    variables = shitlang.Variables(STDIN_FN)

    print("\033[1m== SHITLANG interpreter ==\033[m")

    while True:
        try:
            code = input("> ")
        except KeyboardInterrupt:
            # ignore control + c exit
            exit(0)

        ret = shitlang.run(code, STDIN_FN, vars_=variables)
        if ret[-1]:
            print(ret[-1])
        # if shitlang.is_SLerr(ret):
        #     print(ret)
elif sys.argv[1] in ["-h", "--help"]:
    print(
        f"""\
\033[1mshitlang interpreter v1.0\033[m
made in python

usage:
    python3 {os.path.basename(__file__)} [file]

    run without file to get stdin interpreter"""
    )
    exit(0)
else:
    path = sys.argv[1]

    if not os.path.exists(path):
        print("error: file does not exist")
        exit(1)

    with open(path, "r") as f:
        ret = shitlang.run_file(path)
        if shitlang.is_SLerr(ret):
            print(ret)
