import dpkt
import logging
from threading import Thread, Event

class DNSAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stop_event = Event()
        self.dns_queries = set()
        self.dns_responses = set()
        
    def start_analysis(self, pcap_file=None):
        """Start DNS analysis"""
        if pcap_file:
            self._analyze_pcap(pcap_file)
        else:
            self.thread = Thread(target=self._live_analysis)
            self.thread.start()
            
    def stop_analysis(self):
        """Stop analysis and return results"""
        self.stop_event.set()
        if hasattr(self, 'thread'):
            self.thread.join()
            
        return {
            'queries': list(self.dns_queries),
            'responses': list(self.dns_responses)
        }
        
    def _live_analysis(self):
        """Perform live DNS analysis"""
        try:
            import pyshark
            capture = pyshark.LiveCapture(
                interface=Settings.NETWORK_INTERFACE,
                display_filter='dns'
            )
            
            for packet in capture.sniff_continuously():
                if self.stop_event.is_set():
                    break
                    
                if hasattr(packet, 'dns'):
                    self._process_dns_packet(packet.dns)
                    
        except Exception as e:
            self.logger.error(f"Live DNS analysis failed: {e}")
            
    def _analyze_pcap(self, pcap_file):
        """Analyze DNS traffic from PCAP file"""
        try:
            with open(pcap_file, 'rb') as f:
                pcap = dpkt.pcap.Reader(f)
                
                for ts, buf in pcap:
                    try:
                        eth = dpkt.ethernet.Ethernet(buf)
                        ip = eth.data
                        udp = ip.data
                        
                        if isinstance(udp, dpkt.udp.UDP) and udp.dport == 53:
                            dns = dpkt.dns.DNS(udp.data)
                            self._process_dns_object(dns)
                            
                    except Exception:
                        continue
                        
        except Exception as e:
            self.logger.error(f"PCAP analysis failed: {e}")
            
    def _process_dns_packet(self, dns_layer):
        """Process DNS packet from live capture"""
        if hasattr(dns_layer, 'qry_name'):
            self.dns_queries.add(dns_layer.qry_name)
        if hasattr(dns_layer, 'resp_name'):
            self.dns_responses.add(dns_layer.resp_name)
            
    def _process_dns_object(self, dns):
        """Process DNS object from dpkt"""
        for q in dns.qd:
            if q.name:
                self.dns_queries.add(q.name)
        for rr in dns.an:
            if rr.name:
                self.dns_responses.add(rr.name)
