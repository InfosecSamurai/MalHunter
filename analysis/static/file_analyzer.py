import hashlib
import math
import logging
from pathlib import Path

class FileAnalyzer:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def calculate_hashes(self):
        """Calculate multiple hash digests"""
        hashes = {
            'md5': hashlib.md5(),
            'sha1': hashlib.sha1(),
            'sha256': hashlib.sha256()
        }
        
        try:
            with open(self.file_path, 'rb') as f:
                while chunk := f.read(8192):
                    for algo in hashes.values():
                        algo.update(chunk)
            
            return {k: v.hexdigest() for k, v in hashes.items()}
        except Exception as e:
            self.logger.error(f"Hash calculation failed: {e}")
            return None
    
    def calculate_entropy(self):
        """Calculate file entropy"""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            if not data:
                return 0.0
                
            entropy = 0.0
            for x in range(256):
                p_x = float(data.count(x))/len(data)
                if p_x > 0:
                    entropy += - p_x * math.log(p_x, 2)
            
            return round(entropy, 4)
        except Exception as e:
            self.logger.error(f"Entropy calculation failed: {e}")
            return None
    
    def extract_strings(self, min_length=4):
        """Extract ASCII strings from binary"""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            strings = []
            current_string = []
            
            for byte in data:
                if 32 <= byte <= 126:  # Printable ASCII
                    current_string.append(chr(byte))
                else:
                    if len(current_string) >= min_length:
                        strings.append(''.join(current_string))
                    current_string = []
            
            # Add any remaining string
            if len(current_string) >= min_length:
                strings.append(''.join(current_string))
                
            return strings
        except Exception as e:
            self.logger.error(f"String extraction failed: {e}")
            return None
