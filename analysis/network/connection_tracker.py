import socket
import psutil
import logging
from threading import Thread, Event

class ConnectionTracker:
    def __init__(self, pid):
        self.pid = pid
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stop_event = Event()
        self.connections = []
        
    def start_tracking(self):
        """Start connection tracking"""
        self.thread = Thread(target=self._track_loop)
        self.thread.start()
        
    def stop_tracking(self):
        """Stop tracking and return results"""
        self.stop_event.set()
        self.thread.join()
        return self.connections
        
    def _track_loop(self):
        """Track network connections"""
        try:
            process = psutil.Process(self.pid)
            
            while not self.stop_event.is_set():
                for conn in process.connections(kind='inet'):
                    conn_info = {
                        'family': 'IPv4' if conn.family == socket.AF_INET else 'IPv6',
                        'type': 'TCP' if conn.type == socket.SOCK_STREAM else 'UDP',
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                        'status': conn.status,
                        'timestamp': time.time()
                    }
                    
                    if conn_info not in self.connections:
                        self.connections.append(conn_info)
                
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Connection tracking failed: {e}")
