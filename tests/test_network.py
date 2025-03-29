import unittest
from analysis.network import DNSAnalyzer
from analysis.network import ConnectionTracker

class TestNetworkAnalysis(unittest.TestCase):
    def test_dns_analysis(self):
        analyzer = DNSAnalyzer()
        analyzer.start_analysis(pcap_file="tests/samples/dns_traffic.pcap")
        results = analyzer.stop_analysis()
        
        self.assertIn('queries', results)
        self.assertIn('responses', results)
        
    def test_connection_tracking(self):
        tracker = ConnectionTracker(pid=1)  # System process for test
        tracker.start_tracking()
        time.sleep(5)
        results = tracker.stop_tracking()
        
        self.assertIsInstance(results, list)

if __name__ == '__main__':
    unittest.main()
