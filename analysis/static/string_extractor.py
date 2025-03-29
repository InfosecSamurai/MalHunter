import re
import logging
from pathlib import Path

class StringExtractor:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def extract_ascii(self, min_length=4):
        """Extract ASCII strings from binary"""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            strings = []
            current = []
            
            for byte in data:
                if 32 <= byte <= 126:  # Printable ASCII
                    current.append(chr(byte))
                else:
                    if len(current) >= min_length:
                        strings.append(''.join(current))
                    current = []
            
            if len(current) >= min_length:
                strings.append(''.join(current))
                
            return strings
        except Exception as e:
            self.logger.error(f"ASCII extraction failed: {e}")
            return None
    
    def extract_unicode(self, min_length=4):
        """Extract Unicode strings from binary"""
        try:
            with open(self.file_path, 'rb') as f:
                data = f.read()
            
            # Look for UTF-16LE strings (common in Windows)
            pattern = b'(?:[^\x00][\x00]){%d,}' % min_length
            matches = re.finditer(pattern, data)
            
            strings = []
            for match in matches:
                try:
                    decoded = match.group().decode('utf-16le')
                    strings.append(decoded)
                except UnicodeDecodeError:
                    continue
            
            return strings
        except Exception as e:
            self.logger.error(f"Unicode extraction failed: {e}")
            return None
    
    def extract_all_strings(self, min_length=4):
        """Extract both ASCII and Unicode strings"""
        return {
            'ascii': self.extract_ascii(min_length),
            'unicode': self.extract_unicode(min_length)
        }
