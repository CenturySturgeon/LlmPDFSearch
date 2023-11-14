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

# x = subprocess.check_output(['ls', '-l']).decode('utf-8')
# print(x)
llmCommand = ['/Users/jgras/Ai/llama.cpp/main -m /Users/jgras/Ai/models/mistral-7b-v0.1.Q4_K_M.gguf \
  --color \
  --ctx_size 2048 \
  -n -1 \
  -ins -b 128 \
  --top_k 10000 \
  --temp 0.2 \
  --repeat_penalty 1.1 \
  --n-gpu-layers 30 \
  -t 8']
process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(llmCommand[0].encode())
# myout, juan = process.communicate('ls -la'.encode())

print(out)