import psutil
import time
import logging
from threading import Thread, Event

class ProcessMonitor:
    def __init__(self, pid):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stop_event = Event()
        self.results = {
            'process_tree': [],
            'files_accessed': set(),
            'registry_changes': set(),
            'network_connections': set(),
            'suspicious_behavior': []
        }
        
    def monitor(self, timeout):
        """Monitor process activity"""
        monitor_thread = Thread(target=self._monitor_loop, args=(timeout,))
        monitor_thread.start()
        monitor_thread.join(timeout + 5)  # Add buffer time
        
        # Convert sets to lists for JSON serialization
        self.results['files_accessed'] = list(self.results['files_accessed'])
        self.results['registry_changes'] = list(self.results['registry_changes'])
        self.results['network_connections'] = [
            self._parse_connection(conn) 
            for conn in self.results['network_connections']
        ]
        
        return self.results
    
    def _monitor_loop(self, timeout):
        start_time = time.time()
        
        try:
            while not self.stop_event.is_set() and time.time() - start_time < timeout:
                self._check_process_tree()
                self._check_file_access()
                self._check_network_activity()
                time.sleep(1)
        except psutil.NoSuchProcess:
            self.logger.info(f"Process {self.pid} terminated")
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
        finally:
            self.stop_event.set()
    
    def _check_process_tree(self):
        """Track spawned child processes"""
        for child in self.process.children(recursive=True):
            if not any(p['pid'] == child.pid for p in self.results['process_tree']):
                self.results['process_tree'].append({
                    'pid': child.pid,
                    'name': child.name(),
                    'cmdline': child.cmdline(),
                    'create_time': child.create_time(),
                    'parent_pid': child.ppid()
                })
    
    def _check_file_access(self):
        """Track file system activity"""
        for file in self.process.open_files():
            self.results['files_accessed'].add(file.path)
    
    def _check_network_activity(self):
        """Track network connections"""
        for conn in self.process.connections(kind='inet'):
            if conn.status == psutil.CONN_ESTABLISHED:
                self.results['network_connections'].add(conn)
    
    def _parse_connection(self, conn):
        return {
            'local_ip': conn.laddr.ip,
            'local_port': conn.laddr.port,
            'remote_ip': conn.raddr.ip if conn.raddr else None,
            'remote_port': conn.raddr.port if conn.raddr else None,
            'status': conn.status,
            'family': 'IPv4' if conn.family == 2 else 'IPv6'
        }
