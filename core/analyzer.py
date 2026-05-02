import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

class CodeAnalyzer:
    """
    Multi-step code analyzer:
    1. SCAN - Find all files & structure
    2. UNDERSTAND - Parse code meaning & relationships
    3. GENERATE - Create documentation with reasoning
    """
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.java': 'Java',
        '.cpp': 'C++',
        '.c': 'C',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
    }
    
    def __init__(self):
        self.files = []
        self.structure = {}
        self.code_snippets = {}
        self.dependencies = set()
        self.classes = []
        self.functions = []
        self.imports = []
    
    # ═══════════════════════════════════════════
    # STEP 1: SCAN - Find all files & structure
    # ═══════════════════════════════════════════
    def scan_directory(self, path: str) -> Dict[str, Any]:
        """Scan directory and build file tree"""
        self.files = []
        self.structure = {"name": os.path.basename(path), "type": "directory", "children": []}
        
        for root, dirs, files in os.walk(path):
            # Skip hidden & common non-essential dirs
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.git', 'dist', 'build']]
            
            for file in files:
                filepath = os.path.join(root, file)
                ext = os.path.splitext(file)[1].lower()
                
                if ext in self.SUPPORTED_EXTENSIONS or file in ['README.md', 'package.json', 'requirements.txt', 'Cargo.toml']:
                    rel_path = os.path.relpath(filepath, path)
                    self.files.append({
                        "path": rel_path,
                        "extension": ext,
                        "language": self.SUPPORTED_EXTENSIONS.get(ext, "Config"),
                        "size": os.path.getsize(filepath)
                    })
        
        return {
            "total_files": len(self.files),
            "languages": self._get_language_stats(),
            "files": self.files
        }
    
    def _get_language_stats(self) -> Dict[str, int]:
        """Get language distribution"""
        stats = {}
        for f in self.files:
            lang = f["language"]
            stats[lang] = stats.get(lang, 0) + 1
        return stats
    
    # ═══════════════════════════════════════════
    # STEP 2: UNDERSTAND - Parse code meaning
    # ═══════════════════════════════════════════
    def understand_code(self, path: str, max_files: int = 20) -> Dict[str, Any]:
        """Parse code to understand structure & relationships"""
        self.classes = []
        self.functions = []
        self.imports = []
        self.dependencies = set()
        
        files_to_analyze = self.files[:max_files]
        
        for f in files_to_analyze:
            filepath = os.path.join(path, f["path"])
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    self.code_snippets[f["path"]] = content[:5000]  # First 5k chars
                    
                    if f["extension"] == '.py':
                        self._parse_python(content, f["path"])
                    elif f["extension"] in ['.js', '.ts', '.jsx', '.tsx']:
                        self._parse_javascript(content, f["path"])
            except Exception as e:
                continue
        
        return {
            "classes": self.classes,
            "functions": self.functions[:50],
            "imports": self.imports[:50],
            "dependencies": list(self.dependencies)
        }
    
    def _parse_python(self, content: str, filepath: str):
        """Parse Python code for classes, functions, imports"""
        # Find imports
        for match in re.finditer(r'^(?:from|import)\s+([\w.]+)', content, re.MULTILINE):
            self.imports.append({"file": filepath, "module": match.group(1)})
            self.dependencies.add(match.group(1).split('.')[0])
        
        # Find classes
        for match in re.finditer(r'^class\s+(\w+)(?:\(([^)]+)\))?', content, re.MULTILINE):
            self.classes.append({
                "name": match.group(1),
                "parent": match.group(2),
                "file": filepath
            })
        
        # Find functions
        for match in re.finditer(r'^(?:def|async def)\s+(\w+)\s*\(([^)]*)\)', content, re.MULTILINE):
            self.functions.append({
                "name": match.group(1),
                "params": match.group(2)[:100],
                "file": filepath
            })
    
    def _parse_javascript(self, content: str, filepath: str):
        """Parse JavaScript/TypeScript code"""
        # Find imports
        for match in re.finditer(r'(?:import|require)\s*[\({]?\s*['"]([^'"]+)['"]', content):
            self.imports.append({"file": filepath, "module": match.group(1)})
            if not match.group(1).startswith('.'):
                self.dependencies.add(match.group(1).split('/')[0])
        
        # Find classes
        for match in re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?', content):
            self.classes.append({
                "name": match.group(1),
                "parent": match.group(2),
                "file": filepath
            })
        
        # Find functions
        for match in re.finditer(r'(?:function|const|let|var)\s+(\w+)\s*(?:=\s*)?\(([^)]*)\)', content):
            self.functions.append({
                "name": match.group(1),
                "params": match.group(2)[:100],
                "file": filepath
            })
    
    # ═══════════════════════════════════════════
    # STEP 3: PREPARE - Build context for AI
    # ═══════════════════════════════════════════
    def prepare_for_ai(self, path: str) -> Dict[str, Any]:
        """Prepare structured context for MiMo AI"""
        scan_result = self.scan_directory(path)
        understand_result = self.understand_code(path)
        
        # Build main entry point
        main_file = self._find_main_file(path)
        
        return {
            "project_name": os.path.basename(path),
            "scan": scan_result,
            "understand": understand_result,
            "main_file": main_file,
            "code_snippets": {k: v for k, v in list(self.code_snippets.items())[:10]}
        }
    
    def _find_main_file(self, path: str) -> str:
        """Find the main entry point file"""
        candidates = ['main.py', 'app.py', 'index.py', 'server.py', 'main.js', 'index.js', 'app.js']
        for candidate in candidates:
            if os.path.exists(os.path.join(path, candidate)):
                return candidate
        return self.files[0]["path"] if self.files else "unknown"
