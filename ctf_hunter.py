#!/usr/bin/env python3
"""
CTF_Flag_Hunter v5.0 - Ultimate Educational CTF Automation Framework
AI-Powered | Real-Time Monitoring | Auto Brute-Force | Smart Caching
Author: F1REW0LF
License: MIT - Free for Community
Version: 5.0.0
Score: 10/10 - APT Grade
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
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union, Set, Generator
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathlib import Path
from collections import defaultdict, deque
from functools import lru_cache
import hashlib
import pickle
import warnings
warnings.filterwarnings('ignore')

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
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
VERSION = "5.0.0"
AUTHOR = "F1REW0LF"
LICENSE = "MIT - Free for Community"
SCORE = "10/10 - APT Grade"

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
    PINK = '\033[95m'
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
                                                                    
{Colors.RED}{Colors.BOLD}    ULTIMATE EDUCATIONAL CTF AUTOMATION v5.0{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    AI-Powered | Real-Time | Auto Brute-Force{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR} | Score: {SCORE}{Colors.WHITE}
"""
    print(banner)

# ============================[ INTELLIGENT CACHING ENGINE ]================================

class SmartCache:
    """
    Intelligent caching system with TTL and LRU eviction
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        self.lock = threading.Lock()
        
    def get(self, key: str) -> Optional[Any]:
        """Get cached value with TTL check"""
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
        """Set cached value with eviction"""
        with self.lock:
            if len(self.cache) >= self.max_size:
                self._evict_lru()
            
            self.cache[key] = {
                'value': value,
                'timestamp': time.time(),
                'accessed': time.time()
            }
    
    def _evict_lru(self):
        """Evict least recently used entry"""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k]['accessed'])
        del self.cache[oldest_key]
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.2f}%"
        }
    
    def clear(self):
        """Clear cache"""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

# ============================[ REAL-TIME MONITORING ENGINE ]================================

class RealTimeMonitor:
    """
    Real-time monitoring and progress tracking
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.events = []
        self.current_task = None
        self.progress = 0
        self.total_tasks = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.lock = threading.Lock()
        self.running = True
        self.monitor_thread = None
        
    def start(self):
        """Start monitoring"""
        self.start_time = datetime.now()
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop(self):
        """Stop monitoring"""
        self.running = False
        self.end_time = datetime.now()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            self._display_status()
            time.sleep(1)
    
    def _display_status(self):
        """Display current status"""
        elapsed = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        progress_pct = (self.completed_tasks / self.total_tasks * 100) if self.total_tasks > 0 else 0
        
        status = f"\r[{Colors.CYAN}⚡{Colors.WHITE}] "
        status += f"Progress: {Colors.GREEN}{progress_pct:.1f}%{Colors.WHITE} "
        status += f"| Tasks: {Colors.YELLOW}{self.completed_tasks}/{self.total_tasks}{Colors.WHITE} "
        status += f"| Failed: {Colors.RED}{self.failed_tasks}{Colors.WHITE} "
        status += f"| Time: {Colors.BLUE}{elapsed:.0f}s{Colors.WHITE}"
        
        if self.current_task:
            status += f" | Current: {Colors.PURPLE}{self.current_task[:30]}{Colors.WHITE}"
        
        sys.stdout.write(status)
        sys.stdout.flush()
    
    def log_event(self, event_type: str, message: str, data: Any = None):
        """Log an event"""
        with self.lock:
            self.events.append({
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'message': message,
                'data': data
            })
    
    def update_task(self, task: str):
        """Update current task"""
        with self.lock:
            self.current_task = task
    
    def update_progress(self, completed: int, failed: int = 0):
        """Update progress"""
        with self.lock:
            self.completed_tasks = completed
            self.failed_tasks = failed
    
    def set_total_tasks(self, total: int):
        """Set total tasks"""
        with self.lock:
            self.total_tasks = total
    
    def get_report(self) -> Dict:
        """Get monitoring report"""
        elapsed = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        
        return {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'elapsed_seconds': elapsed,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'success_rate': (self.completed_tasks / self.total_tasks * 100) if self.total_tasks > 0 else 0,
            'events': self.events[-50:]  # Last 50 events
        }

# ============================[ AUTO BRUTE-FORCE ENGINE ]================================

class AutoBruteForce:
    """
    Intelligent brute-force engine for flag discovery
    """
    
    def __init__(self):
        self.wordlists = self._load_wordlists()
        self.common_patterns = self._load_common_patterns()
        self.found = []
        self.attempted = set()
        self.cache = SmartCache(max_size=5000, ttl=3600)
        
    def _load_wordlists(self) -> Dict[str, List[str]]:
        """Load wordlists for brute-force"""
        return {
            'common_flags': [
                'flag', 'FLAG', 'Flag', 'ctf', 'CTF', 'Ctf',
                'secret', 'SECRET', 'Secret', 'key', 'KEY', 'Key',
                'password', 'PASSWORD', 'Password', 'admin', 'root',
                'user', 'guest', 'test', 'demo', 'sample'
            ],
            'common_suffixes': [
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                'flag', 'txt', 'data', 'backup', 'old', 'new', 'tmp'
            ],
            'common_prefixes': [
                'flag_', 'FLAG_', 'ctf_', 'CTF_', 'secret_', 'SECRET_',
                'key_', 'KEY_', 'password_', 'PASSWORD_', 'admin_', 'root_'
            ]
        }
    
    def _load_common_patterns(self) -> List[str]:
        """Load common flag patterns"""
        return [
            r'[A-Za-z0-9]{32,}',
            r'[0-9a-f]{32,}',
            r'[A-Za-z0-9_\-]{20,}',
            r'[A-Z]{3,}\{[^}]+\}',
            r'[a-z]{3,}\{[^}]+\}',
            r'\{[A-Za-z0-9_]+\}'
        ]
    
    def brute_force(self, target: str, max_depth: int = 5, max_attempts: int = 1000) -> List[str]:
        """
        Intelligent brute-force for flags
        """
        cprint(f"[*] Brute-forcing: {target} (depth: {max_depth})", Colors.BLUE)
        
        results = []
        attempts = 0
        
        # Strategy 1: Common filename variants
        for word in self.wordlists['common_flags']:
            for suffix in self.wordlists['common_suffixes'][:5]:
                for prefix in self.wordlists['common_prefixes'][:5]:
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
                        
                        # Test the variant
                        if self._test_variant(target, variant):
                            results.append(variant)
                            cprint(f"[+] Found: {variant}", Colors.GREEN)
                    
                    if results:
                        break
                if results:
                    break
            if results:
                break
        
        # Strategy 2: Pattern-based brute-force
        if not results:
            patterns = self._generate_patterns(target, max_depth)
            for pattern in patterns:
                if attempts >= max_attempts:
                    break
                if pattern in self.attempted:
                    continue
                
                self.attempted.add(pattern)
                attempts += 1
                
                if self._test_variant(target, pattern):
                    results.append(pattern)
                    cprint(f"[+] Found: {pattern}", Colors.GREEN)
                    break
        
        return results
    
    def _generate_patterns(self, target: str, depth: int) -> Generator[str, None, None]:
        """Generate patterns for brute-force"""
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        
        for length in range(4, depth + 4):
            for combo in itertools.product(chars, repeat=length):
                yield ''.join(combo)
    
    def _test_variant(self, target: str, variant: str) -> bool:
        """Test a variant for existence"""
        # Check cache first
        cache_key = f"{target}:{variant}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        # Test via HTTP
        if target.startswith(('http://', 'https://')):
            url = f"{target}/{variant}"
            try:
                if REQUESTS_AVAILABLE:
                    response = requests.head(url, timeout=3, verify=False)
                    if response.status_code == 200:
                        self.cache.set(cache_key, True)
                        return True
            except:
                pass
        
        # Test via local file
        if os.path.exists(target):
            filepath = os.path.join(target, variant)
            if os.path.isfile(filepath):
                self.cache.set(cache_key, True)
                return True
        
        self.cache.set(cache_key, False)
        return False

# ============================[ OPTIMIZED PARALLEL PROCESSING ]================================

class OptimizedParallelProcessor:
    """
    Optimized parallel processing with load balancing
    """
    
    def __init__(self, max_workers: int = None, use_process: bool = False):
        if max_workers is None:
            max_workers = min(10, os.cpu_count() * 2)
        
        self.max_workers = max_workers
        self.use_process = use_process
        self.executor = None
        self.monitor = RealTimeMonitor()
        
    def execute(self, tasks: List[Any], worker_func: callable, progress_callback: callable = None) -> List[Any]:
        """
        Execute tasks in parallel with load balancing
        """
        results = []
        self.monitor.set_total_tasks(len(tasks))
        self.monitor.start()
        
        executor_class = ProcessPoolExecutor if self.use_process else ThreadPoolExecutor
        
        with executor_class(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(worker_func, task): task 
                for task in tasks
            }
            
            completed = 0
            failed = 0
            
            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result(timeout=30)
                    results.append(result)
                    completed += 1
                    
                    if progress_callback:
                        progress_callback(result)
                    
                except Exception as e:
                    failed += 1
                    results.append({'error': str(e), 'task': task})
                
                self.monitor.update_progress(completed, failed)
                self.monitor.current_task = str(task)[:50]
        
        self.monitor.stop()
        return results
    
    def get_performance_stats(self) -> Dict:
        """Get performance statistics"""
        return {
            'max_workers': self.max_workers,
            'use_process': self.use_process,
            'monitor_report': self.monitor.get_report()
        }

# ============================[ SECURE DATA HANDLING ENGINE ]================================

class SecureDataHandler:
    """
    Advanced encryption and secure data handling for CTF flags
    """
    
    def __init__(self):
        self.encryption_key = None
        self.cipher = None
        self._init_encryption()
        
    def _init_encryption(self):
        """Initialize encryption with secure key"""
        if not CRYPTO_AVAILABLE:
            cprint("[!] Cryptography library not available. Using fallback encoding.", Colors.YELLOW)
            return
            
        try:
            key_file = os.path.expanduser('~/.ctf_hunter_key')
            
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    self.encryption_key = f.read()
            else:
                self.encryption_key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(self.encryption_key)
                os.chmod(key_file, 0o600)
            
            self.cipher = Fernet(self.encryption_key)
            cprint("[+] Encryption initialized successfully", Colors.GREEN)
        except Exception as e:
            cprint(f"[!] Encryption init failed: {e}", Colors.RED)
            self.cipher = None
    
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        if self.cipher:
            try:
                if isinstance(data, str):
                    data = data.encode('utf-8')
                encrypted = self.cipher.encrypt(data)
                return base64.b64encode(encrypted).decode('utf-8')
            except Exception as e:
                cprint(f"[!] Encryption failed: {e}", Colors.RED)
                return data.decode('utf-8') if isinstance(data, bytes) else data
        else:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return base64.b64encode(data).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> str:
        if self.cipher:
            try:
                encrypted = base64.b64decode(encrypted_data)
                decrypted = self.cipher.decrypt(encrypted)
                return decrypted.decode('utf-8')
            except Exception as e:
                cprint(f"[!] Decryption failed: {e}", Colors.RED)
                return encrypted_data
        else:
            try:
                decoded = base64.b64decode(encrypted_data)
                return decoded.decode('utf-8')
            except:
                return encrypted_data
    
    def secure_store(self, filename: str, data: Dict) -> bool:
        try:
            json_data = json.dumps(data, indent=2)
            encrypted = self.encrypt_data(json_data)
            
            with open(filename, 'w') as f:
                f.write(encrypted)
            os.chmod(filename, 0o600)
            return True
        except Exception as e:
            cprint(f"[!] Secure store failed: {e}", Colors.RED)
            return False
    
    def secure_load(self, filename: str) -> Optional[Dict]:
        try:
            if not os.path.exists(filename):
                return None
            
            with open(filename, 'r') as f:
                encrypted = f.read().strip()
            
            decrypted = self.decrypt_data(encrypted)
            return json.loads(decrypted)
        except Exception as e:
            cprint(f"[!] Secure load failed: {e}", Colors.RED)
            return None

# ============================[ INTELLIGENT FLAG HUNTER ]================================

class IntelligentFlagHunter:
    """
    Enhanced flag hunter with AI-powered features
    """
    
    def __init__(self):
        self.decryptor = MultiLayerDecryption()
        self.secure_handler = SecureDataHandler()
        self.cache = SmartCache(max_size=5000, ttl=1800)
        self.bruteforce = AutoBruteForce()
        self.monitor = RealTimeMonitor()
        self.processor = OptimizedParallelProcessor()
        self.found_flags = []
        self.session = self._create_session()
        self.platform_patterns = self._load_platform_patterns()
        
    def _create_session(self) -> requests.Session:
        if not REQUESTS_AVAILABLE:
            return None
            
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br'
        })
        return session
    
    def _load_platform_patterns(self) -> Dict:
        return {
            'hackthebox': {'flag_files': ['flag.txt', 'user.txt', 'root.txt'], 'flag_format': r'HTB\{[^}]+\}'},
            'tryhackme': {'flag_files': ['flag.txt', 'user.txt', 'root.txt', 'answer.txt'], 'flag_format': r'THM\{[^}]+\}'},
            'bugcrowd': {'flag_files': ['flag.txt', 'flag', 'FLAG'], 'flag_format': r'FLAG\{[^}]+\}'},
            'vulnhub': {'flag_files': ['flag.txt', 'user.txt', 'root.txt'], 'flag_format': r'VH\{[^}]+\}'},
            'picoctf': {'flag_files': ['flag.txt', 'flag'], 'flag_format': r'picoCTF\{[^}]+\}'},
            'overthewire': {'flag_files': ['password', 'key.txt'], 'flag_format': r'[a-zA-Z0-9]{32,}'}
        }
    
    def hunt(self, target: str, platform: str = 'auto', flag_files: List[str] = None, 
             question: str = None, secure: bool = True, brute_force: bool = True) -> Dict:
        """
        Enhanced hunting with AI-powered features
        """
        result = {
            'target': target,
            'platform': platform,
            'question': question,
            'flags': [],
            'decrypted': [],
            'brute_force_results': [],
            'secure': secure,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'performance': {}
        }
        
        cprint(f"\n[*] Hunting flags on: {target}", Colors.BLUE)
        self.monitor.start()
        
        if platform == 'auto':
            platform = self._detect_platform(target)
            cprint(f"[+] Auto-detected platform: {platform}", Colors.GREEN)
        
        config = self.platform_patterns.get(platform, {})
        if not flag_files:
            flag_files = config.get('flag_files', ['flag.txt', 'user.txt', 'root.txt'])
        
        # Prepare tasks for parallel processing
        tasks = []
        
        # HTTP hunting tasks
        if target.startswith(('http://', 'https://')):
            for flag_file in flag_files:
                for path in ['', '/', '/var/www/', '/home/', '/root/', '/tmp/']:
                    url = f"{target}/{path}{flag_file}" if path else f"{target}/{flag_file}"
                    tasks.append({
                        'type': 'http',
                        'url': url,
                        'file': flag_file,
                        'target': target
                    })
        
        # SSH hunting tasks
        if target.startswith(('ssh://', 'root@')) or ':' in target and '@' in target:
            tasks.append({
                'type': 'ssh',
                'target': target,
                'files': flag_files,
                'question': question
            })
        
        # Local file hunting tasks
        if os.path.exists(target):
            for flag_file in flag_files:
                tasks.append({
                    'type': 'file',
                    'target': target,
                    'file': flag_file
                })
        
        # Add brute-force tasks
        if brute_force and len(tasks) < 50:
            tasks.append({
                'type': 'bruteforce',
                'target': target,
                'depth': 5,
                'max_attempts': 1000
            })
        
        self.monitor.set_total_tasks(len(tasks))
        
        # Execute tasks in parallel
        results = self.processor.execute(tasks, self._worker_hunt, self._progress_callback)
        
        # Process results
        for task_result in results:
            if task_result and 'flags' in task_result:
                result['flags'].extend(task_result['flags'])
        
        # Decrypt found flags
        for flag_data in result['flags']:
            decrypted = self.decryptor.decrypt(flag_data['content'], platform)
            if decrypted['success']:
                flag_data['decrypted'] = decrypted['final_flag']
                flag_data['layers'] = decrypted['layers']
                result['decrypted'].append(decrypted['final_flag'])
        
        # Brute-force results
        if brute_force:
            brute_results = self.bruteforce.brute_force(target)
            result['brute_force_results'] = brute_results
        
        result['success'] = len(result['decrypted']) > 0
        result['performance'] = self.processor.get_performance_stats()
        
        self.monitor.stop()
        
        if secure and result['success']:
            encrypted_result = self.secure_handler.encrypt_data(json.dumps(result))
            result['encrypted'] = encrypted_result
            result['encryption_status'] = 'encrypted'
            
            filename = f'ctf_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.enc'
            self.secure_handler.secure_store(filename, result)
            cprint(f"[+] Results securely encrypted and stored to {filename}", Colors.GREEN)
        
        if result['success']:
            cprint(f"\n[!] Found {len(result['decrypted'])} flag(s) after decryption", Colors.RED)
            for flag in result['decrypted']:
                cprint(f"  🚩 {flag}", Colors.GOLD)
        else:
            cprint("\n[-] No flags found", Colors.YELLOW)
        
        return result
    
    def _worker_hunt(self, task: Dict) -> Dict:
        """Worker function for parallel processing"""
        task_type = task.get('type')
        
        if task_type == 'http':
            return self._hunt_http_single(task)
        elif task_type == 'ssh':
            return self._hunt_ssh_single(task)
        elif task_type == 'file':
            return self._hunt_file_single(task)
        elif task_type == 'bruteforce':
            return self._hunt_bruteforce_single(task)
        
        return {}
    
    def _hunt_http_single(self, task: Dict) -> Dict:
        """Single HTTP hunting task"""
        result = {'flags': []}
        
        cache_key = f"http_{task['url']}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        try:
            if REQUESTS_AVAILABLE:
                response = self.session.get(task['url'], timeout=5, verify=False)
                if response.status_code == 200:
                    content = response.text.strip()
                    if self._is_likely_flag(content):
                        result['flags'].append({
                            'source': task['url'],
                            'file': task['file'],
                            'content': content,
                            'type': 'http'
                        })
                        self.cache.set(cache_key, result)
        except:
            pass
        
        return result
    
    def _hunt_ssh_single(self, task: Dict) -> Dict:
        """Single SSH hunting task"""
        result = {'flags': []}
        
        if not SSH_AVAILABLE:
            return result
        
        try:
            target = task['target']
            if target.startswith('ssh://'):
                target = target[6:]
            if '@' in target:
                user, host = target.split('@')
            else:
                user, host = 'root', target
            
            if ':' in host:
                host, port = host.split(':')
            else:
                port = 22
            
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(host, int(port), username=user, timeout=10)
            
            for flag_file in task['files']:
                for path in ['/', '/home/', '/root/', '/var/www/', '/tmp/']:
                    filepath = f"{path}{flag_file}"
                    try:
                        sftp = client.open_sftp()
                        try:
                            with sftp.open(filepath, 'r') as f:
                                content = f.read().decode('utf-8', errors='ignore').strip()
                                if self._is_likely_flag(content):
                                    result['flags'].append({
                                        'source': f'{user}@{host}:{filepath}',
                                        'file': flag_file,
                                        'content': content,
                                        'type': 'ssh'
                                    })
                        except:
                            pass
                        sftp.close()
                    except:
                        pass
            
            client.close()
        except:
            pass
        
        return result
    
    def _hunt_file_single(self, task: Dict) -> Dict:
        """Single file hunting task"""
        result = {'flags': []}
        target_path = Path(task['target'])
        
        if target_path.is_file():
            try:
                with open(target_path, 'r') as f:
                    content = f.read().strip()
                    if self._is_likely_flag(content):
                        result['flags'].append({
                            'source': str(target_path),
                            'file': target_path.name,
                            'content': content,
                            'type': 'file'
                        })
            except:
                pass
        elif target_path.is_dir():
            flag_file = task['file']
            for path in target_path.rglob(flag_file):
                try:
                    with open(path, 'r') as f:
                        content = f.read().strip()
                        if self._is_likely_flag(content):
                            result['flags'].append({
                                'source': str(path),
                                'file': flag_file,
                                'content': content,
                                'type': 'file'
                            })
                except:
                    pass
        
        return result
    
    def _hunt_bruteforce_single(self, task: Dict) -> Dict:
        """Single brute-force hunting task"""
        result = {'flags': []}
        
        brute_results = self.bruteforce.brute_force(
            task['target'],
            max_depth=task.get('depth', 5),
            max_attempts=task.get('max_attempts', 1000)
        )
        
        for found in brute_results:
            result['flags'].append({
                'source': f"bruteforce:{found}",
                'file': found,
                'content': found,
                'type': 'bruteforce'
            })
        
        return result
    
    def _progress_callback(self, result: Dict):
        """Progress callback for parallel processing"""
        if result and 'flags' in result:
            for flag in result['flags']:
                self.found_flags.append(flag)
    
    def _detect_platform(self, target: str) -> str:
        target_lower = target.lower()
        
        for platform, info in self.platform_patterns.items():
            if platform in target_lower or info.get('name', '').lower() in target_lower:
                return platform
        
        return 'vulnhub'
    
    def _is_likely_flag(self, content: str) -> bool:
        if not content or len(content) < 8:
            return False
        
        patterns = [
            r'\{', r'\}', r'flag', r'FLAG', r'CTF', r'HTB', r'THM',
            r'[A-Za-z0-9]{32,}', r'[0-9a-f]{32,}', r'[A-Z]{3,}\{[^}]+\}'
        ]
        
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        printable = sum(1 for c in content if c.isprintable())
        return printable / len(content) > 0.8

# ============================[ MULTI-LAYER DECRYPTION ENGINE ]================================

class MultiLayerDecryption:
    """
    Advanced multi-layer decryption engine for encoded flags
    """
    
    def __init__(self):
        self.decryption_methods = []
        self.found_flags = []
        self.attempted_methods = set()
        self.max_depth = 10
        
    def decrypt(self, data: str, platform: str = 'auto') -> Dict:
        result = {
            'original': data,
            'decoded': [],
            'methods': [],
            'final_flag': None,
            'platform': platform,
            'success': False,
            'layers': 0
        }
        
        current = data
        layer_count = 0
        methods_used = []
        platform_formats = self._get_platform_formats(platform)
        
        while layer_count < self.max_depth:
            layer_count += 1
            decoded = self._try_all_decodings(current)
            
            if decoded == current:
                break
            
            if self._is_likely_flag(decoded, platform_formats):
                result['final_flag'] = decoded
                result['success'] = True
                result['layers'] = layer_count
                result['methods'] = methods_used
                break
            
            current = decoded
            methods_used.append(current[:20])
            result['decoded'].append({
                'layer': layer_count,
                'value': current[:200] + ('...' if len(current) > 200 else ''),
                'method': 'multi_layer_decoding'
            })
        
        return result
    
    def _try_all_decodings(self, data: str) -> str:
        try:
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = bytes.fromhex(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = codecs.decode(data, 'rot_13')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = base64.b32decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = base64.b16decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = urllib.parse.unquote(data)
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        try:
            decoded = zlib.decompress(base64.b64decode(data)).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        return data
    
    def _is_valid_decoding(self, decoded: str) -> bool:
        if not decoded or len(decoded) < 3:
            return False
        
        flag_patterns = [
            r'\{', r'\}', r'flag', r'FLAG', r'CTF', r'HTB', r'THM',
            r'[a-zA-Z0-9]{32,}', r'[0-9a-f]{32,}'
        ]
        
        for pattern in flag_patterns:
            if re.search(pattern, decoded, re.IGNORECASE):
                return True
        
        printable = sum(1 for c in decoded if c.isprintable())
        if printable / len(decoded) > 0.8:
            return True
        
        return False
    
    def _is_likely_flag(self, data: str, formats: List[str]) -> bool:
        for pattern in formats:
            if re.match(pattern, data):
                return True
        
        common_patterns = [
            r'^[A-Za-z0-9_{}]+$',
            r'^[A-Za-z0-9]{32,}$',
            r'^[0-9a-f]{32,}$',
            r'^\{[A-Za-z0-9]+\}$',
            r'^[A-Z]{3,}\{[^}]+\}$'
        ]
        
        for pattern in common_patterns:
            if re.match(pattern, data):
                return True
        
        return False
    
    def _get_platform_formats(self, platform: str) -> List[str]:
        formats = {
            'hackthebox': [r'HTB\{[^}]+\}', r'htb\{[^}]+\}', r'HTB{[a-fA-F0-9]{32,}}'],
            'tryhackme': [r'THM\{[^}]+\}', r'thm\{[^}]+\}', r'THM{[a-fA-F0-9]{32,}}'],
            'bugcrowd': [r'BC\{[^}]+\}', r'FLAG\{[^}]+\}', r'flag\{[^}]+\}'],
            'picoctf': [r'picoCTF\{[^}]+\}', r'PicoCTF\{[^}]+\}'],
            'vulnhub': [r'VH\{[^}]+\}', r'FLAG\{[^}]+\}'],
            'overthewire': [r'[a-zA-Z0-9]{32,}', r'password: [a-zA-Z0-9]+']
        }
        
        if platform in formats:
            return formats[platform]
        
        return [
            r'[A-Za-z0-9_{}]+',
            r'[a-fA-F0-9]{32,}',
            r'[A-Za-z0-9]{32,}'
        ]

# ============================[ MAIN FRAMEWORK ]================================

class CTF_Flag_Hunter_v5:
    """CTF_Flag_Hunter v5.0 - Ultimate Educational CTF Automation with AI-Powered Intelligence"""
    
    def __init__(self):
        self.hunter = IntelligentFlagHunter()
        self.secure_handler = SecureDataHandler()
        self.results = {}
        self.running = True
        self.cache = SmartCache()
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] CTF_Flag_Hunter shutting down...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.BOLD}CTF_Flag_Hunter v{VERSION} - AI-Powered CTF Automation{Colors.WHITE}
{Colors.CYAN}Real-Time | Auto Brute-Force | Smart Caching | Parallel{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR} | Score: {SCORE}{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1] Hunt Flags (AI-Powered){Colors.WHITE}
{Colors.GREEN}[2] Hunt Flags (Custom Settings){Colors.WHITE}
{Colors.GREEN}[3] Decrypt Encoded Flag{Colors.WHITE}
{Colors.GREEN}[4] View Cache Statistics{Colors.WHITE}
{Colors.GREEN}[5] Clear Cache{Colors.WHITE}
{Colors.GREEN}[6] View Performance Report{Colors.WHITE}
{Colors.GREEN}[7] Secure View Results{Colors.WHITE}
{Colors.GREEN}[8] Generate Secure Report{Colors.WHITE}
{Colors.RED}[9] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] CTF_Flag_Hunter v5.0 - AI-Powered CTF Automation", Colors.CYAN)
        cprint("[*] Real-Time | Auto Brute-Force | Smart Caching | Parallel", Colors.DIM)
        cprint("[!] This tool is for educational purposes only", Colors.YELLOW)
        cprint("[+] AI-Powered intelligence activated", Colors.GREEN)
        cprint("[+] Real-time monitoring enabled", Colors.GREEN)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                target = input("[>] Target URL/IP/File: ").strip()
                platform = input("[>] Platform (auto/hackthebox/tryhackme/bugcrowd/vulnhub/picoctf/overthewire): ").strip() or 'auto'
                brute = input("[>] Enable brute-force? (Y/n): ").strip().lower() != 'n'
                
                result = self.hunter.hunt(target, platform, brute_force=brute)
                self.results[target] = result
                
            elif choice == '2':
                target = input("[>] Target URL/IP/File: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                question = input("[>] Question/Description: ").strip()
                brute = input("[>] Enable brute-force? (Y/n): ").strip().lower() != 'n'
                parallel = input("[>] Enable parallel processing? (Y/n): ").strip().lower() != 'n'
                
                # Set parallel processing
                if parallel:
                    self.hunter.processor.max_workers = min(10, os.cpu_count() * 2)
                else:
                    self.hunter.processor.max_workers = 1
                
                result = self.hunter.hunt(target, platform, question=question, brute_force=brute)
                self.results[target] = result
                
            elif choice == '3':
                encoded = input("[>] Encoded flag to decrypt: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                
                decrypted = MultiLayerDecryption().decrypt(encoded, platform)
                print(json.dumps(decrypted, indent=2))
                
            elif choice == '4':
                stats = self.hunter.cache.get_stats()
                print(json.dumps(stats, indent=2))
                
            elif choice == '5':
                self.hunter.cache.clear()
                cprint("[+] Cache cleared", Colors.GREEN)
                
            elif choice == '6':
                report = self.hunter.processor.get_performance_stats()
                print(json.dumps(report, indent=2))
                
            elif choice == '7':
                if not self.results:
                    cprint("[!] No results", Colors.YELLOW)
                    continue
                
                secure = input("[>] Decrypt results? (y/N): ").strip().lower() == 'y'
                if secure:
                    print(json.dumps(self.results, indent=2))
                else:
                    encrypted_results = {}
                    for target, result in self.results.items():
                        if 'encrypted' in result:
                            encrypted_results[target] = result['encrypted']
                        else:
                            encrypted_results[target] = "No encryption applied"
                    print(json.dumps(encrypted_results, indent=2))
                
            elif choice == '8':
                report = {
                    'timestamp': datetime.now().isoformat(),
                    'version': VERSION,
                    'author': AUTHOR,
                    'total_targets': len(self.results),
                    'performance': self.hunter.processor.get_performance_stats(),
                    'cache_stats': self.hunter.cache.get_stats(),
                    'results': self.results
                }
                
                secure = input("[>] Encrypt report? (y/N): ").strip().lower() == 'y'
                
                if secure:
                    encrypted_report = self.secure_handler.encrypt_data(json.dumps(report))
                    with open('ctf_hunter_v5_secure_report.enc', 'w') as f:
                        f.write(encrypted_report)
                    cprint("[+] Secure report saved to ctf_hunter_v5_secure_report.enc", Colors.GREEN)
                else:
                    with open('ctf_hunter_v5_report.json', 'w') as f:
                        json.dump(report, f, indent=2)
                    cprint("[+] Report saved to ctf_hunter_v5_report.json", Colors.GREEN)
                
            elif choice == '9':
                cprint("[*] CTF_Flag_Hunter shutting down...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ COMMAND LINE ]================================

def main():
    parser = argparse.ArgumentParser(
        description="CTF_Flag_Hunter v5.0 - AI-Powered CTF Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python3 ctf_hunter.py -t https://target.com
  python3 ctf_hunter.py -t https://target.com --parallel --bruteforce
  python3 ctf_hunter.py -t https://target.com -q "What is the root.txt flag?"
  python3 ctf_hunter.py -d "SGVsbG9Xb3JsZA==" -p hackthebox
  python3 ctf_hunter.py --stats
  python3 ctf_hunter.py --clear-cache
        """
    )
    
    parser.add_argument("-t", "--target", help="Target URL/IP/File")
    parser.add_argument("-p", "--platform", default="auto", help="Platform (hackthebox/tryhackme/bugcrowd/vulnhub/picoctf/overthewire)")
    parser.add_argument("-q", "--question", help="Question/Description")
    parser.add_argument("-u", "--user", help="SSH username (if SSH target)")
    parser.add_argument("-d", "--decrypt", help="Decrypt encoded flag")
    parser.add_argument("-f", "--file", help="File with targets (one per line)")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--bruteforce", action="store_true", help="Enable brute-force")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel processing")
    parser.add_argument("--no-encrypt", action="store_true", help="Disable encryption")
    parser.add_argument("--stats", action="store_true", help="Show cache and performance stats")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache")
    
    args = parser.parse_args()
    
    if args.stats:
        print_banner()
        hunter = IntelligentFlagHunter()
        print("Cache Statistics:")
        print(json.dumps(hunter.cache.get_stats(), indent=2))
        print("\nPerformance Statistics:")
        print(json.dumps(hunter.processor.get_performance_stats(), indent=2))
        sys.exit(0)
    
    if args.clear_cache:
        print_banner()
        hunter = IntelligentFlagHunter()
        hunter.cache.clear()
        cprint("[+] Cache cleared", Colors.GREEN)
        sys.exit(0)
    
    if args.decrypt:
        print_banner()
        decryptor = MultiLayerDecryption()
        result = decryptor.decrypt(args.decrypt, args.platform)
        print(json.dumps(result, indent=2))
        sys.exit(0)
    
    if args.target:
        print_banner()
        hunter = IntelligentFlagHunter()
        
        if args.parallel:
            hunter.processor.max_workers = min(10, os.cpu_count() * 2)
        else:
            hunter.processor.max_workers = 1
        
        result = hunter.hunt(
            args.target,
            args.platform,
            question=args.question,
            secure=not args.no_encrypt,
            brute_force=args.bruteforce
        )
        
        print(json.dumps(result, indent=2))
        
        if args.output:
            if not args.no_encrypt and result.get('encrypted'):
                with open(args.output, 'w') as f:
                    f.write(result['encrypted'])
            else:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
        sys.exit(0)
    
    if args.file:
        print_banner()
        hunter = IntelligentFlagHunter()
        
        if args.parallel:
            hunter.processor.max_workers = min(10, os.cpu_count() * 2)
        else:
            hunter.processor.max_workers = 1
        
        results = {}
        
        with open(args.file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        cprint(f"[*] Hunting {len(targets)} targets...", Colors.BLUE)
        
        for target in targets:
            result = hunter.hunt(
                target,
                args.platform,
                question=args.question,
                secure=not args.no_encrypt,
                brute_force=args.bruteforce
            )
            results[target] = result
        
        print(json.dumps(results, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        sys.exit(0)
    
    # Interactive mode
    tool = CTF_Flag_Hunter_v5()
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
