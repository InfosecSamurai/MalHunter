import os
import magic
import hashlib
import logging
from pathlib import Path

class FileUtils:
    @staticmethod
    def safe_path(base_path, *paths):
        """Create safe joined path preventing directory traversal"""
        try:
            base = Path(base_path).resolve()
            full_path = base.joinpath(*paths).resolve()
            
            if base in full_path.parents or base == full_path:
                return full_path
            raise ValueError("Path traversal attempt detected")
        except Exception as e:
            logging.error(f"Path validation failed: {e}")
            raise

    @staticmethod
    def get_file_type(file_path):
        """Get file type using libmagic"""
        try:
            return magic.from_file(str(file_path))
        except Exception as e:
            logging.warning(f"File type detection failed: {e}")
            return "Unknown"

    @staticmethod
    def calculate_hashes(file_path, algorithms=['md5', 'sha1', 'sha256']):
        """Calculate multiple hash digests for a file"""
        hashes = {alg: getattr(hashlib, alg)() for alg in algorithms}
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    for h in hashes.values():
                        h.update(chunk)
            
            return {k: v.hexdigest() for k, v in hashes.items()}
        except Exception as e:
            logging.error(f"Hash calculation failed: {e}")
            return None
