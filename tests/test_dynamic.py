import unittest
import subprocess
import time
import os
from analysis.dynamic import ProcessMonitor

class TestDynamicAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_process = subprocess.Popen(["notepad.exe"])
        time.sleep(1)  # Allow process to start
        cls.pid = cls.test_process.pid
    
    def test_process_monitoring(self):
        monitor = ProcessMonitor(self.pid)
        results = monitor.monitor(timeout=5)
        
        self.assertIn('process_tree', results)
        self.assertIn('files_accessed', results)
        
    @classmethod
    def tearDownClass(cls):
        cls.test_process.terminate()

if __name__ == '__main__':
    unittest.main()
