#!/usr/bin/env python3
"""
System Health Monitor
Me: Preetham L
Description: Monitors CPU, memory, disk usage and sends alerts when thresholds are exceeded.
Designed for IT Support Engineers and System Administrators.
"""

import psutil
import smtplib
import yaml
import time
import json
import logging
import argparse
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional

class SystemMonitor:
    """
    A comprehensive system health monitoring tool.
    
    Features:
    - CPU, Memory, Disk monitoring
    - Configurable thresholds
    - Email alerts
    - Logging
    - JSON output support
    """
    
    def __init__(self, config_file: str = 'config.yaml'):
        """
        Initialize the system monitor with configuration.
        
        Args:
            config_file (str): Path to the configuration file
        """
        self.config_file = config_file
        self.config = self._load_config()
        self._setup_logging()
        self.alert_sent = False  # Prevent spam emails
        
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default settings.")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if config file is not available."""
        return {
            'thresholds': {
                'cpu': 80,
                'memory': 85,
                'disk': 90
            },
            'check_interval': 60,
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'port': 587,
                'from': 'monitoring@example.com',
                'to': 'admin@example.com',
                'username': '',
                'password': ''
            },
            'logging': {
                'level': 'INFO',
                'file': 'system_monitor.log'
            }
        }
    # logging in...
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = getattr(logging, self.config['logging']['level'].upper())
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config['logging']['file']),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_system_stats(self) -> Dict:
        """
        Collect comprehensive system statistics.
        
        Returns:
            Dict: System statistics including CPU, memory, disk, and network
        """
        try:
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count_logical = psutil.cpu_count()
            cpu_count_physical = psutil.cpu_count(logical=False)
            
            # Memory Information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_total_gb = round(memory.total / (1024**3), 2)
            memory_used_gb = round(memory.used / (1024**3), 2)
            memory_available_gb = round(memory.available / (1024**3), 2)
            
            # Disk Information
            disk = psutil.disk_usage('/')
            disk_percent = round((disk.used / disk.total) * 100, 2)
            disk_total_gb = round(disk.total / (1024**3), 2)
            disk_used_gb = round(disk.used / (1024**3), 2)
            disk_free_gb = round(disk.free / (1024**3), 2)
            
            # Load Average (Unix-like systems)
            try:
                load_avg = psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            except (OSError, AttributeError):
                load_avg = 0
            
            # Network Information
            network = psutil.net_io_counters()
            
            # System Uptime
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            # Process Count
            process_count = len(psutil.pids())
            
            stats = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'cpu': {
                    'percent': cpu_percent,
                    'count_logical': cpu_count_logical,
                    'count_physical': cpu_count_physical,
                    'load_avg': round(load_avg, 2)
                },
                'memory': {
                    'percent': memory_percent,
                    'total_gb': memory_total_gb,
                    'used_gb': memory_used_gb,
                    'available_gb': memory_available_gb
                },
                'disk': {
                    'percent': disk_percent,
                    'total_gb': disk_total_gb,
                    'used_gb': disk_used_gb,
                    'free_gb': disk_free_gb
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'system': {
                    'uptime_days': uptime.days,
                    'uptime_hours': uptime.seconds // 3600,
                    'process_count': process_count,
                    'boot_time': boot_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error collecting system stats: {e}")
            return {}
    
    def check_thresholds(self, stats: Dict) -> List[str]:
        """
        Check if any metrics exceed configured thresholds.
        
        Args:
            stats (Dict): System statistics
            
        Returns:
            List[str]: List of alert messages
        """
        alerts = []
        thresholds = self.config['thresholds']
        
        # Check CPU threshold
        if stats['cpu']['percent'] > thresholds['cpu']:
            alerts.append(
                f"CPU usage: {stats['cpu']['percent']:.1f}% "
                f"(threshold: {thresholds['cpu']}%)"
            )
        
        # Check Memory threshold
        if stats['memory']['percent'] > thresholds['memory']:
            alerts.append(
                f"Memory usage: {stats['memory']['percent']:.1f}% "
                f"(threshold: {thresholds['memory']}%) - "
                f"{stats['memory']['used_gb']:.1f}GB used"
            )
        
        # Check Disk threshold
        if stats['disk']['percent'] > thresholds['disk']:
            alerts.append(
                f"Disk usage: {stats['disk']['percent']:.1f}% "
                f"(threshold: {thresholds['disk']}%) - "
                f"{stats['disk']['used_gb']:.1f}GB used"
            )
        
        return alerts
    
    def send_alert(self, alerts: List[str], stats: Dict):
        """
        Send email alert for threshold violations.
        
        Args:
            alerts (List[str]): List of alert messages
            stats (Dict): Current system statistics
        """
        if not alerts or not self.config['email']['enabled']:
            return
        
        # Prevent spam - only send one alert per monitoring session
        if self.alert_sent:
            return
        
        try:
            smtp_config = self.config['email']
            
            msg = MIMEMultipart()
            msg['From'] = smtp_config['from']
            msg['To'] = smtp_config['to']
            msg['Subject'] = f"System Health Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Create detailed email body
            body = f"""
System Health Alert - Threshold Exceeded

Time: {stats['timestamp']}
System Uptime: {stats['system']['uptime_days']} days, {stats['system']['uptime_hours']} hours

ALERTS:
"""
            for alert in alerts:
                body += f"  • {alert}\n"
            
            body += f"""

CURRENT SYSTEM STATUS:
  CPU Usage: {stats['cpu']['percent']:.1f}% (Load: {stats['cpu']['load_avg']})
  Memory Usage: {stats['memory']['percent']:.1f}% ({stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB)
  Disk Usage: {stats['disk']['percent']:.1f}% ({stats['disk']['used_gb']:.1f}GB / {stats['disk']['total_gb']:.1f}GB)
  Active Processes: {stats['system']['process_count']}

Please investigate and take necessary action.

---
System Health Monitor
Generated automatically
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['port'])
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info("Alert email sent successfully")
            self.alert_sent = True
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def display_stats(self, stats: Dict, alerts: List[str]):
        """
        Display formatted system statistics to console.
        
        Args:
            stats (Dict): System statistics
            alerts (List[str]): Current alerts
        """
        print(f"\n{'='*60}")
        print(f"🖥️  SYSTEM HEALTH MONITOR - {stats['timestamp']}")
        print(f"{'='*60}")
        
        # CPU Information
        cpu_status = "RED" if stats['cpu']['percent'] > self.config['thresholds']['cpu'] else "🟢"
        print(f"{cpu_status} CPU Usage: {stats['cpu']['percent']:.1f}% "
              f"(Load: {stats['cpu']['load_avg']}) "
              f"[{stats['cpu']['count_physical']} cores, {stats['cpu']['count_logical']} threads]")
        
        # Memory Information
        memory_status = "RED" if stats['memory']['percent'] > self.config['thresholds']['memory'] else "🟢"
        print(f"{memory_status} Memory Usage: {stats['memory']['percent']:.1f}% "
              f"({stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB)")
        
        # Disk Information
        disk_status = "RED" if stats['disk']['percent'] > self.config['thresholds']['disk'] else "🟢"
        print(f"{disk_status} Disk Usage: {stats['disk']['percent']:.1f}% "
              f"({stats['disk']['used_gb']:.1f}GB / {stats['disk']['total_gb']:.1f}GB)")
        
        # System Information
        print(f"Uptime: {stats['system']['uptime_days']} days, {stats['system']['uptime_hours']} hours")
        print(f"Active Processes: {stats['system']['process_count']}")
        
        # Network Information
        print(f"Network: ⬆{stats['network']['bytes_sent']:,} bytes sent, "
              f"⬇{stats['network']['bytes_recv']:,} bytes received")
        
        # Alerts
        if alerts:
            print(f"\n  ACTIVE ALERTS ({len(alerts)}):")
            for alert in alerts:
                print(f"   {alert}")
        else:
            print(f"\n All systems normal - no alerts")
        
        print(f"{'='*60}")
    
    def save_stats_json(self, stats: Dict, filename: str = None):
        """
        Save statistics to JSON file.
        
        Args:
            stats (Dict): System statistics
            filename (str): Output filename (optional)
        """
        if not filename:
            filename = f"system_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(stats, f, indent=2)
            self.logger.info(f"Statistics saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save statistics: {e}")
    
    def run_once(self) -> Dict:
        """
        Run monitoring once and return statistics.
        
        Returns:
            Dict: System statistics
        """
        stats = self.get_system_stats()
        if not stats:
            return {}
        
        alerts = self.check_thresholds(stats)
        self.display_stats(stats, alerts)
        
        if alerts:
            self.logger.warning(f"System alerts triggered: {len(alerts)} threshold(s) exceeded")
            self.send_alert(alerts, stats)
        
        return stats
    
    def run_monitoring(self):
        """Main continuous monitoring loop."""
        self.logger.info("Starting system health monitoring...")
        self.logger.info(f"Monitoring interval: {self.config['check_interval']} seconds")
        self.logger.info(f"Thresholds - CPU: {self.config['thresholds']['cpu']}%, "
                        f"Memory: {self.config['thresholds']['memory']}%, "
                        f"Disk: {self.config['thresholds']['disk']}%")
        
        try:
            while True:
                stats = self.run_once()
                
                if stats:
                    # Log basic stats
                    self.logger.info(
                        f"CPU: {stats['cpu']['percent']:.1f}% | "
                        f"Memory: {stats['memory']['percent']:.1f}% | "
                        f"Disk: {stats['disk']['percent']:.1f}%"
                    )
                
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user.")
            print("\n System monitoring stopped.")
        except Exception as e:
            self.logger.error(f"Monitoring error: {e}")
            raise


def main():
    """Main function with command line argument parsing."""
    parser = argparse.ArgumentParser(
        description="System Health Monitor - Monitor CPU, Memory, and Disk usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py                    # Run with default config
  python monitor.py -c custom.yaml     # Use custom config
  python monitor.py --once             # Run once and exit
  python monitor.py --json output.json # Save stats to JSON
        """
    )
    
    parser.add_argument(
        '-c', '--config',
        default='config.yaml',
        help='Configuration file path (default: config.yaml)'
    )
    
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run monitoring once and exit'
    )
    
    parser.add_argument(
        '--json',
        help='Save statistics to JSON file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='System Health Monitor v1.0.0'
    )
    
    args = parser.parse_args()
    
    try:
        monitor = SystemMonitor(args.config)
        
        if args.once:
            # Run once and exit
            stats = monitor.run_once()
            if args.json and stats:
                monitor.save_stats_json(stats, args.json)
        else:
            # Continuous monitoring
            monitor.run_monitoring()
            
    except KeyboardInterrupt:
        print("\n Goodbye!")
    except Exception as e:
        print(f"\n Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())