IMAGE_CODE = '\033]1337;File=name=name;inline=true;:{}\a'


import base64
import tempfile
import sys
import termios
import tty
from IPython.terminal.pt_inputhooks import register



### Iterm 2 specific utils.


def _read_response():
    """
    Read bytes bytes until we got `n`
    """
    res = ''
    while True:
        res += sys.stdin.read(1)
        if res[-1] == 'n':
            break
    return res


def is_iterm2():
    """
    Iterm 2 is one of the terminal that support inline images.
    This code should properly detect if we are running in iterm2.

    It needs to be ran outside of prompt toolkit as it needs direct access to
    stdin/out.
    """
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
    try:
        tty.setraw(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        print('\x1b[1337n', end='')
        print('\x1b[5n', end='')
        sys.stdout.flush()
        res = _read_response()
        if not res.startswith('\x1b['):
            raise ValueError
        if 'ITERM2' in res:
            _read_response()
            return True
        else:
            return False

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return res


def imcat(image_data, metadata):
#     import subprocess
#     with tempfile.NamedTemporaryFile() as f:
#         f.write(image_data)
#         f.flush()
#         subprocess.run(['qlmanage', '-p', f.name])
    if isinstance(image_data, bytes):
        print(IMAGE_CODE.format(base64.encodebytes(image_data).decode()))
    elif isinstance(image_data, str):
        from warnings import warn
        warn('Image recieved a string, was supposed to get bytes !')
        print(IMAGE_CODE.format(image_data))
    else:
        raise ValueError('Unknown type', type(image_data))

def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example
    if is_iterm2():
        register('inline', None)
        ipython.mime_renderers['image/png'] = imcat
        ipython.mime_renderers['image/jpg'] = imcat
    else:
        print('can only handle ITerm2 for now')


