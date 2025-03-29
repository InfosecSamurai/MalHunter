# MalHunter - Advanced Malware Analysis Sandbox 🔍🛡️

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/InfosecSamurai/malhunter/tests.yml)](https://github.com/InfosecSamurai/malhunter/actions)
[![Code Coverage](https://img.shields.io/codecov/c/github/InfosecSamurai/malhunter)](https://codecov.io/gh/InfosecSamurai/malhunter)
[![Open Issues](https://img.shields.io/github/issues/InfosecSamurai/malhunter)](https://github.com/InfosecSamurai/malhunter/issues)
[![Last Commit](https://img.shields.io/github/last-commit/InfosecSamurai/malhunter)](https://github.com/InfosecSamurai/malhunter/commits/main)

**A fully-featured malware analysis sandbox for automated static and dynamic analysis of suspicious files**

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/InfosecSamurai)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://github.com/sponsors/InfosecSamurai)

## Features ✨

- **Hybrid Analysis**: Static + Dynamic analysis pipeline
- **Comprehensive Monitoring**:
  - Process tree analysis
  - API call tracing
  - File system/registry changes
  - Network traffic inspection
- **Multi-layered Detection**:
  - YARA rule scanning
  - Behavioral heuristics
  - Memory pattern analysis
- **Flexible Deployment**:
  - Standalone Python application
  - Docker container support
  - REST API (coming soon)

## Quick Start 🚀

### Prerequisites
- Python 3.9+
- Docker (optional)
- Windows/Linux (Windows recommended for full API monitoring)

### Installation
```bash
# Clone repository
git clone https://github.com/InfosecSamurai/malhunter.git
cd malhunter

# Install dependencies
pip install -r requirements.txt

# Set up directories
mkdir -p samples reports logs
```

### Basic Usage
```bash
# Analyze a sample
python main.py samples/suspicious.exe

# With custom timeout (seconds)
python main.py samples/malware.dll -t 120

# Generate HTML report
python main.py samples/trojan.exe -o reports/trojan_analysis.html
```

### Docker Usage
```bash
# Build the image
docker build -t malhunter .

# Run analysis (mount sample directory)
docker run -v $(pwd)/samples:/app/samples -v $(pwd)/reports:/app/reports malhunter samples/ransomware.exe
```

## Documentation 📚

### Analysis Modules

| Module | Description | Key Features |
|--------|-------------|--------------|
| **Static Analysis** | Pre-execution examination | PE parsing, YARA scanning, String extraction |
| **Dynamic Analysis** | Runtime behavior monitoring | API calls, Process injection, Registry modifications |
| **Network Analysis** | Traffic inspection | DNS queries, HTTP traffic, Connection tracking |

### Sample Report Preview
![Report Screenshot](docs/report_preview.png)

### Configuration
Edit `config/settings.py` to customize:
```python
# Analysis parameters
ANALYSIS_TIMEOUT = 60  # Seconds
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# VirusTotal integration
VT_API_KEY = os.getenv('VT_API_KEY')  # Set your API key
VT_ENABLED = True
```

## Advanced Usage 🔧

### Custom YARA Rules
Add your rules to:
```
config/yara_rules/
├── custom_rules.yar
├── packed.yar
└── malware.yar
```

### API Documentation
```python
from malhunter import Sandbox

# Create custom analysis
sandbox = Sandbox(
    sample_path="malware.exe",
    timeout=90,
    static_only=False
)
results = sandbox.run()
```

## Support the Project ❤️

If you find MalHunter useful, consider supporting its development:

[![Buy Me A Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/InfosecSamurai)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red)](https://github.com/sponsors/InfosecSamurai)
[![PayPal](https://img.shields.io/badge/PayPal-Support-blue)](https://paypal.me/InfosecSamurai)

## Roadmap 🗺️

- [x] Core analysis engine
- [x] Docker support
- [ ] Cuckoo Sandbox integration
- [ ] REST API interface
- [ ] Distributed analysis cluster
- [ ] Threat intelligence feeds

## Contributing 🤝

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: Use this tool only on systems you own or have permission to analyze. The developers are not responsible for any misuse or damage caused by this software.
