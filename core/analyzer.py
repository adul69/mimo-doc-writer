import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any


class CodeAnalyzer:
    """
    Multi-step code analyzer:
    1. SCAN - Find all files and structure
    2. UNDERSTAND - Parse code meaning and relationships
    3. GENERATE - Create documentation with reasoning
    """
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
    }
    
    def __init__(self):
        self.files = []
        self.code_snippets = {}
        self.dependencies = set()
        self.classes = []
        self.functions = []
        self.imports = []
    
    def scan_directory(self, path):
        self.files = []
        skip_dirs = ['node_modules', '__pycache__', 'venv', '.git', 'dist', 'build']
        
        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in skip_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                if ext in self.SUPPORTED_EXTENSIONS:
                    rel_path = os.path.relpath(filepath, path)
                    self.files.append({
                        "path": rel_path,
                        "extension": ext,
                        "language": self.SUPPORTED_EXTENSIONS.get(ext, "Other"),
                        "size": os.path.getsize(filepath)
                    })
        
        return {
            "total_files": len(self.files),
            "languages": self._get_language_stats(),
            "files": self.files
        }
    
    def _get_language_stats(self):
        stats = {}
        for f in self.files:
            lang = f["language"]
            stats[lang] = stats.get(lang, 0) + 1
        return stats
    
    def understand_code(self, path, max_files=20):
        self.classes = []
        self.functions = []
        self.imports = []
        self.dependencies = set()
        
        for f in self.files[:max_files]:
            filepath = os.path.join(path, f["path"])
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    self.code_snippets[f["path"]] = content[:5000]
                    
                    if f["extension"] == '.py':
                        self._parse_python(content, f["path"])
                    elif f["extension"] in ['.js', '.ts', '.jsx', '.tsx']:
                        self._parse_javascript(content, f["path"])
            except Exception:
                continue
        
        return {
            "classes": self.classes,
            "functions": self.functions[:50],
            "imports": self.imports[:50],
            "dependencies": list(self.dependencies)
        }
    
    def _parse_python(self, content, filepath):
        for match in re.finditer(r'^(?:from|import)\s+([\w.]+)', content, re.MULTILINE):
            self.imports.append({"file": filepath, "module": match.group(1)})
            self.dependencies.add(match.group(1).split('.')[0])
        
        for match in re.finditer(r'^class\s+(\w+)', content, re.MULTILINE):
            self.classes.append({"name": match.group(1), "file": filepath})
        
        for match in re.finditer(r'^(?:def|async def)\s+(\w+)', content, re.MULTILINE):
            self.functions.append({"name": match.group(1), "file": filepath})
    
    def _parse_javascript(self, content, filepath):
        import_pattern = r'(?:import|require).*?["\'](.*?)["\']'
        for match in re.finditer(import_pattern, content):
            self.imports.append({"file": filepath, "module": match.group(1)})
            if not match.group(1).startswith('.'):
                self.dependencies.add(match.group(1).split('/')[0])
        
        for match in re.finditer(r'class\s+(\w+)', content):
            self.classes.append({"name": match.group(1), "file": filepath})
        
        for match in re.finditer(r'(?:function|const|let|var)\s+(\w+)', content):
            self.functions.append({"name": match.group(1), "file": filepath})
    
    def prepare_for_ai(self, path):
        scan_result = self.scan_directory(path)
        understand_result = self.understand_code(path)
        main_file = self._find_main_file(path)
        
        return {
            "project_name": os.path.basename(path),
            "scan": scan_result,
            "understand": understand_result,
            "main_file": main_file,
            "code_snippets": dict(list(self.code_snippets.items())[:10])
        }
    
    def _find_main_file(self, path):
        candidates = ['main.py', 'app.py', 'index.py', 'server.py', 'main.js', 'index.js']
        for candidate in candidates:
            if os.path.exists(os.path.join(path, candidate)):
                return candidate
        return self.files[0]["path"] if self.files else "unknown"
