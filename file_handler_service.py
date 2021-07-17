from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import shutil
import time

import win32.lib.win32serviceutil
import win32.win32service
import win32.servicemanager as sm
import socket

class Service(win32.lib.win32serviceutil.ServiceFramework):
    name = 'PythonTestService'
    disp_name = 'Python Test Service'

    def __init__(self, args):
        win32.lib.win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32.win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def Service_Stop(self):
        self.ReportServiceStatus(win32.win32service.SERVICE_STOP_PENDING)
        win32.win32event.SetEvent(self.hWaitStop)

    def Service_Do_Run(self):
        sm.LogMsg(sm.EVENTLOG_INFORMATION_TYPE,
                sm.PYS_SERVICE_STARTED,
                (self.name,''))

        self.main()
    
    def main(self):
        
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

if __name__ == '__main__':
    win32.lib.win32serviceutil.HandleCommandLine(Service)