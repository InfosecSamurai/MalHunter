import os
import time
from analysis.static import StaticAnalyzer
from analysis.dynamic import DynamicAnalyzer
from core.reporter import ReportGenerator

class Sandbox:
    def __init__(self, sample_path, timeout=60, report_path=None):
        self.sample_path = sample_path
        self.timeout = timeout
        self.report_path = report_path or f"report_{os.path.basename(sample_path)}.html"
        self.results = {}
        
    def run(self):
        """Execute full analysis pipeline"""
        try:
            # Static Analysis Phase
            static = StaticAnalyzer(self.sample_path)
            self.results['static'] = static.analyze()
            
            # Dynamic Analysis Phase
            dynamic = DynamicAnalyzer(self.sample_path, self.timeout)
            self.results['dynamic'] = dynamic.analyze()
            
            # Generate Report
            reporter = ReportGenerator(self.results)
            reporter.generate(self.report_path)
            
        except Exception as e:
            raise SandboxError(f"Analysis failed: {str(e)}")

class SandboxError(Exception):
    pass
