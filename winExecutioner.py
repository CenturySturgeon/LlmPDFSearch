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
        self.process = Popen('cmd', stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def writeall():
            while True:
                # print("read data: ")
                data = self.process.stdout.read(1).decode("cp437")
                if not data:
                    break
                sys.stdout.write(data)
                sys.stdout.flush()

        writer = threading.Thread(target=writeall)
        writer.start()

        # try:
        #     while True:
        #         d = sys.stdin.read(1)
        #         if not d:
        #             break
        #         self._write(p, d.encode(encoding="cp437"))

        # except EOFError:
        #     pass

    def _write(self, message):
        self.process.stdin.write(message)
        self.process.stdin.flush()

    def kill(self):
        self.process.kill()


shell = LocalShell()
shell.run()
shell._write("systeminfo\n".encode())