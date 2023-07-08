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

        ret = shitlang.run(code, STDIN_FN, vars=variables)
        print(ret)
        # if shitlang.is_SLerr(ret):
        #     print(ret)
elif sys.argv[1] in ["-h", "--help"]:
    print(f"usage: python3 {os.path.basename(__file__)} file [run directory]")
    exit(0)
else:
    path = sys.argv[1]
    rundir = sys.argv[2] if len(sys.argv) >= 3 else None

    if not os.path.exists(path):
        print("error: file does not exist")
        exit(1)
    elif os.path.isdir(path):
        print("error: cannot run directory")
        exit(1)

    if rundir:
        if not os.path.exists(rundir):
            print("error: run directory does not exist")
            exit(1)
        elif not os.path.isdir(rundir):
            print("error: run directory is not a directory")
            exit(1)

    with open(path, "r") as f:
        if rundir:
            os.chdir(rundir)

        ret = shitlang.run(f.read(), os.path.basename(path))
        if shitlang.is_SLerr(ret):
            print(ret)
