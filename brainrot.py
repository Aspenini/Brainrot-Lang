#!/usr/bin/env python3
"""
🧠💀 Brainrot Lang Interpreter 💀🧠
Command-line interface for running Brainrot programs
"""

import sys
import os
from interpreter import run_brainrot

def main():
    if len(sys.argv) != 2:
        print("Usage: python brainrot.py <file.brainrot>")
        print("Example: python brainrot.py examples/hello.brainrot")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        sys.exit(1)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        print(f"Running {filename}...")
        print("=" * 50)
        run_brainrot(source)
        
    except UnicodeDecodeError as e:
        print(f"Unicode error: {e}")
        print("Make sure your file is saved with UTF-8 encoding")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
