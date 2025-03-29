import requests
import logging
from pathlib import Path
from urllib.parse import quote

class VirusTotalAPI:
    BASE_URL = "https://www.virustotal.com/api/v3"
    
    def __init__(self):
        self.api_key = Settings.VT_API_KEY
        self.logger = logging.getLogger(self.__class__.__name__)
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
        
    def check_hash(self, file_hash):
        """Check file hash against VirusTotal"""
        if not Settings.VT_ENABLED:
            return None
            
        try:
            url = f"{self.BASE_URL}/files/{file_hash}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"VirusTotal check failed: {e}")
            return None
    
    def upload_file(self, file_path):
        """Upload file to VirusTotal for analysis"""
        if not Settings.VT_ENABLED or not Settings.VT_UPLOAD:
            return None
            
        try:
            # Get upload URL
            url = f"{self.BASE_URL}/files/upload_url"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            upload_url = response.json()['data']
            
            # Upload file
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f)}
                response = requests.post(upload_url, files=files, headers=self.headers)
                response.raise_for_status()
                
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.warning(f"VirusTotal upload failed: {e}")
            return None
