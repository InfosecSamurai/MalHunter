import pefile
import peutils

class PEAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.signatures = peutils.SignatureDatabase('config/yara_rules/packed.yar')
        
    def analyze(self):
        results = {}
        try:
            pe = pefile.PE(self.file_path)
            
            # Basic PE Info
            results['pe_info'] = {
                'machine_type': pe.FILE_HEADER.Machine,
                'compile_time': pe.FILE_HEADER.TimeDateStamp,
                'entry_point': pe.OPTIONAL_HEADER.AddressOfEntryPoint,
                'sections': [{
                    'name': section.Name.decode().rstrip('\x00'),
                    'virtual_address': section.VirtualAddress,
                    'size': section.Misc_VirtualSize,
                    'characteristics': section.Characteristics
                } for section in pe.sections]
            }
            
            # Imports Analysis
            results['imports'] = []
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    imports = {
                        'dll': entry.dll.decode(),
                        'functions': []
                    }
                    for imp in entry.imports:
                        imports['functions'].append(
                            imp.name.decode() if imp.name else f"ordinal_{imp.ordinal}"
                        )
                    results['imports'].append(imports)
            
            # Packer Detection
            matches = self.signatures.match(pe, ep_only=True)
            if matches:
                results['packers'] = [match for match in matches]
            
            return results
            
        finally:
            if 'pe' in locals():
                pe.close()
