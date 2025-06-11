# SSH Brute Force Detector

A Python-based real-time SSH brute-force attack detector and blocker. It monitors `/var/log/auth.log` for failed SSH login attempts, triggers alerts if a threshold is exceeded, and automatically blocks the attacker's IP using `iptables`.

## Features

- Real-time monitoring of SSH logs
- Configurable threshold and time window
- IP blocking via `iptables`
- Logs alerts to a local file (`alerts.log`)
- Easy to customize and extend

## Requirements

- Ubuntu/Debian-based system
- Python 3.6+
- `watchdog` library
- `iptables` installed and enabled

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ssh-brute-force-detector.git
cd ssh-brute-force-detector

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install watchdog
```

> **Note**: If you see a message about an "externally managed environment", always use a virtual environment to install Python packages.

## Running the Detector

```bash
sudo venv/bin/python detector.py
```

The script will continuously monitor `/var/log/auth.log` for failed SSH login attempts and display debug messages. Once an IP exceeds the set threshold, it will be:

- Printed on the terminal
- Logged in `alerts.log`
- Blocked using `iptables`

## Configuration

You can customize the following variables in `detector.py`:

```python
THRESHOLD = 3         # Number of failed attempts before triggering an alert
TIME_WINDOW = 10      # Time window in seconds to observe repeated attempts
LOG_PATH = "/var/log/auth.log"  # Path to the SSH log file
```

## Sample Output

```bash
[*] Monitoring SSH logs...
[DEBUG] Failed password for invalid user hacker from 192.168.0.101 port 60234 ssh2
[!] ALERT: 192.168.0.101 exceeded threshold of failed SSH login attempts!
[+] Blocked IP: 192.168.0.101 with iptables
```

## Disclaimer

This script modifies firewall rules using `iptables`. Be careful not to block legitimate IPs. Always test in a safe environment before deploying to production.

## License

MIT License

---

**Author:** Aina Andrian  
**GitHub:** [yourusername](https://github.com/yourusername)
