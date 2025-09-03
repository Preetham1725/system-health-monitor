# System Health Monitor


### Me: Preetham L

# Monitoring thresholds (percentage)
thresholds:
  cpu: 80        # Alert when CPU usage exceeds 80%
  memory: 85     # Alert when memory usage exceeds 85%
  disk: 90       # Alert when disk usage exceeds 90%

# Check interval in seconds
check_interval: 60

# Email alert configuration
email:
  enabled: false                      # Set to true to enable email alerts
  smtp_server: "smtp.gmail.com"       # SMTP server
  port: 587                           # SMTP port
  from: "system-monitor@yourdomain.com"
  to: "admin@yourdomain.com"
  username: "your-email@gmail.com"    # Your email username
  password: "your-app-password"       # Use app-specific password for Gmail

# Logging configuration
logging:
  level: "INFO"                       # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file: "system_monitor.log"          # Log file name
'''

requirements_txt = System Health Monitor Dependencies
config_yaml = System Health Monitor Configuration

# Core system monitoring library
psutil==5.9.5

# YAML configuration file parsing
PyYAML==6.0.1

# Email libraries (built-in with Python)
# smtplib - built-in
# email - built-in

# Additional useful libraries for enhanced functionality
requests>=2.31.0          # For HTTP requests (future web hooks)
colorama>=0.4.6           # For colored console output
tabulate>=0.9.0           # For formatted table output

# Development and testing dependencies (optional)
pytest>=7.4.0             # For unit testing
pytest-cov>=4.1.0         # For test coverage
flake8>=6.0.0             # For code linting
black>=23.7.0             # For code formatting
'''

setup_script = '''#!/bin/bash
# System Health Monitor Setup Script

echo "Setting up System Health Monitor..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv monitor_env
source monitor_env/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Create sample configuration if it doesn't exist
if [ ! -f "config.yaml" ]; then
    echo "Creating sample configuration file..."
    cp config.yaml config_sample.yaml
    echo "Please edit config.yaml with your email settings before running the monitor."
fi

# Make monitor.py executable

chmod +x monitor.py

echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config.yaml with your email settings"
echo "2. Test the monitor: python monitor.py --once"
echo "3. Start monitoring: python monitor.py"
echo ""
echo "For help: python monitor.py --help"
'''
readme_content = System Health Monitor

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## Overview

A comprehensive Python-based system health monitoring tool designed for IT support engineers and system administrators. This tool provides real-time monitoring of system resources with configurable thresholds and automated email alerting capabilities.

### Key Features

- **Real-time System Monitoring**: CPU, Memory, Disk, Network, and Process monitoring
- **Configurable Thresholds**: YAML-based configuration for easy customization
- **Email Alert System**: Automated email notifications when thresholds are exceeded
- **Comprehensive Statistics**: Detailed system information including uptime and load averages
- **JSON Export**: Save monitoring data to JSON files for analysis
- **Continuous & One-time Monitoring**: Flexible monitoring modes
- **Rich Console Output**: Color-coded status indicators and formatted display
- **Logging Support**: Comprehensive logging with configurable levels
- **Cross-platform**: Works on Linux, Windows, and macOS

## Technologies Used

- **Python 3.7+**: Core programming language
- **psutil**: System and process utilities for cross-platform monitoring
- **PyYAML**: Configuration file parsing
- **smtplib**: Email notification system
- **logging**: Built-in logging framework
- **argparse**: Command-line interface

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Email account for alerts (Gmail recommended)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Preetham1725/system-health-monitor.git
   cd system-health-monitor
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Or install manually:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yaml` to customize monitoring parameters:

```yaml
# Monitoring thresholds (percentage)
thresholds:
  cpu: 80        # Alert when CPU usage exceeds 80%
  memory: 85     # Alert when memory usage exceeds 85%
  disk: 90       # Alert when disk usage exceeds 90%

# Check interval in seconds
check_interval: 60

# Email alert configuration
email:
  enabled: true
  smtp_server: "smtp.gmail.com"
  from: "monitor@yourdomain.com"
  to: "admin@yourdomain.com"
  username: "your-email@gmail.com"
  password: "your-app-password"
```

## Usage

### Basic Commands

```bash
# Run continuous monitoring
python monitor.py

# Run with custom configuration
python monitor.py -c custom_config.yaml

# Run once and exit
python monitor.py --once

# Save statistics to JSON
python monitor.py --json system_stats.json

# Show help
python monitor.py --help
```

### Example Output

```
============================================================
  SYSTEM HEALTH MONITOR - 2025-09-02 17:54:23
============================================================
CPU Usage: 45.2% (Load: 1.2) [4 cores, 8 threads]
Memory Usage: 67.8% (10.8GB / 16.0GB)
Disk Usage: 92.1% (184.2GB / 200.0GB)
Uptime: 5 days, 14 hours
Active Processes: 234
Network: ⬆1,234,567 bytes sent, ⬇9,876,543 bytes received

  ACTIVE ALERTS (1):
    Disk usage: 92.1% (threshold: 90%) - 184.2GB used
============================================================
```

##  Features in Detail

### System Monitoring
- **CPU**: Usage percentage, load average, core count
- **Memory**: Usage percentage, total/used/available in GB
- **Disk**: Usage percentage, total/used/free space in GB
- **Network**: Bytes and packets sent/received
- **System**: Uptime, process count, boot time

### Alert System
- **Threshold-based Alerts**: Configurable CPU, memory, and disk thresholds
- **Email Notifications**: Detailed alert emails with system status
- **Smart Alerting**: Prevents email spam with single alert per session
- **Rich Formatting**: Color-coded console output with emojis

### Data Export
- **JSON Export**: Save monitoring data for analysis
- **Logging**: Comprehensive logs with configurable levels
- **Timestamped Data**: All data includes precise timestamps

##  Skill Highlights

This project demonstrates proficiency in:

- **System Administration**: Resource monitoring, threshold management, system diagnostics
- **Python Programming**: Object-oriented design, error handling, type hints, documentation
- **Configuration Management**: YAML-based configuration, environment setup
- **Email Integration**: SMTP protocol, email formatting, authentication
- **Cross-platform Development**: Compatible across operating systems
- **Command-line Interfaces**: Argument parsing, user-friendly CLI design
- **Logging & Monitoring**: Professional logging practices, alert systems
- **Documentation**: Comprehensive README, inline code documentation
- **Best Practices**: Clean code structure, modular design, error handling

##  Future Enhancements

-  **Web Dashboard**: Real-time monitoring web interface
-  **Database Integration**: Store historical data in SQLite/PostgreSQL
-  **Multiple Notifications**: Slack, Teams, SMS integration
-  **Docker Support**: Containerized deployment
-  **REST API**: External system integration
-  **Prometheus Metrics**: Export metrics for Prometheus/Grafana
-  **Multi-server Monitoring**: Monitor remote systems
-  **Custom Plugins**: Extensible monitoring modules
-  **Mobile App**: iOS/Android monitoring app
-  **Machine Learning**: Predictive alerting based on trends

## Testing

Run tests with pytest:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=monitor --cov-report=html
```

##  Project Structure

```
system-health-monitor/
├── monitor.py              # Main monitoring script
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── setup.sh               # Setup script
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── tests/                # Test files
│   ├── __init__.py
│   └── test_monitor.py
└── docs/                 # Documentation
    ├── installation.md
    └── configuration.md
```

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## Me

**Preetham L**
- Position: DA II @ Amazon
- Location: Bangalore, India
- GitHub: [@Preetham1725](https://github.com/Preetham1725)
- LinkedIn: [preetham-l-820bb8170](https://linkedin.com/in/preetham-l-820bb8170)

## Acknowledgments

- Built for IT support engineers and system administrators
- Inspired by real-world production monitoring needs
- Thanks to the Python community for excellent libraries like `psutil`

---

**If you found this project helpful, please give it a star!**
**Have questions or suggestions?** Open an issue or start a discussion!
'''

print("=== Configuration File (config.yaml) ===")
print(config_yaml)
print("\n" + "="*60)
print("=== Requirements File (requirements.txt) ===")
print(requirements_txt)
print("\n" + "="*60)
print("=== Setup Script (setup.sh) ===")  
print(setup_script)
print("\n" + "="*60)
print("=== Complete README.md ===")
print(readme_content[:2000] + "... [README continues for full documentation]")
