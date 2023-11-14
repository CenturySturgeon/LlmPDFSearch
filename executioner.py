import sys
import os
import subprocess
from subprocess import Popen, PIPE
import threading


class LocalShell(object):
    def __init__(self):
        pass

    def run(self):
        env = os.environ.copy()
        self.process = Popen('/bin/bash', stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def writeall():
            while True:
                # print("read data: ")
                data = self.process.stdout.read(1).decode("utf-8")
                if not data:
                    print("Am I last")
                    break
                sys.stdout.write(data)
                sys.stdout.flush()
                # print(data)

        writer = threading.Thread(target=writeall)
        writer.start()

        # try:
        #     while True:
        #         d = sys.stdin.read(1)
        #         if not d:
        #             break
        #         self._write(self.process, d.encode())

        # except EOFError:
        #     pass
        # self._write( "ls\n".encode())

    def _write(self, message):
        self.process.stdin.write(message)
        self.process.stdin.flush()


# shell = LocalShell()
# shell.run()

# shell._write("ls\n".encode())
# shell._write("ls\n".encode())

x = subprocess.check_output(['ls', '-l'])
print(x)