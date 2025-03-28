#!/usr/bin/env python3
import sys
import psutil
import platform
import os
from colorama import init, Fore, Style


# Initialize colorama for cross-platform colored output
init()


def is_windows():
    return platform.system().lower() == 'windows'


def get_window_info_windows(pid):
    """Get window information for a process on Windows."""
    try:
        import win32gui
        import win32process

        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                if process_id == pid:
                    windows.append(hwnd)
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    except Exception:
        return []


def get_window_info_macos(pid):
    """Get window information for a process on macOS."""
    try:
        import subprocess
        cmd = ['osascript', '-e', f'tell application "System Events" to get windows of process id {pid}']
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return ""


def check_installed_apps_macos():
    """Check for suspicious applications installed in /Applications/ directory."""
    suspicious_apps = []
    suspicious_keywords = [
        'interview',
        'coder',
        'leetcode',
        'hackerrank',
        'codility',
        'coderpad',
        'replit',
        'codepen'
    ]

    try:
        for item in os.listdir('/Applications/'):
            if item.endswith('.app'):
                app_name = item.lower()
                for keyword in suspicious_keywords:
                    if keyword in app_name:
                        suspicious_apps.append(item)
                        break
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not check installed applications: {e}{Style.RESET_ALL}")

    return suspicious_apps


def check_installed_apps_windows():
    """Check for suspicious applications installed on Windows."""
    suspicious_apps = []
    suspicious_keywords = [
        'interview',
        'coder',
        'leetcode',
        'hackerrank',
        'codility',
        'coderpad',
        'replit',
        'codepen'
    ]

    try:
        # Check Program Files directories
        program_files = [
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
            os.environ.get('LocalAppData', os.path.expanduser('~\\AppData\\Local')),
            os.environ.get('AppData', os.path.expanduser('~\\AppData\\Roaming'))
        ]

        exclude_dirs = [
            'Windows',
            'System32',
            'SysWOW64',
            'node_modules',
            'Python',
            'Java',
            'Android',
            'Adobe',
            'Microsoft',
            'Git',
            'PostgreSQL',
            'MySQL'
        ]

        for program_dir in program_files:
            if not os.path.exists(program_dir):
                continue

            for root, dirs, files in os.walk(program_dir):
                if any(exclude in root for exclude in exclude_dirs):
                    continue
                for item in dirs + files:
                    item_lower = item.lower()
                    for keyword in suspicious_keywords:
                        if keyword in item_lower:
                            full_path = os.path.join(root, item)
                            if os.access(full_path, os.X_OK) or item.endswith('.exe') or item.endswith('.msi') or item.endswith('.bat') or item.endswith('.cmd') or item.endswith('.ps1'):
                                suspicious_apps.append(full_path)
                            break
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not check installed applications: {e}{Style.RESET_ALL}")

    return suspicious_apps


def is_suspicious_process(name, cmdline):
    """Check if the process name or command line indicates a coding assistance tool."""
    name = name.lower()
    cmdline = cmdline.lower()


    # Skip our own process and common system processes
    if any(keyword in name for keyword in ['integritychecker', 'python', 'pyinstaller']):
        return False


    # Skip common system processes and development tools
    ignore_keywords = [
        'decoder',
        'encoder',
        'system',
        'helper',
        'service',
        'daemon',
        'vscode',
        'terminal',
        'iterm',
        'chrome',
        'firefox',
        'safari'
    ]

    # First check if it's a process we should ignore
    if any(keyword in name for keyword in ignore_keywords):
        return False

    # Check suspicious keywords in name
    suspicious_keywords = [
        'interview',
        'coder',
        'leetcode',
        'hackerrank',
        'codility',
        'coderpad',
        'replit',
        'codepen'
    ]

    for keyword in suspicious_keywords:
        if keyword in name:
            return True

    # Check suspicious keywords in command line
    for keyword in suspicious_keywords:
        if keyword in cmdline:
            return True

    return False


def check_processes():
    suspicious_processes = []
    current_pid = os.getpid()

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Skip our own process
            if proc.info['pid'] == current_pid:
                continue

            # Get process information
            info = proc.info
            name = info['name']
            cmdline = info['cmdline'] if info['cmdline'] else []
            cmdline_str = ' '.join(cmdline) if cmdline else ''

            # Check if the process name or command line is suspicious
            if is_suspicious_process(name, cmdline_str):
                if is_windows():
                    windows = get_window_info_windows(info['pid'])
                    if not windows:  # No visible windows found
                        suspicious_processes.append(proc)
                else:  # macOS
                    window_info = get_window_info_macos(info['pid'])
                    if not window_info:  # No visible windows found
                        suspicious_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return suspicious_processes


def main():
    suspicious_processes = check_processes()
    suspicious_apps = []

    # Check for suspicious installed applications
    if is_windows():
        suspicious_apps = check_installed_apps_windows()
    else:
        suspicious_apps = check_installed_apps_macos()

    if suspicious_processes or suspicious_apps:
        print(f"{Fore.RED}⚠️  Warning: Potentially hidden interview coding processes or applications detected!{Style.RESET_ALL}")

        if suspicious_processes:
            print("\nSuspicious processes:")
            for proc in suspicious_processes:
                try:
                    cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else 'N/A'
                    print(f"- {proc.info['name']} (PID: {proc.info['pid']})")
                    print(f"  Command: {cmdline}")
                except:
                    continue

        if suspicious_apps:
            print("\nSuspicious installed applications:")
            for app in suspicious_apps:
                print(f"- {app}")

        sys.exit(1)
    else:
        print(f"{Fore.GREEN}✅ No suspicious processes or applications detected.{Style.RESET_ALL}")
        sys.exit(0)


if __name__ == "__main__":
    main()
