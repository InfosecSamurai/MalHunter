import os
import time
import logging
from pathlib import Path
from threading import Thread, Event

class FileMonitor:
    def __init__(self, pid):
        self.pid = pid
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stop_event = Event()
        self.files_accessed = set()
        self.files_created = set()
        self.files_deleted = set()
        
    def start_monitoring(self):
        """Start filesystem monitoring"""
        self.thread = Thread(target=self._monitor_loop)
        self.thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring and return results"""
        self.stop_event.set()
        self.thread.join()
        
        return {
            'accessed': list(self.files_accessed),
            'created': list(self.files_created),
            'deleted': list(self.files_deleted)
        }
        
    def _monitor_loop(self):
        """Monitor filesystem activity"""
        try:
            import psutil
            process = psutil.Process(self.pid)
            
            initial_files = set()
            for file in process.open_files():
                initial_files.add(file.path)
            
            while not self.stop_event.is_set():
                current_files = set()
                for file in process.open_files():
                    path = file.path
                    current_files.add(path)
                    
                    if path not in initial_files:
                        self.files_accessed.add(path)
                
                # Check for created/deleted files
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"File monitoring failed: {e}")
