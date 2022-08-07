import shitlang
import sys
import os

if len(sys.argv) == 1:
    print(f'usage: python3 {os.path.basename(__file__)} file [run directory]')
else:
    path = sys.argv[1]
    rundir = sys.argv[2] if len(sys.argv) >= 3 else None

    if not os.path.exists(path):
        print('error: file does not exist')
    elif os.path.isdir(path):
        print('error: cannot run directory')
    elif rundir and not os.path.exists(rundir):
        print('error: run directory does not exist')
    elif rundir and not os.path.isdir(rundir):
        print('error: run directory is not a directory')
    else:
        with open(path, 'r') as f:
            if rundir: os.chdir(rundir)

            r = shitlang.run(f.read(), os.path.basename(path))
            if isinstance(r, shitlang.Error):
                print(r)
