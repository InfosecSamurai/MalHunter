import logging
import time
from multiprocessing import Process, Queue
from analysis.static import StaticAnalyzer
from analysis.dynamic import DynamicAnalyzer
from analysis.network import NetworkAnalyzer

class AnalysisSupervisor:
    def __init__(self, sample_path, timeout=60):
        self.sample_path = sample_path
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        self.result_queue = Queue()
        
    def run_analysis(self):
        """Run complete analysis pipeline"""
        start_time = time.time()
        results = {}
        
        # Static Analysis
        static = StaticAnalyzer(self.sample_path)
        results['static'] = static.analyze()
        
        if not Settings.STATIC_ONLY:
            # Dynamic Analysis
            dynamic_proc = Process(
                target=self._run_dynamic_analysis,
                args=(self.sample_path, self.timeout, self.result_queue)
            )
            dynamic_proc.start()
            
            # Network Analysis
            network_proc = Process(
                target=self._run_network_analysis,
                args=(self.timeout, self.result_queue)
            )
            network_proc.start()
            
            # Wait for completion
            dynamic_proc.join()
            network_proc.join()
            
            # Collect results
            while not self.result_queue.empty():
                name, data = self.result_queue.get()
                results[name] = data
        
        results['metadata'] = {
            'analysis_time': time.time() - start_time,
            'sample': str(self.sample_path),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return results
        
    def _run_dynamic_analysis(self, sample_path, timeout, queue):
        """Run dynamic analysis in separate process"""
        try:
            dynamic = DynamicAnalyzer(sample_path, timeout)
            queue.put(('dynamic', dynamic.analyze()))
        except Exception as e:
            self.logger.error(f"Dynamic analysis failed: {e}")
            queue.put(('dynamic', {'error': str(e)}))
            
    def _run_network_analysis(self, timeout, queue):
        """Run network analysis in separate process"""
        try:
            network = NetworkAnalyzer(timeout)
            queue.put(('network', network.capture()))
        except Exception as e:
            self.logger.error(f"Network analysis failed: {e}")
            queue.put(('network', {'error': str(e)}))
