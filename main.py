#!/usr/bin/env python3
import argparse
from core.sandbox import Sandbox
from utils.logging_utils import setup_logging

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description='MalHunter Malware Analysis Sandbox')
    parser.add_argument('sample', help='Path to sample file')
    parser.add_argument('-t', '--timeout', type=int, default=60, help='Analysis timeout in seconds')
    parser.add_argument('-o', '--output', help='Output report path')
    
    args = parser.parse_args()
    
    sandbox = Sandbox(
        sample_path=args.sample,
        timeout=args.timeout,
        report_path=args.output
    )
    sandbox.run()

if __name__ == '__main__':
    main()
