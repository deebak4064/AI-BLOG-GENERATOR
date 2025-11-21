"""
Attribution Enforcement Module
Tracks usage and detects unauthorized derivative works
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

class AttributionTracker:
    """
    Monitors for proper attribution and logs usage instances
    """
    
    def __init__(self, app=None):
        self.app = app
        self.log_file = Path('attribution_logs.json')
        self.original_signature = self._get_original_signature()
        
    def _get_original_signature(self):
        """Generate signature of original codebase"""
        signature_items = [
            "AI Blog Generator",
            "deebak4064",
            "github.com/deebak4064/AI-BLOG-GENERATOR",
            "Deebak Kumar"
        ]
        return hashlib.md5("".join(signature_items).encode()).hexdigest()
    
    def check_attribution(self):
        """
        Check if proper attribution exists in the codebase
        Returns: (is_attributed, missing_items)
        """
        required_items = {
            'license': self._check_file_exists('LICENSE'),
            'citation': self._check_file_exists('CITATION.cff'),
            'readme_attribution': self._check_readme_attribution(),
            'code_header': self._check_code_headers(),
        }
        
        is_attributed = all(required_items.values())
        missing = [k for k, v in required_items.items() if not v]
        
        return is_attributed, missing
    
    def _check_file_exists(self, filename):
        """Check if required file exists"""
        return Path(filename).exists()
    
    def _check_readme_attribution(self):
        """Check if README mentions original author"""
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read().lower()
                attribution_keywords = [
                    'deebak kumar',
                    'deebak4064',
                    'github.com/deebak4064',
                    'original author'
                ]
                return any(keyword in content for keyword in attribution_keywords)
        except FileNotFoundError:
            return False
    
    def _check_code_headers(self):
        """Check if Python files have attribution headers"""
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                content = f.read(500)  # Check first 500 chars
                return 'deepak' in content.lower() or 'deebak4064' in content.lower()
        except FileNotFoundError:
            return False
    
    def log_deployment(self, deployment_info):
        """
        Log deployment instance
        deployment_info should contain: host, timestamp, attributed (bool)
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'host': deployment_info.get('host', 'unknown'),
            'attributed': deployment_info.get('attributed', False),
            'missing_attribution': deployment_info.get('missing', [])
        }
        
        logs = self._read_logs()
        logs.append(log_entry)
        self._write_logs(logs)
        
        # Return warning if not attributed
        if not log_entry['attributed']:
            return self._generate_warning(log_entry)
        return None
    
    def _read_logs(self):
        """Read existing logs"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _write_logs(self, logs):
        """Write logs to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except IOError:
            pass  # Silently fail - don't break the app
    
    def _generate_warning(self, log_entry):
        """Generate warning message for missing attribution"""
        warning = f"""
╔════════════════════════════════════════════════════════════════╗
║                   ⚠️  ATTRIBUTION WARNING  ⚠️                   ║
╠════════════════════════════════════════════════════════════════╣
║ This application is based on AI Blog Generator                 ║
║ Original Author: Deebak Kumar (deebak4064)                     ║
║ Repository: https://github.com/deebak4064/AI-BLOG-GENERATOR    ║
║                                                                ║
║ MISSING ATTRIBUTION for:                                       ║
║ {missing_items}                                 ║
║                                                                ║
║ Please ensure proper attribution is included:                  ║
║  ✓ Include LICENSE file                                        ║
║  ✓ Add credit in README.md                                     ║
║  ✓ Include CITATION.cff                                        ║
║  ✓ Add header comments in code files                           ║
║                                                                ║
║ Learn more: https://github.com/deebak4064/AI-BLOG-GENERATOR    ║
╚════════════════════════════════════════════════════════════════╝
"""
        missing_items = ", ".join(log_entry['missing_attribution'])
        return warning.format(missing_items=missing_items)
    
    def generate_report(self):
        """Generate compliance report"""
        is_attributed, missing = self.check_attribution()
        logs = self._read_logs()
        
        report = {
            'status': 'COMPLIANT' if is_attributed else 'NON-COMPLIANT',
            'attribution_check': {
                'licensed': missing == [],
                'missing_items': missing
            },
            'deployment_history': logs[-10:] if logs else [],  # Last 10 deployments
            'total_instances': len(logs)
        }
        
        return report
