import sys
import os


# Step 1: Construct the relative paths to the directories containing myclass1.py and myclass2.py
current_directory = os.path.dirname(__file__)
WatchDog_path= os.path.join(current_directory, '..')

# Step 2: Add the directories to the Python path
sys.path.append(WatchDog_path)

from monitor import WatchDogMonitor

path_to_watch =  os.path.abspath(os.path.join(current_directory, '..','..', 'samplepdf'))
script_to_run = os.path.abspath(os.path.join(current_directory, '..','..', 'data_clean_mod', 'test_clean_QA', 'test_clean.py'))

python_interpreter = os.path.abspath(os.path.join(current_directory, '..','..', '..', '.venv', 'Scripts', 'python.exe'))
monitor = WatchDogMonitor(path_to_watch, script_to_run, python_interpreter)
monitor.start()