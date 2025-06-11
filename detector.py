import time
import re
import os
import subprocess
from collections import defaultdict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Path to the SSH log file
LOG_PATH = "/var/log/auth.log"
ALERT_LOG_FILE = "alerts.log"

# Alert threshold: 3 failed attempts in 10 seconds
THRESHOLD = 3
TIME_WINDOW = 10  # in seconds

# Dictionary to store IP and list of timestamps of failed attempts
ip_attempts = defaultdict(list)

def log_alert(message):
    with open(ALERT_LOG_FILE, "a") as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def alert(ip):
    alert_message = f"[!] ALERT: {ip} exceeded threshold of failed SSH login attempts!"
    print(alert_message)
    log_alert(alert_message)

    # Block IP using iptables
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        block_message = f"[+] Blocked IP: {ip} with iptables"
        print(block_message)
        log_alert(block_message)
    except subprocess.CalledProcessError:
        error_message = f"[!] Failed to block IP: {ip}"
        print(error_message)
        log_alert(error_message)

    # Reset attempts after alert
    ip_attempts[ip] = []

class SSHLogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                lines = f.readlines()[-50:]  # Read last 50 lines to catch recent activity
                for line in lines:
                    print("[DEBUG]", line.strip())

                    # Match "Failed password for [user] from [IP]"
                    match = re.search(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)", line)
                    if match:
                        ip = match.group(1)
                        now = time.time()
                        ip_attempts[ip].append(now)

                        # Keep only timestamps within TIME_WINDOW
                        ip_attempts[ip] = [t for t in ip_attempts[ip] if now - t <= TIME_WINDOW]

                        if len(ip_attempts[ip]) >= THRESHOLD:
                            alert(ip)

if __name__ == "__main__":
    print("[*] Monitoring SSH logs...")
    log_alert("[*] Started monitoring SSH logs")

    event_handler = SSHLogHandler()
    observer = Observer()

    # Monitor the directory containing the log file
    log_dir = os.path.dirname(LOG_PATH)
    observer.schedule(event_handler, path=log_dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log_alert("[*] Stopped monitoring due to keyboard interrupt")
    observer.join()
