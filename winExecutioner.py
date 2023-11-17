import pexpect
from pexpect.popen_spawn import PopenSpawn

command = 'cmd'
child = PopenSpawn(command)
child.expect('>')
child.sendline('help color')
child.expect('>')
output = child.before.decode("cp437")  # Decode the output from bytes to string
lines = output.splitlines()  # Split the output into separate lines

for line in lines:
    print(line)
