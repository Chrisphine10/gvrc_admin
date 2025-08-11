import subprocess
import json
import os
from django.conf import settings


def run_pytest_tests():
    """Run pytest tests and return results"""
    try:
        # Change to project directory
        os.chdir(settings.BASE_DIR)
        
        # Run pytest with JSON output
        result = subprocess.run([
            'python3', '-m', 'pytest', 
            'tests/', 
            '--tb=short', 
            '-v',
            '--json-report',
            '--json-report-file=/tmp/pytest_report.json'
        ], capture_output=True, text=True, timeout=60)
        
        # Try to read JSON report
        try:
            with open('/tmp/pytest_report.json', 'r') as f:
                json_data = json.load(f)
        except:
            json_data = None
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'json_report': json_data
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'stdout': '',
            'stderr': 'Test execution timed out after 60 seconds',
            'return_code': -1,
            'json_report': None
        }
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'return_code': -1,
            'json_report': None
        }