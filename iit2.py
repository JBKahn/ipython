import sys


import termios
import tty


def is_iterm2():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    try:
        tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        print('\x1b[1337n')
        print('\x1b[5n')
        res = ''
        for i in range(20):
            res += (sys.stdin.read(1))
            if res[-1] == 'n':
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return res


print(repr(is_iterm2()))

