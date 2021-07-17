from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import time

        
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        files = os.listdir(folder_to_track)
            
        for file in files:
            if ".tmp" in file:
                pass
            else:
                try:
                    shutil.move(folder_to_track + '/' + file, folder_destination)
                except:
                    shutil.move(os.path.join(folder_to_track, file), os.path.join(folder_destination, file))
                
folder_to_track = r"C:\Users\KitovYo\Desktop\one"
folder_destination = r"C:\Users\KitovYo\Desktop\two"
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()
