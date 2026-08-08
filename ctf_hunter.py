#!/usr/bin/env python3
"""
CTF_Hunter v5.3 - Ultimate CTF Automation Framework
Live Output | File Support | Task Processing | Multi-Platform
Author: F1REW0LF
License: MIT - Free for Community
Version: 5.3.0
"""

import sys
import os
import re
import json
import time
import random
import hashlib
import base64
import socket
import threading
import queue
import signal
import subprocess
import urllib.parse
import urllib.request
import http.cookiejar
import argparse
import binascii
import zlib
import struct
import codecs
import itertools
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union, Set, Generator
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathlib import Path
from collections import defaultdict, deque
from functools import lru_cache
import hashlib
import warnings
warnings.filterwarnings('ignore')

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

try:
    import requests
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.util.retry import Retry
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    from paramiko import SSHClient, AutoAddPolicy
    SSH_AVAILABLE = True
except ImportError:
    SSH_AVAILABLE = False

# ============================[ VERSION & CONFIGURATION ]================================
VERSION = "5.3.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT - Free for Community"

# ============================[ COLORS ]================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    GOLD = '\033[93m'
    DARK_RED = '\033[31m'
    NEON = '\033[96m'
    ORANGE = '\033[33m'

def cprint(text, color=Colors.WHITE, bold=False):
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.WHITE}")
    else:
        print(f"{color}{text}{Colors.WHITE}")

def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}    ██████╗████████╗███████╗    ███████╗██╗      █████╗  ██████╗ 
    ██╔════╝╚══██╔══╝██╔════╝    ██╔════╝██║     ██╔══██╗██╔════╝ 
    ██║        ██║   █████╗      █████╗  ██║     ███████║██║  ███╗
    ██║        ██║   ██╔══╝      ██╔══╝  ██║     ██╔══██║██║   ██║
    ╚██████╗   ██║   ██║         ██║     ███████╗██║  ██║╚██████╔╝
     ╚═════╝   ╚═╝   ╚═╝         ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
                                                                    
{Colors.RED}{Colors.BOLD}    ULTIMATE CTF AUTOMATION v{VERSION}{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    File Input | Live Output | Multi-Platform{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR}{Colors.WHITE}
"""
    print(banner)

# ============================[ TASK FILE PARSER ]================================

class TaskFileParser:
    """
    Parse task files from CTF labs
    """
    
    def __init__(self):
        self.task_patterns = {
            'flag_file': [
                r'(?:local|root|user|flag|proof)[\s_-]*(?:\.txt|\.flag)?',
                r'what is the ([\w_\-\.]+) flag',
                r'find the ([\w_\-\.]+) file',
                r'cat ([\w_\-\.]+)',
                r'read ([\w_\-\.]+)'
            ],
            'target': [
                r'at (https?://[^\s]+)',
                r'on (https?://[^\s]+)',
                r'http[s]?://[^\s]+',
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            ],
            'platform': [
                r'\[(hackthebox|tryhackme|bugcrowd|vulnhub|picoctf|overthewire)\]',
                r'on (hackthebox|tryhackme|bugcrowd|vulnhub|picoctf|overthewire)'
            ],
            'question': [
                r'Question: (.+?)(?:\n|$)',
                r'Task: (.+?)(?:\n|$)',
                r'What is (.+?)\?',
                r'Find (.+?)(?:\n|$)'
            ],
            'flag_format': [
                r'format: ([A-Z]+)\{',
                r'flag format: ([A-Z]+)\{',
                r'\[([A-Z]+)\{[^}]+\}\]'
            ]
        }
        
    def parse(self, filepath: str) -> Dict:
        """
        Parse task file and extract information
        """
        result = {
            'file': filepath,
            'targets': [],
            'flag_files': [],
            'questions': [],
            'platform': 'auto',
            'flag_format': None,
            'raw_content': '',
            'tasks': []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                result['raw_content'] = content
                
                lines = content.split('\n')
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith(('#', '//', ';')):
                        continue
                    
                    targets = self._extract_targets(line)
                    if targets:
                        result['targets'].extend(targets)
                    
                    flag_files = self._extract_flag_files(line)
                    if flag_files:
                        result['flag_files'].extend(flag_files)
                    
                    question = self._extract_question(line)
                    if question:
                        result['questions'].append(question)
                    
                    platform = self._extract_platform(line)
                    if platform:
                        result['platform'] = platform
                    
                    flag_format = self._extract_flag_format(line)
                    if flag_format:
                        result['flag_format'] = flag_format
                
                result['tasks'] = self._build_tasks(result)
                
        except Exception as e:
            cprint(f"[!] Error parsing file: {e}", Colors.RED)
            result['error'] = str(e)
        
        return result
    
    def _extract_targets(self, line: str) -> List[str]:
        targets = []
        
        for pattern in self.task_patterns['target']:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if match and isinstance(match, str):
                    if not match.startswith(('http://', 'https://')):
                        match = 'https://' + match
                    targets.append(match)
        
        return list(set(targets))
    
    def _extract_flag_files(self, line: str) -> List[str]:
        files = []
        
        for pattern in self.task_patterns['flag_file']:
            matches = re.findall(pattern, line, re.IGNORECASE)
            for match in matches:
                if match:
                    if isinstance(match, tuple):
                        match = match[0]
                    file_match = re.search(r'([\w_\-\.]+\.(?:txt|flag))', match)
                    if file_match:
                        files.append(file_match.group(1))
                    else:
                        common_files = ['flag.txt', 'user.txt', 'root.txt', 'local.txt', 'proof.txt']
                        for f in common_files:
                            if f in match.lower():
                                files.append(f)
        
        return list(set(files)) if files else ['flag.txt', 'user.txt', 'root.txt']
    
    def _extract_question(self, line: str) -> Optional[str]:
        for pattern in self.task_patterns['question']:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_platform(self, line: str) -> Optional[str]:
        for pattern in self.task_patterns['platform']:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        return None
    
    def _extract_flag_format(self, line: str) -> Optional[str]:
        for pattern in self.task_patterns['flag_format']:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        return None
    
    def _build_tasks(self, parsed: Dict) -> List[Dict]:
        tasks = []
        
        targets = parsed.get('targets', [])
        flag_files = parsed.get('flag_files', ['flag.txt', 'user.txt', 'root.txt'])
        questions = parsed.get('questions', [])
        
        if not targets:
            content = parsed.get('raw_content', '')
            ip_match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', content)
            if ip_match:
                targets.append(f"https://{ip_match.group(1)}")
        
        for target in targets:
            for flag_file in flag_files:
                task = {
                    'target': target,
                    'flag_file': flag_file,
                    'question': questions[0] if questions else None,
                    'platform': parsed.get('platform', 'auto'),
                    'flag_format': parsed.get('flag_format')
                }
                tasks.append(task)
        
        return tasks

# ============================[ SMART CACHE ]================================

class SmartCache:
    def __init__(self, max_size: int = 5000, ttl: int = 1800):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                self.misses += 1
                return None
            entry = self.cache[key]
            if time.time() - entry['timestamp'] > self.ttl:
                del self.cache[key]
                self.misses += 1
                return None
            self.hits += 1
            return entry['value']
    
    def set(self, key: str, value: Any):
        with self.lock:
            if len(self.cache) >= self.max_size:
                oldest = min(self.cache.keys(), key=lambda k: self.cache[k]['accessed'])
                del self.cache[oldest]
            self.cache[key] = {'value': value, 'timestamp': time.time(), 'accessed': time.time()}
    
    def clear(self):
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

# ============================[ REAL-TIME MONITOR ]================================

class RealTimeMonitor:
    def __init__(self):
        self.start_time = None
        self.current_task = None
        self.progress = 0
        self.total_tasks = 0
        self.completed = 0
        self.failed = 0
        self.lock = threading.Lock()
        self.running = True
        self.monitor_thread = None
        
    def start(self):
        self.start_time = datetime.now()
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print()
    
    def _monitor_loop(self):
        while self.running:
            self._display_status()
            time.sleep(0.5)
    
    def _display_status(self):
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        pct = (self.completed / self.total_tasks * 100) if self.total_tasks > 0 else 0
        status = f"\r[{Colors.CYAN}▶{Colors.WHITE}] "
        status += f"{Colors.GREEN}{pct:.1f}%{Colors.WHITE} "
        status += f"| {Colors.YELLOW}{self.completed}/{self.total_tasks}{Colors.WHITE} "
        status += f"| {Colors.RED}✗{self.failed}{Colors.WHITE} "
        status += f"| {Colors.BLUE}{elapsed:.0f}s{Colors.WHITE}"
        if self.current_task:
            status += f" | {Colors.PURPLE}{self.current_task[:35]}{Colors.WHITE}"
        sys.stdout.write(status)
        sys.stdout.flush()
    
    def update(self, completed: int, failed: int = 0, task: str = None):
        with self.lock:
            self.completed = completed
            self.failed = failed
            if task:
                self.current_task = task
    
    def set_total(self, total: int):
        with self.lock:
            self.total_tasks = total

# ============================[ AUTO BRUTE-FORCE ]================================

class AutoBruteForce:
    def __init__(self):
        self.wordlists = {
            'common_flags': ['flag', 'FLAG', 'ctf', 'CTF', 'secret', 'key', 'password', 'admin', 'root', 'user'],
            'suffixes': ['1','2','3','4','5','6','7','8','9','0','01','02','03','04','05','flag','txt','backup','old','new'],
            'prefixes': ['flag_', 'FLAG_', 'ctf_', 'CTF_', 'secret_', 'key_', 'password_', 'admin_', 'root_']
        }
        self.attempted = set()
        self.cache = SmartCache(max_size=3000, ttl=1800)
    
    def brute_force(self, target: str, max_depth: int = 5, max_attempts: int = 500) -> List[str]:
        results = []
        attempts = 0
        
        for word in self.wordlists['common_flags']:
            for suffix in self.wordlists['suffixes'][:3]:
                for prefix in self.wordlists['prefixes'][:3]:
                    if attempts >= max_attempts:
                        break
                    variants = [
                        f"{prefix}{word}.txt",
                        f"{word}_{suffix}.txt",
                        f"{word}.{suffix}",
                        f"{word}{suffix}.txt",
                        f"{prefix}{word}{suffix}.txt"
                    ]
                    for variant in variants:
                        if attempts >= max_attempts:
                            break
                        if variant in self.attempted:
                            continue
                        self.attempted.add(variant)
                        attempts += 1
                        if self._test_variant(target, variant):
                            results.append(variant)
                            cprint(f"[+] Brute-force found: {variant}", Colors.GREEN)
                    if results:
                        break
                if results:
                    break
            if results:
                break
        
        if not results:
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            for length in range(4, min(max_depth + 4, 7)):
                for combo in itertools.product(chars, repeat=length):
                    if attempts >= max_attempts:
                        break
                    variant = ''.join(combo) + '.txt'
                    if variant in self.attempted:
                        continue
                    self.attempted.add(variant)
                    attempts += 1
                    if self._test_variant(target, variant):
                        results.append(variant)
                        cprint(f"[+] Brute-force found: {variant}", Colors.GREEN)
                        break
                if results:
                    break
        
        return results
    
    def _test_variant(self, target: str, variant: str) -> bool:
        cache_key = f"{target}:{variant}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        if target.startswith(('http://', 'https://')):
            url = f"{target}/{variant}"
            try:
                if REQUESTS_AVAILABLE:
                    response = requests.head(url, timeout=2, verify=False)
                    if response.status_code == 200:
                        self.cache.set(cache_key, True)
                        return True
            except:
                pass
        
        if os.path.exists(target):
            filepath = os.path.join(target, variant)
            if os.path.isfile(filepath):
                self.cache.set(cache_key, True)
                return True
        
        self.cache.set(cache_key, False)
        return False

# ============================[ OPTIMIZED PARALLEL PROCESSOR ]================================

class OptimizedParallelProcessor:
    def __init__(self, max_workers: int = None):
        if max_workers is None:
            max_workers = min(8, os.cpu_count() * 2)
        self.max_workers = max_workers
        self.monitor = RealTimeMonitor()
    
    def execute(self, tasks: List[Any], worker_func: callable) -> List[Any]:
        results = []
        self.monitor.set_total(len(tasks))
        self.monitor.start()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(worker_func, task): task for task in tasks}
            completed = 0
            failed = 0
            
            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                    completed += 1
                except Exception as e:
                    failed += 1
                    results.append({'error': str(e), 'task': task})
                self.monitor.update(completed, failed, str(task)[:50])
        
        self.monitor.stop()
        return results

# ============================[ MULTI-LAYER DECRYPTION ]================================

class MultiLayerDecryption:
    def decrypt(self, data: str, platform: str = 'auto') -> Dict:
        result = {'original': data, 'final_flag': None, 'success': False, 'layers': 0}
        current = data
        layer_count = 0
        platform_formats = self._get_formats(platform)
        
        while layer_count < 10:
            layer_count += 1
            decoded = self._try_decodings(current)
            if decoded == current:
                break
            if self._is_flag(decoded, platform_formats):
                result['final_flag'] = decoded
                result['success'] = True
                result['layers'] = layer_count
                break
            current = decoded
        
        return result
    
    def _try_decodings(self, data: str) -> str:
        try:
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = bytes.fromhex(data).decode('utf-8', errors='ignore')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = codecs.decode(data, 'rot_13')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = base64.b32decode(data).decode('utf-8', errors='ignore')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = urllib.parse.unquote(data)
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        try:
            decoded = zlib.decompress(base64.b64decode(data)).decode('utf-8', errors='ignore')
            if self._is_valid(decoded):
                return decoded
        except:
            pass
        return data
    
    def _is_valid(self, data: str) -> bool:
        if not data or len(data) < 3:
            return False
        patterns = [r'\{', r'\}', r'flag', r'FLAG', r'CTF', r'HTB', r'THM', r'[a-zA-Z0-9]{32,}']
        for pattern in patterns:
            if re.search(pattern, data, re.IGNORECASE):
                return True
        printable = sum(1 for c in data if c.isprintable())
        return printable / len(data) > 0.8
    
    def _is_flag(self, data: str, formats: List[str]) -> bool:
        for pattern in formats:
            if re.match(pattern, data):
                return True
        patterns = [r'^[A-Za-z0-9_{}]+$', r'^[A-Za-z0-9]{32,}$', r'^[0-9a-f]{32,}$']
        for pattern in patterns:
            if re.match(pattern, data):
                return True
        return False
    
    def _get_formats(self, platform: str) -> List[str]:
        formats = {
            'hackthebox': [r'HTB\{[^}]+\}', r'htb\{[^}]+\}'],
            'tryhackme': [r'THM\{[^}]+\}', r'thm\{[^}]+\}'],
            'bugcrowd': [r'BC\{[^}]+\}', r'FLAG\{[^}]+\}'],
            'picoctf': [r'picoCTF\{[^}]+\}'],
            'vulnhub': [r'VH\{[^}]+\}', r'FLAG\{[^}]+\}'],
            'overthewire': [r'[a-zA-Z0-9]{32,}']
        }
        return formats.get(platform, [r'[A-Za-z0-9_{}]+', r'[a-fA-F0-9]{32,}'])

# ============================[ FLAG HUNTER ]================================

class FlagHunter:
    def __init__(self):
        self.decryptor = MultiLayerDecryption()
        self.cache = SmartCache()
        self.bruteforce = AutoBruteForce()
        self.processor = OptimizedParallelProcessor()
        self.parser = TaskFileParser()
        self.session = self._create_session()
        self.platforms = {
            'hackthebox': {'files': ['flag.txt', 'user.txt', 'root.txt'], 'format': r'HTB\{[^}]+\}'},
            'tryhackme': {'files': ['flag.txt', 'user.txt', 'root.txt', 'answer.txt'], 'format': r'THM\{[^}]+\}'},
            'bugcrowd': {'files': ['flag.txt', 'flag', 'FLAG'], 'format': r'FLAG\{[^}]+\}'},
            'vulnhub': {'files': ['flag.txt', 'user.txt', 'root.txt'], 'format': r'VH\{[^}]+\}'},
            'picoctf': {'files': ['flag.txt', 'flag'], 'format': r'picoCTF\{[^}]+\}'},
            'overthewire': {'files': ['password', 'key.txt'], 'format': r'[a-zA-Z0-9]{32,}'}
        }
    
    def _create_session(self):
        if not REQUESTS_AVAILABLE:
            return None
        s = requests.Session()
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        return s
    
    def hunt_from_file(self, filepath: str) -> Dict:
        """
        Hunt flags using task file
        """
        cprint(f"\n[*] Processing task file: {filepath}", Colors.BLUE)
        
        parsed = self.parser.parse(filepath)
        
        if 'error' in parsed:
            cprint(f"[-] Error: {parsed['error']}", Colors.RED)
            return parsed
        
        cprint(f"[+] Found {len(parsed['targets'])} target(s)", Colors.GREEN)
        cprint(f"[+] Found {len(parsed['flag_files'])} flag file(s)", Colors.GREEN)
        cprint(f"[+] Found {len(parsed['questions'])} question(s)", Colors.GREEN)
        cprint(f"[+] Platform: {parsed['platform']}", Colors.CYAN)
        
        if parsed['flag_format']:
            cprint(f"[+] Flag format: {parsed['flag_format']}", Colors.GOLD)
        
        results = {}
        
        for task in parsed['tasks']:
            target = task['target']
            flag_file = task['flag_file']
            question = task['question']
            platform = task['platform']
            
            cprint(f"\n[*] Task: {target} → {flag_file}", Colors.PURPLE)
            
            result = self.hunt(target, platform, question, flag_files=[flag_file], brute_force=True)
            results[f"{target}_{flag_file}"] = result
        
        return {
            'parsed': parsed,
            'results': results,
            'total_tasks': len(parsed['tasks']),
            'successful': sum(1 for r in results.values() if r.get('success', False))
        }
    
    def hunt(self, target: str, platform: str = 'auto', question: str = None, 
             flag_files: List[str] = None, brute_force: bool = True) -> Dict:
        """
        Hunt flags from target
        """
        result = {'target': target, 'platform': platform, 'question': question, 
                  'flags': [], 'decrypted': [], 'success': False}
        
        if platform == 'auto':
            platform = self._detect_platform(target)
        
        config = self.platforms.get(platform, {'files': ['flag.txt', 'user.txt', 'root.txt']})
        if not flag_files:
            flag_files = config['files']
        
        if question:
            match = re.search(r'(local\.txt|root\.txt|flag\.txt|user\.txt)', question, re.IGNORECASE)
            if match:
                flag_files = [match.group(1)]
        
        tasks = []
        if target.startswith(('http://', 'https://')):
            for f in flag_files:
                for p in ['', '/', '/var/www/', '/home/', '/root/', '/tmp/']:
                    url = f"{target}/{p}{f}" if p else f"{target}/{f}"
                    tasks.append({'type': 'http', 'url': url, 'file': f})
        
        if os.path.exists(target):
            for f in flag_files:
                tasks.append({'type': 'file', 'target': target, 'file': f})
        
        if brute_force and len(tasks) < 30:
            tasks.append({'type': 'bruteforce', 'target': target})
        
        self.processor.monitor.set_total(len(tasks))
        self.processor.monitor.start()
        
        results = self.processor.execute(tasks, self._worker)
        
        self.processor.monitor.stop()
        print()
        
        for r in results:
            if r and 'flags' in r:
                result['flags'].extend(r['flags'])
        
        for flag in result['flags']:
            dec = self.decryptor.decrypt(flag['content'], platform)
            if dec['success']:
                flag['decrypted'] = dec['final_flag']
                result['decrypted'].append(dec['final_flag'])
        
        result['success'] = len(result['decrypted']) > 0
        
        if result['success']:
            cprint(f"\n[!] Found {len(result['decrypted'])} flag(s):", Colors.RED)
            for f in result['decrypted']:
                cprint(f"  {Colors.GOLD}🚩 {f}{Colors.WHITE}", Colors.WHITE)
        else:
            cprint("\n[-] No flags found", Colors.YELLOW)
        
        return result
    
    def _worker(self, task: Dict) -> Dict:
        t = task.get('type')
        if t == 'http':
            return self._hunt_http(task)
        elif t == 'file':
            return self._hunt_file(task)
        elif t == 'bruteforce':
            return self._hunt_bruteforce(task)
        return {'flags': []}
    
    def _hunt_http(self, task: Dict) -> Dict:
        result = {'flags': []}
        cache_key = f"http_{task['url']}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        try:
            if REQUESTS_AVAILABLE:
                r = self.session.get(task['url'], timeout=3, verify=False)
                if r.status_code == 200:
                    content = r.text.strip()
                    if self._is_flag(content):
                        result['flags'].append({'source': task['url'], 'file': task['file'], 'content': content})
                        self.cache.set(cache_key, result)
        except:
            pass
        return result
    
    def _hunt_file(self, task: Dict) -> Dict:
        result = {'flags': []}
        p = Path(task['target'])
        if p.is_file():
            try:
                with open(p, 'r') as f:
                    content = f.read().strip()
                    if self._is_flag(content):
                        result['flags'].append({'source': str(p), 'file': p.name, 'content': content})
            except:
                pass
        elif p.is_dir():
            for path in p.rglob(task['file']):
                try:
                    with open(path, 'r') as f:
                        content = f.read().strip()
                        if self._is_flag(content):
                            result['flags'].append({'source': str(path), 'file': task['file'], 'content': content})
                except:
                    pass
        return result
    
    def _hunt_bruteforce(self, task: Dict) -> Dict:
        result = {'flags': []}
        found = self.bruteforce.brute_force(task['target'])
        for f in found:
            result['flags'].append({'source': f"bruteforce:{f}", 'file': f, 'content': f})
        return result
    
    def _detect_platform(self, target: str) -> str:
        for p in self.platforms:
            if p in target.lower():
                return p
        return 'vulnhub'
    
    def _is_flag(self, content: str) -> bool:
        if not content or len(content) < 8:
            return False
        patterns = [r'\{', r'\}', r'flag', r'FLAG', r'CTF', r'HTB', r'THM', r'[A-Za-z0-9]{32,}']
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        printable = sum(1 for c in content if c.isprintable())
        return printable / len(content) > 0.8

# ============================[ BATCH PROCESSOR ]================================

class BatchProcessor:
    """
    Process multiple task files at once
    """
    
    def __init__(self):
        self.hunter = FlagHunter()
        self.results = {}
        
    def process_directory(self, directory: str) -> Dict:
        """
        Process all task files in a directory
        """
        cprint(f"\n[*] Processing directory: {directory}", Colors.BLUE)
        
        task_files = []
        extensions = ['.txt', '.md', '.task', '.ctf', '.json', '.yml']
        
        for ext in extensions:
            task_files.extend(Path(directory).glob(f'*{ext}'))
        
        if not task_files:
            cprint("[-] No task files found", Colors.RED)
            return {}
        
        cprint(f"[+] Found {len(task_files)} task file(s)", Colors.GREEN)
        
        for task_file in task_files:
            cprint(f"\n[*] Processing: {task_file.name}", Colors.CYAN)
            result = self.hunter.hunt_from_file(str(task_file))
            self.results[str(task_file)] = result
        
        return self.results
    
    def process_files(self, files: List[str]) -> Dict:
        """
        Process multiple task files
        """
        for filepath in files:
            if os.path.exists(filepath):
                cprint(f"\n[*] Processing: {filepath}", Colors.CYAN)
                result = self.hunter.hunt_from_file(filepath)
                self.results[filepath] = result
            else:
                cprint(f"[-] File not found: {filepath}", Colors.RED)
        
        return self.results

# ============================[ MAIN ]================================

class CTF_Hunter:
    def __init__(self):
        self.hunter = FlagHunter()
        self.batch = BatchProcessor()
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] Interrupted", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.BOLD}CTF_Hunter v{VERSION}{Colors.WHITE}
{Colors.CYAN}File Input | Batch Processing | Live Output{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR}{Colors.WHITE}
{Colors.BLUE}{'='*55}{Colors.WHITE}
{Colors.GREEN}[1] Hunt from File (Single){Colors.WHITE}
{Colors.GREEN}[2] Hunt from Directory (Batch){Colors.WHITE}
{Colors.GREEN}[3] Hunt Multiple Files (Batch){Colors.WHITE}
{Colors.GREEN}[4] Hunt Single Target{Colors.WHITE}
{Colors.GREEN}[5] Hunt with Question{Colors.WHITE}
{Colors.GREEN}[6] Decrypt Flag{Colors.WHITE}
{Colors.RED}[7] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] CTF_Hunter v5.3 - Ultimate CTF Automation", Colors.CYAN)
        cprint("[*] File Input | Batch Processing | Live Output", Colors.DIM)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                filepath = input("[>] Task file path: ").strip()
                if os.path.exists(filepath):
                    result = self.hunter.hunt_from_file(filepath)
                    print("\n[+] Summary:")
                    cprint(f"  Total tasks: {result.get('total_tasks', 0)}", Colors.CYAN)
                    cprint(f"  Successful: {result.get('successful', 0)}", Colors.GREEN)
                else:
                    cprint("[-] File not found", Colors.RED)
                
            elif choice == '2':
                directory = input("[>] Directory path: ").strip()
                if os.path.exists(directory) and os.path.isdir(directory):
                    results = self.batch.process_directory(directory)
                    print("\n[+] Summary:")
                    cprint(f"  Total files: {len(results)}", Colors.CYAN)
                    total = sum(r.get('total_tasks', 0) for r in results.values())
                    success = sum(r.get('successful', 0) for r in results.values())
                    cprint(f"  Total tasks: {total}", Colors.CYAN)
                    cprint(f"  Successful: {success}", Colors.GREEN)
                else:
                    cprint("[-] Directory not found", Colors.RED)
                
            elif choice == '3':
                print("[*] Enter file paths (one per line, empty to finish):")
                files = []
                while True:
                    filepath = input("[>] ").strip()
                    if not filepath:
                        break
                    files.append(filepath)
                
                if files:
                    results = self.batch.process_files(files)
                    print("\n[+] Summary:")
                    cprint(f"  Total files: {len(results)}", Colors.CYAN)
                    total = sum(r.get('total_tasks', 0) for r in results.values())
                    success = sum(r.get('successful', 0) for r in results.values())
                    cprint(f"  Total tasks: {total}", Colors.CYAN)
                    cprint(f"  Successful: {success}", Colors.GREEN)
                
            elif choice == '4':
                target = input("[>] Target: ").strip()
                platform = input("[>] Platform (auto/hackthebox/tryhackme/bugcrowd/vulnhub/picoctf/overthewire): ").strip() or 'auto'
                brute = input("[>] Brute-force? (Y/n): ").strip().lower() != 'n'
                self.hunter.hunt(target, platform, brute_force=brute)
                
            elif choice == '5':
                target = input("[>] Target: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                question = input("[>] Question/Description: ").strip()
                brute = input("[>] Brute-force? (Y/n): ").strip().lower() != 'n'
                self.hunter.hunt(target, platform, question, brute_force=brute)
                
            elif choice == '6':
                data = input("[>] Encoded flag: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                result = MultiLayerDecryption().decrypt(data, platform)
                if result['success']:
                    cprint(f"[+] Decrypted: {Colors.GOLD}{result['final_flag']}{Colors.WHITE}", Colors.WHITE)
                    cprint(f"[+] Layers: {result['layers']}", Colors.DIM)
                else:
                    cprint("[-] Failed to decrypt", Colors.RED)
                
            elif choice == '7':
                cprint("[*] Goodbye", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid", Colors.RED)

# ============================[ COMMAND LINE ]================================

def main():
    parser = argparse.ArgumentParser(description="CTF_Hunter v5.3 - Ultimate CTF Automation")
    parser.add_argument("-f", "--file", help="Task file to process")
    parser.add_argument("-d", "--directory", help="Directory with task files")
    parser.add_argument("-t", "--target", help="Target URL/IP/File")
    parser.add_argument("-p", "--platform", default="auto", help="Platform")
    parser.add_argument("-q", "--question", help="Question/Description")
    parser.add_argument("--decrypt", help="Decrypt encoded flag")
    parser.add_argument("--no-brute", action="store_true", help="Disable brute-force")
    parser.add_argument("--batch", nargs='+', help="Multiple task files to process")
    
    args = parser.parse_args()
    
    if args.directory:
        print_banner()
        batch = BatchProcessor()
        results = batch.process_directory(args.directory)
        print("\n[+] Summary:")
        cprint(f"  Total files: {len(results)}", Colors.CYAN)
        total = sum(r.get('total_tasks', 0) for r in results.values())
        success = sum(r.get('successful', 0) for r in results.values())
        cprint(f"  Total tasks: {total}", Colors.CYAN)
        cprint(f"  Successful: {success}", Colors.GREEN)
        sys.exit(0)
    
    if args.batch:
        print_banner()
        batch = BatchProcessor()
        results = batch.process_files(args.batch)
        print("\n[+] Summary:")
        cprint(f"  Total files: {len(results)}", Colors.CYAN)
        total = sum(r.get('total_tasks', 0) for r in results.values())
        success = sum(r.get('successful', 0) for r in results.values())
        cprint(f"  Total tasks: {total}", Colors.CYAN)
        cprint(f"  Successful: {success}", Colors.GREEN)
        sys.exit(0)
    
    if args.file:
        print_banner()
        hunter = FlagHunter()
        result = hunter.hunt_from_file(args.file)
        print("\n[+] Summary:")
        cprint(f"  Total tasks: {result.get('total_tasks', 0)}", Colors.CYAN)
        cprint(f"  Successful: {result.get('successful', 0)}", Colors.GREEN)
        sys.exit(0)
    
    if args.decrypt:
        print_banner()
        result = MultiLayerDecryption().decrypt(args.decrypt, args.platform)
        if result['success']:
            cprint(f"[+] Decrypted: {Colors.GOLD}{result['final_flag']}{Colors.WHITE}", Colors.WHITE)
            cprint(f"[+] Layers: {result['layers']}", Colors.DIM)
        else:
            cprint("[-] Failed to decrypt", Colors.RED)
        sys.exit(0)
    
    if args.target:
        print_banner()
        hunter = FlagHunter()
        hunter.hunt(args.target, args.platform, args.question, brute_force=not args.no_brute)
        sys.exit(0)
    
    # Interactive
    tool = CTF_Hunter()
    tool.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        cprint("\n[!] Interrupted", Colors.RED)
        sys.exit(0)
    except Exception as e:
        cprint(f"\n[!] Error: {e}", Colors.RED)
        sys.exit(1)
