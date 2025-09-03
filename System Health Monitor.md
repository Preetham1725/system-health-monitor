System Health Monitor

# System Health Monitor

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

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure settings:**
   ```bash
   # Edit config.yaml with your settings
   nano config.yaml
   ```

## ⚙️ Configuration

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

## 🚀 Usage

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
               SYSTEM HEALTH MONITOR 
============================================================
CPU Usage: 45.2% (Load: 1.2) [4 cores, 8 threads]
Memory Usage: 67.8% (10.8GB / 16.0GB)
Disk Usage: 92.1% (184.2GB / 200.0GB)
 Uptime: 5 days, 14 hours
 Active Processes: 234
Network: ⬆️ 1,234,567 bytes sent, ⬇️ 9,876,543 bytes received

  ACTIVE ALERTS (1):
 Disk usage: 92.1% (threshold: 90%) - 184.2GB used
============================================================
```

## Features in Detail

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

## Skill Highlights

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

- [ ] **Web Dashboard**: Real-time monitoring web interface
- [ ] **Database Integration**: Store historical data in SQLite/PostgreSQL
- [ ] **Multiple Notifications**: Slack, Teams, SMS integration
- [ ] **Docker Support**: Containerized deployment
- [ ] **REST API**: External system integration
- [ ] **Prometheus Metrics**: Export metrics for Prometheus/Grafana
- [ ] **Multi-server Monitoring**: Monitor remote systems
- [ ] **Custom Plugins**: Extensible monitoring modules

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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