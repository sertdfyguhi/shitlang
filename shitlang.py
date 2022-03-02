import shitlang
import sys
import os

if len(sys.argv) == 1:
    print(f'usage: python3 {os.path.basename(__file__)} [file]')
else:
    path = sys.argv[1]

    if not os.path.exists(path):
        print('error: file does not exist')
    elif os.path.isdir(path):
        print('error: cannot run folder')
    else:
        with open(path, 'r') as f:
            r = shitlang.run(f.read())
            if isinstance(r, shitlang.Error):
                print(r)
