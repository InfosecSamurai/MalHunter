import unittest
import os
from pathlib import Path
from analysis.static import StaticAnalyzer
from analysis.static import StringExtractor

class TestStaticAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = Path("tests/samples/test.exe")
        if not cls.test_file.exists():
            raise FileNotFoundError("Test sample not found")
    
    def test_pe_analysis(self):
        analyzer = StaticAnalyzer(self.test_file)
        results = analyzer.analyze()
        
        self.assertIn('pe_info', results)
        self.assertIn('imports', results)
        self.assertIsInstance(results['imports'], list)
        
    def test_string_extraction(self):
        extractor = StringExtractor(self.test_file)
        strings = extractor.extract_all_strings()
        
        self.assertIn('ascii', strings)
        self.assertIn('unicode', strings)
        self.assertGreater(len(strings['ascii']), 0)

if __name__ == '__main__':
    unittest.main()
