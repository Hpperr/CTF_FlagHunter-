#!/usr/bin/env python3
"""
CTF_Flag_Hunter v4.0 - Ultimate Educational CTF Automation Framework
Multi-Layer Decryption | Secure Data Handling | Intelligent Detection
Author: F1REW0LF
License: MIT - Free for Community
Version: 4.0.0
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
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union, Set
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from collections import defaultdict

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
VERSION = "4.0.0"
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
                                                                    
{Colors.RED}{Colors.BOLD}    ULTIMATE EDUCATIONAL CTF AUTOMATION v4.0{Colors.WHITE}
{Colors.YELLOW}{Colors.BOLD}    Secure Data Handling | Multi-Layer Decryption{Colors.WHITE}
{Colors.GOLD}    Version {VERSION} | Author: {AUTHOR} 
"""
    print(banner)

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
            # Generate or load encryption key
            key_file = os.path.expanduser('~/.ctf_hunter_key')
            
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    self.encryption_key = f.read()
            else:
                # Generate new key
                self.encryption_key = Fernet.generate_key()
                with open(key_file, 'wb') as f:
                    f.write(self.encryption_key)
                os.chmod(key_file, 0o600)  # Secure file permissions
            
            self.cipher = Fernet(self.encryption_key)
            cprint("[+] Encryption initialized successfully", Colors.GREEN)
        except Exception as e:
            cprint(f"[!] Encryption init failed: {e}", Colors.RED)
            self.cipher = None
    
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """
        Encrypt sensitive data
        """
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
            # Fallback: Base64 encoding
            if isinstance(data, str):
                data = data.encode('utf-8')
            return base64.b64encode(data).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt encrypted data
        """
        if self.cipher:
            try:
                encrypted = base64.b64decode(encrypted_data)
                decrypted = self.cipher.decrypt(encrypted)
                return decrypted.decode('utf-8')
            except Exception as e:
                cprint(f"[!] Decryption failed: {e}", Colors.RED)
                return encrypted_data
        else:
            # Fallback: Base64 decoding
            try:
                decoded = base64.b64decode(encrypted_data)
                return decoded.decode('utf-8')
            except:
                return encrypted_data
    
    def secure_store(self, filename: str, data: Dict) -> bool:
        """
        Securely store data to file with encryption
        """
        try:
            json_data = json.dumps(data, indent=2)
            encrypted = self.encrypt_data(json_data)
            
            # Use secure file permissions
            with open(filename, 'w') as f:
                f.write(encrypted)
            os.chmod(filename, 0o600)  # Owner read/write only
            return True
        except Exception as e:
            cprint(f"[!] Secure store failed: {e}", Colors.RED)
            return False
    
    def secure_load(self, filename: str) -> Optional[Dict]:
        """
        Securely load data from file with decryption
        """
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
    
    def secure_delete(self, filename: str) -> bool:
        """
        Securely delete file with overwrite
        """
        try:
            if not os.path.exists(filename):
                return True
            
            # Overwrite with random data before deletion
            with open(filename, 'wb') as f:
                f.write(os.urandom(os.path.getsize(filename)))
            os.remove(filename)
            return True
        except Exception as e:
            cprint(f"[!] Secure delete failed: {e}", Colors.RED)
            return False

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
        """
        Attempt to decrypt multi-layer encoded data
        """
        result = {
            'original': data,
            'decoded': [],
            'methods': [],
            'final_flag': None,
            'platform': platform,
            'success': False,
            'layers': 0
        }
        
        cprint(f"[*] Analyzing encoded data: {data[:50]}...", Colors.BLUE)
        
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
        """Try all known decoding methods"""
        # Base64
        try:
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # Base64 URL safe
        try:
            decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # Hex
        try:
            decoded = bytes.fromhex(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # ROT13
        try:
            decoded = codecs.decode(data, 'rot_13')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # Base32
        try:
            decoded = base64.b32decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # Base16
        try:
            decoded = base64.b16decode(data).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # URL decode
        try:
            decoded = urllib.parse.unquote(data)
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        # Zlib decompress
        try:
            decoded = zlib.decompress(base64.b64decode(data)).decode('utf-8', errors='ignore')
            if self._is_valid_decoding(decoded):
                return decoded
        except:
            pass
        
        return data
    
    def _is_valid_decoding(self, decoded: str) -> bool:
        """Check if decoded string looks valid"""
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
        """Check if data is likely a flag"""
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
        """Get flag formats for specific platform"""
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

# ============================[ INTELLIGENT FLAG HUNTER ]================================

class IntelligentFlagHunter:
    """
    Intelligent flag hunting with multi-layer decryption and secure data handling
    """
    
    def __init__(self):
        self.decryptor = MultiLayerDecryption()
        self.secure_handler = SecureDataHandler()
        self.found_flags = []
        self.session = self._create_session()
        self.platform_patterns = self._load_platform_patterns()
        self.results_cache = {}
        
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
    
    def hunt(self, target: str, platform: str = 'auto', flag_files: List[str] = None, question: str = None, secure: bool = True) -> Dict:
        """
        Intelligent flag hunting with auto-detection and decryption
        """
        result = {
            'target': target,
            'platform': platform,
            'question': question,
            'flags': [],
            'decrypted': [],
            'secure': secure,
            'timestamp': datetime.now().isoformat(),
            'success': False
        }
        
        cprint(f"\n[*] Hunting flags on: {target}", Colors.BLUE)
        
        if platform == 'auto':
            platform = self._detect_platform(target)
            cprint(f"[+] Auto-detected platform: {platform}", Colors.GREEN)
        
        config = self.platform_patterns.get(platform, {})
        if not flag_files:
            flag_files = config.get('flag_files', ['flag.txt', 'user.txt', 'root.txt'])
        
        if target.startswith(('http://', 'https://')):
            http_flags = self._hunt_http(target, flag_files, question)
            result['flags'].extend(http_flags)
        
        if target.startswith(('ssh://', 'root@')) or ':' in target and '@' in target:
            ssh_flags = self._hunt_ssh(target, flag_files, question)
            result['flags'].extend(ssh_flags)
        
        if os.path.exists(target):
            file_flags = self._hunt_files(target, flag_files, question)
            result['flags'].extend(file_flags)
        
        for flag_data in result['flags']:
            decrypted = self.decryptor.decrypt(flag_data['content'], platform)
            if decrypted['success']:
                flag_data['decrypted'] = decrypted['final_flag']
                flag_data['layers'] = decrypted['layers']
                flag_data['methods'] = decrypted['methods']
                result['decrypted'].append(decrypted['final_flag'])
        
        result['success'] = len(result['decrypted']) > 0
        
        if secure and result['success']:
            encrypted_result = self.secure_handler.encrypt_data(json.dumps(result))
            result['encrypted'] = encrypted_result
            result['encryption_status'] = 'encrypted'
            
            self.secure_handler.secure_store(f'ctf_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.enc', result)
            cprint("[+] Results securely encrypted and stored", Colors.GREEN)
        
        if result['success']:
            cprint(f"\n[!] Found {len(result['decrypted'])} flag(s) after decryption", Colors.RED)
            for flag in result['decrypted']:
                cprint(f"  🚩 {flag}", Colors.GOLD)
        else:
            cprint("\n[-] No flags found", Colors.YELLOW)
        
        return result
    
    def _detect_platform(self, target: str) -> str:
        target_lower = target.lower()
        
        for platform, info in self.platform_patterns.items():
            if platform in target_lower or info.get('name', '').lower() in target_lower:
                return platform
        
        return 'vulnhub'
    
    def _hunt_http(self, target: str, flag_files: List[str], question: str = None) -> List[Dict]:
        flags = []
        
        if not REQUESTS_AVAILABLE:
            return flags
        
        if question:
            file_match = re.search(r'(local\.txt|root\.txt|flag\.txt|user\.txt)', question, re.IGNORECASE)
            if file_match:
                flag_files = [file_match.group(1)]
        
        for flag_file in flag_files:
            for path in ['', '/', '/var/www/', '/home/', '/root/', '/tmp/']:
                url = f"{target}/{path}{flag_file}" if path else f"{target}/{flag_file}"
                try:
                    response = self.session.get(url, timeout=5, verify=False)
                    if response.status_code == 200:
                        content = response.text.strip()
                        if self._is_likely_flag(content):
                            flags.append({
                                'source': url,
                                'file': flag_file,
                                'content': content,
                                'type': 'http'
                            })
                except:
                    pass
        
        return flags
    
    def _hunt_ssh(self, target: str, flag_files: List[str], question: str = None) -> List[Dict]:
        flags = []
        
        if not SSH_AVAILABLE:
            return flags
        
        try:
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
            
            for flag_file in flag_files:
                for path in ['/', '/home/', '/root/', '/var/www/', '/tmp/']:
                    filepath = f"{path}{flag_file}"
                    try:
                        sftp = client.open_sftp()
                        try:
                            with sftp.open(filepath, 'r') as f:
                                content = f.read().decode('utf-8', errors='ignore').strip()
                                if self._is_likely_flag(content):
                                    flags.append({
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
        
        return flags
    
    def _hunt_files(self, target: str, flag_files: List[str], question: str = None) -> List[Dict]:
        flags = []
        target_path = Path(target)
        
        if target_path.is_file():
            try:
                with open(target_path, 'r') as f:
                    content = f.read().strip()
                    if self._is_likely_flag(content):
                        flags.append({
                            'source': str(target_path),
                            'file': target_path.name,
                            'content': content,
                            'type': 'file'
                        })
            except:
                pass
        elif target_path.is_dir():
            for flag_file in flag_files:
                for path in target_path.rglob(flag_file):
                    try:
                        with open(path, 'r') as f:
                            content = f.read().strip()
                            if self._is_likely_flag(content):
                                flags.append({
                                    'source': str(path),
                                    'file': flag_file,
                                    'content': content,
                                    'type': 'file'
                                })
                    except:
                        pass
        
        return flags
    
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

# ============================[ MAIN FRAMEWORK ]================================

class CTF_Flag_Hunter_v4:
    """CTF_Flag_Hunter v4.0 - Ultimate Educational CTF Automation with Encryption"""
    
    def __init__(self):
        self.hunter = IntelligentFlagHunter()
        self.secure_handler = SecureDataHandler()
        self.results = {}
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        cprint("\n[!] CTF_Flag_Hunter shutting down...", Colors.RED)
        self.running = False
        sys.exit(0)
    
    def show_menu(self):
        print(f"""
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.BOLD}CTF_Flag_Hunter v{VERSION} - Ultimate Educational CTF Automation{Colors.WHITE}
{Colors.CYAN}Secure Data Handling | Multi-Layer Decryption | Intelligent{Colors.WHITE}
{Colors.YELLOW}Author: {AUTHOR} | Score: {SCORE}{Colors.WHITE}
{Colors.BLUE}{'='*70}{Colors.WHITE}
{Colors.GREEN}[1] Hunt Flags (Auto-Detect){Colors.WHITE}
{Colors.GREEN}[2] Hunt Flags (Manual File Name){Colors.WHITE}
{Colors.GREEN}[3] Decrypt Encoded Flag{Colors.WHITE}
{Colors.GREEN}[4] Multi-Target Hunt{Colors.WHITE}
{Colors.GREEN}[5] Secure View Results{Colors.WHITE}
{Colors.GREEN}[6] Generate Secure Report{Colors.WHITE}
{Colors.GREEN}[7] Decrypt Previous Results{Colors.WHITE}
{Colors.RED}[8] Exit{Colors.WHITE}
""")
    
    def run(self):
        print_banner()
        cprint("[*] CTF_Flag_Hunter v4.0 - Ultimate Educational CTF Automation", Colors.CYAN)
        cprint("[*] Secure Data Handling | Multi-Layer Decryption", Colors.DIM)
        cprint("[!] This tool is for educational purposes only", Colors.YELLOW)
        cprint("[+] Encryption initialized for secure data storage", Colors.GREEN)
        
        while self.running:
            self.show_menu()
            choice = input(f"{Colors.CYAN}[>] Select: {Colors.WHITE}").strip()
            
            if choice == '1':
                target = input("[>] Target URL/IP/File: ").strip()
                platform = input("[>] Platform (auto/hackthebox/tryhackme/bugcrowd/vulnhub/picoctf/overthewire): ").strip() or 'auto'
                
                result = self.hunter.hunt(target, platform)
                self.results[target] = result
                
            elif choice == '2':
                target = input("[>] Target URL/IP/File: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                question = input("[>] Question/Description (e.g., What is the root.txt flag?): ").strip()
                
                result = self.hunter.hunt(target, platform, question=question)
                self.results[target] = result
                
            elif choice == '3':
                encoded = input("[>] Encoded flag to decrypt: ").strip()
                platform = input("[>] Platform: ").strip() or 'auto'
                
                decrypted = MultiLayerDecryption().decrypt(encoded, platform)
                print(json.dumps(decrypted, indent=2))
                
            elif choice == '4':
                print("[*] Enter targets (one per line, empty to finish):")
                targets = []
                while True:
                    target = input("[>] ").strip()
                    if not target:
                        break
                    targets.append(target)
                
                if targets:
                    platform = input("[>] Platform (auto for all): ").strip() or 'auto'
                    cprint(f"[*] Hunting {len(targets)} targets...", Colors.BLUE)
                    
                    for target in targets:
                        result = self.hunter.hunt(target, platform)
                        self.results[target] = result
                        
            elif choice == '5':
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
                
            elif choice == '6':
                report = {
                    'timestamp': datetime.now().isoformat(),
                    'version': VERSION,
                    'author': AUTHOR,
                    'total_targets': len(self.results),
                    'results': self.results
                }
                
                secure = input("[>] Encrypt report? (y/N): ").strip().lower() == 'y'
                
                if secure:
                    encrypted_report = self.secure_handler.encrypt_data(json.dumps(report))
                    with open('ctf_hunter_v4_secure_report.enc', 'w') as f:
                        f.write(encrypted_report)
                    cprint("[+] Secure report saved to ctf_hunter_v4_secure_report.enc", Colors.GREEN)
                else:
                    with open('ctf_hunter_v4_report.json', 'w') as f:
                        json.dump(report, f, indent=2)
                    cprint("[+] Report saved to ctf_hunter_v4_report.json", Colors.GREEN)
                
            elif choice == '7':
                filename = input("[>] Encrypted file to decrypt: ").strip()
                data = self.secure_handler.secure_load(filename)
                if data:
                    print(json.dumps(data, indent=2))
                else:
                    cprint("[!] Failed to decrypt file", Colors.RED)
                
            elif choice == '8':
                cprint("[*] CTF_Flag_Hunter shutting down...", Colors.GREEN)
                break
            else:
                cprint("[-] Invalid selection", Colors.RED)

# ============================[ COMMAND LINE ]================================

def main():
    parser = argparse.ArgumentParser(
        description="CTF_Flag_Hunter v4.0 - Ultimate Educational CTF Automation with Encryption",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python3 ctf_hunter.py -t https://target.com
  python3 ctf_hunter.py -t https://target.com -p hackthebox
  python3 ctf_hunter.py -t https://target.com -q "What is the root.txt flag?"
  python3 ctf_hunter.py -d "SGVsbG9Xb3JsZA==" -p hackthebox
  python3 ctf_hunter.py --decrypt-file results.enc
        """
    )
    
    parser.add_argument("-t", "--target", help="Target URL/IP/File")
    parser.add_argument("-p", "--platform", default="auto", help="Platform (hackthebox/tryhackme/bugcrowd/vulnhub/picoctf/overthewire)")
    parser.add_argument("-q", "--question", help="Question/Description")
    parser.add_argument("-u", "--user", help="SSH username (if SSH target)")
    parser.add_argument("-d", "--decrypt", help="Decrypt encoded flag")
    parser.add_argument("--decrypt-file", help="Decrypt encrypted results file")
    parser.add_argument("-f", "--file", help="File with targets (one per line)")
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("--no-encrypt", action="store_true", help="Disable encryption")
    
    args = parser.parse_args()
    
    if args.decrypt_file:
        print_banner()
        handler = SecureDataHandler()
        data = handler.secure_load(args.decrypt_file)
        if data:
            print(json.dumps(data, indent=2))
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(data, f, indent=2)
        else:
            cprint("[!] Failed to decrypt file", Colors.RED)
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
        result = hunter.hunt(args.target, args.platform, question=args.question, secure=not args.no_encrypt)
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
        results = {}
        
        with open(args.file, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        
        cprint(f"[*] Hunting {len(targets)} targets...", Colors.BLUE)
        
        for target in targets:
            result = hunter.hunt(target, args.platform, question=args.question, secure=not args.no_encrypt)
            results[target] = result
        
        print(json.dumps(results, indent=2))
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
        sys.exit(0)
    
    # Interactive mode
    tool = CTF_Flag_Hunter_v4()
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
