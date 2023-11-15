import wexpect

# Replace this with the actual command you want to execute
command = "ping google.com"

# Spawn a command prompt and execute the specified command
child = wexpect.spawn(command)

# Expect for a certain pattern in the output
# In this case, we are expecting to see 'Reply' which is part of the output of 'ping' command
index = child.expect(['Reply', wexpect.EOF])

# Print the output
print(child.before)

# Close the child process
child.close()
