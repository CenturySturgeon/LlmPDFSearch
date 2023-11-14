import subprocess

def execute_python_interactive(commands):
    try:
        # Construct the command to run Python in interactive mode with the specified commands
        python_command = '\n'.join(commands) + '\nexit()'

        # Run the Python command and capture the output
        result = subprocess.run(['python', '-i'], input=python_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the output
        print("Python Interactive Output:")
        print(result.stdout)
        
        # Print any errors, if present
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing Python interactive command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example: execute multiple commands in Python terminal
python_commands = [
    "print('Hello from inside the Python terminal')",
    "x = 42",
    "print('The value of x is:', x)"
]
execute_python_interactive(python_commands)
