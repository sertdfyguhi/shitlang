import shitlang
import sys

if len(sys.argv) == 1:
    print('usage: python3 main.py [file]')
else:
    path = sys.argv[1]

    with open(path, 'r') as f:
        r = shitlang.run(f.read())
        if isinstance(r, shitlang.Error):
            print(r)