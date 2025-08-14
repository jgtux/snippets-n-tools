import os
import time
import threading

# File monitoring snippets 

"""
Monitor a file for modifications and call a callback function when it changes.

Args:
      path (str): Path to the file to monitor.
      callback (callable): Function to call when the file is modified.
      interval (int, optional): Time in seconds between checks. Defaults to 5.
"""
def monitor_file_changes(path: str, callback, interval: int = 5):
    last_mtime = os.path.getmtime(path)
    while True:
        current_mtime = os.path.getmtime(path)
        if current_mtime != last_mtime:
            callback()
            last_mtime = current_mtime
        time.sleep(interval)

# Example usage:
# def on_file_change():
#     print("File modified, reloading...")
#
# thread = threading.Thread(
#     target=monitor_file_changes, 
#     args=("example.csv", on_file_change), 
#     daemon=True
# )
# thread.start()
