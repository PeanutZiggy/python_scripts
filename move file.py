from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import json
import time



folder_to_track = r"C:\Users\KitovYo\Desktop\one"
folder_destination = "C:/Users/KitovYo/Desktop/two"


test_files = os.listdir(folder_destination)

print(test_files)

if test_files == list():
    print('empty')
else:
    print('not empty')

for file in test_files:
    shutil.move(folder_destination + '/' + file, folder_to_track)

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()
#     observer.join()
