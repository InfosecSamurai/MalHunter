import logging
import psutil
import re
from pathlib import Path

class MemoryUtils:
    @staticmethod
    def dump_process_memory(pid, output_dir):
        """Dump process memory to files"""
        try:
            output_dir = Path(output_dir)
            output_dir.mkdir(exist_ok=True)
            
            process = psutil.Process(pid)
            memory_maps = process.memory_maps()
            
            dumps = []
            for i, region in enumerate(memory_maps):
                try:
                    with open(region.path, 'rb') as f:
                        f.seek(region.rss)
                        data = f.read(region.rss)
                        
                        dump_file = output_dir / f"region_{i}_{region.addr}.dmp"
                        with open(dump_file, 'wb') as out:
                            out.write(data)
                        dumps.append(str(dump_file))
                except Exception as e:
                    logging.warning(f"Failed to dump memory region {i}: {e}")
            
            return dumps
        except Exception as e:
            logging.error(f"Memory dump failed: {e}")
            return None

    @staticmethod
    def scan_memory_for_patterns(pid, patterns):
        """Scan process memory for specific patterns"""
        results = {}
        try:
            process = psutil.Process(pid)
            memory_maps = process.memory_maps()
            
            for pattern_name, pattern in patterns.items():
                compiled = re.compile(pattern)
                matches = []
                
                for region in memory_maps:
                    try:
                        with open(region.path, 'rb') as f:
                            f.seek(region.rss)
                            data = f.read(region.rss)
                            
                            for match in compiled.finditer(data):
                                matches.append({
                                    'address': region.addr,
                                    'offset': match.start(),
                                    'match': match.group().decode('utf-8', errors='ignore')
                                })
                    except Exception:
                        continue
                
                results[pattern_name] = matches
            
            return results
        except Exception as e:
            logging.error(f"Memory scan failed: {e}")
            return None
