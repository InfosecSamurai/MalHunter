import psutil
import time

class ProcessMonitor:
    def __init__(self, pid):
        self.pid = pid
        self.process = psutil.Process(pid)
        self.children = set()
        
    def monitor(self, timeout=60):
        results = {
            'process_created': [],
            'files_accessed': set(),
            'connections': set()
        }
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Track child processes
                current_children = set(p.pid for p in self.process.children(recursive=True))
                new_children = current_children - self.children
                
                for child_pid in new_children:
                    child = psutil.Process(child_pid)
                    results['process_created'].append({
                        'pid': child_pid,
                        'name': child.name(),
                        'cmdline': child.cmdline(),
                        'create_time': child.create_time()
                    })
                    self.children.add(child_pid)
                
                # Track file access
                for file in self.process.open_files():
                    results['files_accessed'].add(file.path)
                
                # Track network connections
                for conn in self.process.connections():
                    if conn.status == 'ESTABLISHED':
                        results['connections'].add(
                            (conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port)
                        )
                
                time.sleep(1)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                break
        
        # Convert sets to lists for JSON serialization
        results['files_accessed'] = list(results['files_accessed'])
        results['connections'] = [{
            'local_ip': conn[0],
            'local_port': conn[1],
            'remote_ip': conn[2],
            'remote_port': conn[3]
        } for conn in results['connections']]
        
        return results
