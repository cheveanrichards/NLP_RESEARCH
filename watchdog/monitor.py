import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import sys
import os

class WatchDogHandler(FileSystemEventHandler):
    def __init__(self, script_to_run, python_interpreter):
        self.script_to_run = script_to_run
        self.python_interpreter = python_interpreter

    def on_created(self, event):
        if not event.is_directory:
            print(f'File created: {event.src_path}')
            self.run_script("created")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f'File deleted: {event.src_path}')
            self.run_script("deleted")

    def run_script(self, action):
        subprocess.run([self.python_interpreter, self.script_to_run, action], check=True)

class WatchDogMonitor:
    def __init__(self, path, script_to_run, python_interpreter):
        self.path = path
        self.script_to_run = script_to_run
        self.python_interpreter = python_interpreter
        self.event_handler = WatchDogHandler(script_to_run, python_interpreter)
        self.observer = Observer()

    def start(self):
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()
        print(f'Started monitoring {self.path}')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()


