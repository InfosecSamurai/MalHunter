import yara
import logging
from pathlib import Path

class YARAScanner:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rules = self._compile_rules()
        
    def _compile_rules(self):
        """Compile all YARA rules from config directory"""
        try:
            return yara.compile(filepaths={
                'packed': str(Settings.YARA_RULES['packed']),
                'malware': str(Settings.YARA_RULES['malware']),
                'suspicious': str(Settings.YARA_RULES['suspicious'])
            })
        except yara.Error as e:
            self.logger.error(f"YARA rule compilation failed: {e}")
            return None
    
    def scan_file(self, file_path):
        """Scan a file with YARA rules"""
        if not self.rules:
            return None
            
        try:
            matches = self.rules.match(str(file_path))
            return [{
                'rule': match.rule,
                'tags': match.tags,
                'meta': match.meta
            } for match in matches]
        except yara.Error as e:
            self.logger.error(f"YARA scan failed: {e}")
            return None
