import subprocess

def execute_command(command):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the output
        print("Command Output:")
        print(result.stdout)
        
        # Print any errors, if present
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example: execute 'ls' command
execute_command('ls')
