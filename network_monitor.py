import os
import time
import socket
import tkinter as tk
from threading import Thread
from colorama import init, Fore
import sys

# Initialize colorama for cross-platform compatibility
init(autoreset=True)

# Network check function
def is_connected(host="8.8.8.8", port=53, timeout=3):
    """
    Check if the network is connected by attempting to reach a host.
    Returns True if connected, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

# Function to update the UI with connection status
def update_status():
    if is_connected():
        status_label.config(text="Network is connected", fg="green")
        successful_connections.set(successful_connections.get() + 1)
    else:
        status_label.config(text="Network disconnected!", fg="red")
        disconnections.set(disconnections.get() + 1)

    successful_label.config(text=f"Successful Connections: {successful_connections.get()}")
    disconnection_label.config(text=f"Disconnections: {disconnections.get()}")

    # Schedule next check
    root.after(200, update_status)

# Create the main window
root = tk.Tk()
root.title("Network Monitor")
root.geometry("300x200")

# Labels to display connection stats
status_label = tk.Label(root, text="Checking network...", font=("Helvetica", 14))
status_label.pack(pady=10)

successful_connections = tk.IntVar(value=0)
successful_label = tk.Label(root, text=f"Successful Connections: {successful_connections.get()}")
successful_label.pack(pady=5)

disconnections = tk.IntVar(value=0)
disconnection_label = tk.Label(root, text=f"Disconnections: {disconnections.get()}")
disconnection_label.pack(pady=5)

# Start the network monitoring in a separate thread to keep the UI responsive
thread = Thread(target=update_status)
thread.daemon = True
thread.start()

# Close the CMD window if the script is run through CMD (checking for the terminal name)
if "cmd" in sys.argv[0].lower():  # Check if it's being run from a CMD window
    os.system("exit")

# Start the Tkinter event loop
root.mainloop()

# count time from last disconnect
# show how long a disconnect lasts for
# #of disconnects & total time disconnected in last 5 min, 1h, 6h, 24h
# tabs for 5min, 1h, 6h, 24h. each tab contains a list of disconnects
# show time-ordered list of individual disconnects and how long they lasted for each tab
#   if the disconnect are longer than .2 seconds, show them in different color
