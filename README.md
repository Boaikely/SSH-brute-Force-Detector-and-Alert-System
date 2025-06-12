# SSH Brute Force Detector

A Python-based real-time SSH brute-force attack detector and blocker. It monitors `/var/log/auth.log` for failed SSH login attempts, triggers alerts if a threshold is exceeded, and automatically blocks the attacker's IP using `iptables`.

## Features

- Real-time monitoring of SSH logs
- Configurable threshold and time window
- IP blocking via `iptables`
- Logs alerts to a local file (`alerts.log`)
- Optional email alerts (configure SMTP settings in 'detector.py')
- Easy to customize and extend

## Requirements

- Ubuntu/Debian-based system
- Python 3.6+
- `watchdog` library
- `iptables` installed and enabled
- (Optional) SMTP server for email alerts

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
- (Optional) Sent as an email alert if configured

## Configuration

You can customize the following variables in `detector.py`:

```python
THRESHOLD = 3         # Number of failed attempts before triggering an alert
TIME_WINDOW = 100      # Time window in seconds to observe repeated attempts
LOG_PATH = "/var/log/auth.log"  # Path to the SSH log file
```
## Email alert setting (disabled by default)

EMAIL_ALERTS_ENABLED = False
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
EMAIL_USERNAME = "your_email@example.com"
EMAIL_PASSWORD = "your_password"
EMAIL_FROM = "your_email@example.com"
EMAIL_TO = "admin@example.com"

## Sample Output

```bash
[*] Monitoring SSH logs...
[DEBUG] Failed password for invalid user hacker from 127.0.0.1 port 44934 ssh2
[!] ALERT: 127.0.0.1 exceeded threshold of failed SSH login attempts!
[+] Blocked IP: 127.0.0.1 with iptables
[+] Email alert sent for 127.0.0.1

```

## Disclaimer

This script modifies firewall rules using `iptables`. Be careful not to block legitimate IPs. Always test in a safe environment before deploying to production.

## License

MIT License

---

**Author:** Aina Andrian  
**GitHub:** [Boaikely](https://github.com/Boaikely)
