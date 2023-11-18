import sys
import os
import subprocess
from subprocess import Popen, PIPE
import threading
import time


class LocalShell(object):
    def __init__(self):

        # Get the name of the operating system
        os_name = os.name
        self.encoder = 'utf-8'

        if os_name == 'nt':
            # Windows OS detected
            self.encoder = 'cp437'
        
        self.process = None

    def run(self):
        env = os.environ.copy()
        self.process = Popen('python -i', stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT, shell=True, env=env)
        sys.stdout.write("Started Local Terminal...\r\n\r\n")

        def listen():
            while True:
                # print("read data: ")
                data = self.process.stdout.read()
                if not data:
                    print("ENDED COMMMAND")
                    break
                # sys.stdout.write(data)
                print(data)
                sys.stdout.flush()
                if data == '>':
                    # print("COMPLETED CMD COMMAND")
                    pass

        writer = threading.Thread(target=listen)
         # Give the thread time to initialize
        time.sleep(1)
        # Daemon threads can be abruptly interrupted (program does not wait for them to finish in order to close)
        # writer.daemon = True
        writer.start()

    def _write(self, message):
        self.process.stdin.write(message)
        self.process.stdin.flush()

    def kill(self):
        self.process.kill()


shell = LocalShell()
shell.run()
shell._write("print('Hello from nested subprocess!')\n".encode())
shell._write("print('Hello from nested subprocess!')\n".encode())
shell._write("exit()\n".encode())
# shell._write("exit\n".encode())
# time.sleep(5)
shell.kill()