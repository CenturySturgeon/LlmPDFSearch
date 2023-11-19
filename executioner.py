import sys
import os
import subprocess
from subprocess import Popen, PIPE
import threading
import time


class LocalShell(object):
    def __init__(self):
        os_name = os.name
        self.encoder = 'utf-8'

        if os_name == 'nt':
            self.encoder = 'cp437'
        
        self.process = None
        self.command_completed = False  # Flag to indicate command completion
        self.commandOutput = ''

    def run(self):
        env = os.environ.copy()
        self.process = Popen('python -i', stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def listen():
            while True:
                data = self.process.stdout.read(1)  # Read line by line
                if not data:
                    print("ENDED PROCESS")
                    break
                # print(data.decode(self.encoder).strip())
                self.commandOutput += (data.decode(self.encoder))
                if b"\r" in data:
                    self.command_completed = True  # Set flag when command completes
                sys.stdout.flush()

        writer = threading.Thread(target=listen)
        time.sleep(1)
        writer.start()

    def _write(self, message):
        self.commandOutput = ''
        self.process.stdin.write(message)
        self.process.stdin.flush()
        self.command_completed = False  # Reset flag before sending a command

    def wait_for_command_completion(self):
        while not self.command_completed:
            time.sleep(0.1)  # Wait until the command is completed
        print("uaaaaaa")

    def kill(self):
        self.process.kill()


shell = LocalShell()
shell.run()
shell._write("print('Hello from nested subprocess!')\n".encode())
shell.wait_for_command_completion()  # Wait for the command to complete
# print(shell.commandOutput)
shell._write("import time\ntime.sleep(3)\nprint('Hello from nested subprocess!')\n".encode())
shell.wait_for_command_completion()  # Wait for the command to complete
print(shell.commandOutput)

shell._write("print('Hello from nested subprocess!')\n".encode())
shell.wait_for_command_completion()  # Wait for the command to complete
shell._write("exit()\n".encode())
shell.kill()
