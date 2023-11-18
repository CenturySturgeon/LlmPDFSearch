import subprocess
import time

# Create subprocess
process = subprocess.Popen('python -i', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# List of example commands to execute in the Python interactive shell
commands = [
    "print('Hello, World!')\n",
    "print('Hello, World!')\n",
    "exit()\n",
]

# Send commands to the interactive shell
for cmd in commands:
    process.stdin.write(cmd)
    process.stdin.flush()

# Close the stdin to signal that no more input will be sent
# process.stdin.close()

# Read output from the subprocess
# for line in process.stdout:
#     print(line.strip())

time.sleep(4)

print(process.stdout.readlines())

# Wait for the process to finish and get the return code
return_code = process.wait()

if return_code == 0:
    print("Commands executed successfully.")
else:
    print("Commands failed.")
