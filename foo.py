import os 
import pexpect 
from  textwrap import dedent
import sys
import datetime

print('Start', datetime.datetime.now())

ipy_prompt = r']:' #ansi color codes give problems matching beyond this
env = os.environ.copy()
env['IPY_TEST_SIMPLE_PROMPT'] = '1'


child = pexpect.spawn(sys.executable, ['-m', 'IPython', '--colors=nocolor'],
                        env=env)
child.timeout = 2

child.expect(ipy_prompt)
child.timeout = 0.4

for l in dedent("""
    def f(x):
        raise Exception
    gen = (f(x) for x in [0])
    for x in gen:
        pass""").splitlines():
    child.sendline(l)

def escape(str):
    return str.replace('[', '\[').replace(']','\]')
exp = 'In [4]: '
child.expect(escape(exp))
print(child.before.decode())
print(exp, end='')

child.sendline('%debug')
exp ='ipdb> '
child.expect(exp)
print(child.before.decode())
print(exp, end='')


child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')


child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')


child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')

child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')

child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')

child.sendline('u')
exp = 'ipdb> '
child.expect(exp)
print(child.before.decode(), end='')
print(exp, end='')



#########
i = 0
buff = []
try:
    for i in range(100): 
        buff.append(child.read(1))
except:
    pass

print(i, 'more characters:')
print('|'+b''.join(buff).decode()+'|')
#exp = 'pdb>'
#child.expect(exp)
print('== ok ==')

