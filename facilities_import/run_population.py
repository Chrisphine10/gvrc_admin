#!/usr/bin/env python3
"""
Run data population for GBV facilities
"""

import os
import sys
import subprocess
from pathlib import Path

def run_population():
    """Run the data population script"""
    script_dir = Path(__file__).parent
    populate_script = script_dir / 'populate_sample_data.py'
    
    print("Running GBV facilities data population...")
    print(f"Script location: {populate_script}")
    
    try:
        # Run the population script
        result = subprocess.run([
            sys.executable, str(populate_script)
        ], capture_output=True, text=True, cwd=script_dir.parent)
        
        if result.returncode == 0:
            print("SUCCESS: Data population completed!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("ERROR: Data population failed!")
            print("\nError output:")
            print(result.stderr)
            print("\nStandard output:")
            print(result.stdout)
            
    except Exception as e:
        print(f"ERROR: Failed to run population script: {e}")

if __name__ == '__main__':
    run_population()