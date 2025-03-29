import pyshark
import logging
from threading import Thread, Event
from queue import Queue

class NetworkAnalyzer:
    def __init__(self, timeout):
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        self.packet_queue = Queue()
        self.stop_event = Event()
        
    def capture(self):
        """Capture network traffic during analysis"""
        results = {
            'dns_queries': set(),
            'http_requests': set(),
            'tcp_connections': set(),
            'udp_flows': set()
        }
        
        # Start capture thread
        capture_thread = Thread(target=self._capture_thread)
        capture_thread.start()
        
        # Process packets while monitoring
        start_time = time.time()
        while time.time() - start_time < self.timeout and not self.stop_event.is_set():
            try:
                packet = self.packet_queue.get(timeout=1)
                self._process_packet(packet, results)
            except Empty:
                continue
        
        # Clean up
        self.stop_event.set()
        capture_thread.join()
        
        # Convert sets to lists
        for key in results:
            results[key] = list(results[key])
            
        return results
    
    def _capture_thread(self):
        """Thread that performs actual packet capture"""
        try:
            capture = pyshark.LiveCapture(
                interface=Settings.NETWORK_INTERFACE,
                display_filter=Settings.CAPTURE_FILTER
            )
            
            for packet in capture.sniff_continuously():
                if self.stop_event.is_set():
                    break
                self.packet_queue.put(packet)
                
        except Exception as e:
            self.logger.error(f"Packet capture failed: {e}")
    
    def _process_packet(self, packet, results):
        """Analyze individual packets"""
        try:
            # DNS Queries
            if hasattr(packet, 'dns') and hasattr(packet.dns, 'qry_name'):
                results['dns_queries'].add(packet.dns.qry_name)
            
            # HTTP Requests
            elif hasattr(packet, 'http') and hasattr(packet.http, 'request_uri'):
                results['http_requests'].add(
                    f"{packet.http.host}:{packet.http.request_uri}"
                )
            
            # TCP Connections
            elif hasattr(packet, 'tcp'):
                src = f"{packet.ip.src}:{packet.tcp.srcport}"
                dst = f"{packet.ip.dst}:{packet.tcp.dstport}"
                results['tcp_connections'].add(f"{src} -> {dst}")
            
            # UDP Flows
            elif hasattr(packet, 'udp'):
                src = f"{packet.ip.src}:{packet.udp.srcport}"
                dst = f"{packet.ip.dst}:{packet.udp.dstport}"
                results['udp_flows'].add(f"{src} -> {dst}")
                
        except AttributeError:
            pass  # Skip packets missing expected layers
