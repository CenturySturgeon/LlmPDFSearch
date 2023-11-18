import sys
import os
import subprocess
from subprocess import Popen, PIPE
import threading
import time


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
                    print("ENDED COMMMAND")
                    break
                sys.stdout.write(data)
                sys.stdout.flush()
                if data == '>':
                    print("COMPLETED CMD COMMAND")

        writer = threading.Thread(target=writeall)
        writer.daemon = True
        writer.start()

    def _write(self, message):
        self.process.stdin.write(message)
        self.process.stdin.flush()

    def kill(self):
        self.process.kill()


shell = LocalShell()
shell.run()
shell._write("python -c \"print('Hello from nested subprocess!')\" \n".encode())
shell._write("python -c \"print('Hello from nested subprocess!')\" \n".encode())
time.sleep(5)