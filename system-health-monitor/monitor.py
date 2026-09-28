#!/usr/bin/env python3
"""System Health Monitor.

Monitors CPU, memory, and disk usage and can alert via email when thresholds are exceeded.
"""

from __future__ import annotations

import argparse
import json
import logging
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional

import psutil
import yaml


class SystemMonitor:
    """Monitor core system health metrics and alert on threshold breaches."""

    DEFAULT_CONFIG: Dict = {
        "thresholds": {"cpu": 80, "memory": 85, "disk": 90},
        "check_interval": 60,
        "email": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "port": 587,
            "from": "monitoring@example.com",
            "to": "admin@example.com",
            "username": "",
            "password": "",
        },
        "logging": {"level": "INFO", "file": "system_monitor.log"},
    }

    def __init__(self, config_file: str = "config.yaml") -> None:
        self.config_file = config_file
        self.config = self._load_config()
        self._setup_logging()
        self.alert_sent = False

    def _load_config(self) -> Dict:
        try:
            with open(self.config_file, "r", encoding="utf-8") as handle:
                loaded = yaml.safe_load(handle) or {}
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found. Using default settings.")
            return self.DEFAULT_CONFIG.copy()
        except yaml.YAMLError as exc:
            print(f"Error parsing config file: {exc}")
            return self.DEFAULT_CONFIG.copy()

        merged = self.DEFAULT_CONFIG.copy()
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
        return merged

    def _setup_logging(self) -> None:
        log_path = Path(self.config["logging"].get("file", "system_monitor.log"))
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            level=getattr(logging, str(self.config["logging"].get("level", "INFO")).upper(), logging.INFO),
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=str(log_path),
            filemode="a",
        )
        self.logger = logging.getLogger("system_monitor")

    def get_system_stats(self) -> Dict:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            load_avg = 0.0
            try:
                if hasattr(psutil, "getloadavg"):
                    load_avg = psutil.getloadavg()[0]
            except (AttributeError, OSError):
                load_avg = 0.0

            network = psutil.net_io_counters()
            return {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cpu": {
                    "percent": cpu_percent,
                    "count_logical": psutil.cpu_count(),
                    "count_physical": psutil.cpu_count(logical=False),
                    "load_avg": round(load_avg, 2),
                },
                "memory": {
                    "percent": memory.percent,
                    "total_gb": round(memory.total / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                },
                "disk": {
                    "percent": round((disk.used / disk.total) * 100, 2),
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv,
                },
                "system": {
                    "uptime_days": uptime.days,
                    "uptime_hours": uptime.seconds // 3600,
                    "process_count": len(psutil.pids()),
                    "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        except Exception as exc:
            self.logger.error("Error collecting system stats: %s", exc)
            return {}

    def check_thresholds(self, stats: Dict) -> List[str]:
        alerts: List[str] = []
        thresholds = self.config.get("thresholds", {})

        if stats.get("cpu", {}).get("percent", 0) > thresholds.get("cpu", 0):
            alerts.append(
                f"CPU usage: {stats['cpu']['percent']:.1f}% (threshold: {thresholds['cpu']}%)"
            )

        if stats.get("memory", {}).get("percent", 0) > thresholds.get("memory", 0):
            alerts.append(
                f"Memory usage: {stats['memory']['percent']:.1f}% (threshold: {thresholds['memory']}%) - "
                f"{stats['memory']['used_gb']:.1f}GB used"
            )

        if stats.get("disk", {}).get("percent", 0) > thresholds.get("disk", 0):
            alerts.append(
                f"Disk usage: {stats['disk']['percent']:.1f}% (threshold: {thresholds['disk']}%) - "
                f"{stats['disk']['used_gb']:.1f}GB used"
            )

        return alerts

    def send_alert(self, alerts: List[str], stats: Dict) -> None:
        if not alerts or not self.config["email"].get("enabled"):
            return
        if self.alert_sent:
            return

        smtp_config = self.config["email"]
        if not smtp_config.get("smtp_server"):
            self.logger.warning("Email alerts enabled but SMTP settings are incomplete.")
            return

        try:
            message = MIMEMultipart()
            message["From"] = smtp_config.get("from", "")
            message["To"] = smtp_config.get("to", "")
            message["Subject"] = f"System Health Alert - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            body = [
                "System Health Alert - Threshold Exceeded",
                "",
                f"Time: {stats['timestamp']}",
                f"System Uptime: {stats['system']['uptime_days']} days, {stats['system']['uptime_hours']} hours",
                "",
                "ALERTS:",
            ]
            body.extend(f"  • {alert}" for alert in alerts)
            body.extend([
                "",
                "CURRENT SYSTEM STATUS:",
                f"  CPU Usage: {stats['cpu']['percent']:.1f}% (Load: {stats['cpu']['load_avg']})",
                f"  Memory Usage: {stats['memory']['percent']:.1f}% ({stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB)",
                f"  Disk Usage: {stats['disk']['percent']:.1f}% ({stats['disk']['used_gb']:.1f}GB / {stats['disk']['total_gb']:.1f}GB)",
                f"  Active Processes: {stats['system']['process_count']}",
            ])
            message.attach(MIMEText("\n".join(body), "plain"))

            server = smtplib.SMTP(smtp_config["smtp_server"], int(smtp_config.get("port", 587)))
            server.starttls()
            server.login(smtp_config["username"], smtp_config["password"])
            server.send_message(message)
            server.quit()

            self.logger.info("Alert email sent successfully")
            self.alert_sent = True
        except Exception as exc:
            self.logger.error("Failed to send email alert: %s", exc)

    def display_stats(self, stats: Dict, alerts: List[str]) -> None:
        print(f"\n{'=' * 60}")
        print(f"SYSTEM HEALTH MONITOR - {stats['timestamp']}")
        print(f"{'=' * 60}")

        cpu_status = "RED" if stats['cpu']['percent'] > self.config['thresholds']['cpu'] else "GREEN"
        print(f"{cpu_status} CPU Usage: {stats['cpu']['percent']:.1f}% (Load: {stats['cpu']['load_avg']}) "
              f"[{stats['cpu']['count_physical']} cores, {stats['cpu']['count_logical']} threads]")

        memory_status = "RED" if stats['memory']['percent'] > self.config['thresholds']['memory'] else "GREEN"
        print(f"{memory_status} Memory Usage: {stats['memory']['percent']:.1f}% "
              f"({stats['memory']['used_gb']:.1f}GB / {stats['memory']['total_gb']:.1f}GB)")

        disk_status = "RED" if stats['disk']['percent'] > self.config['thresholds']['disk'] else "GREEN"
        print(f"{disk_status} Disk Usage: {stats['disk']['percent']:.1f}% "
              f"({stats['disk']['used_gb']:.1f}GB / {stats['disk']['total_gb']:.1f}GB)")

        print(f"Uptime: {stats['system']['uptime_days']} days, {stats['system']['uptime_hours']} hours")
        print(f"Active Processes: {stats['system']['process_count']}")
        print(f"Network: ⬆{stats['network']['bytes_sent']:,} bytes sent, ⬇{stats['network']['bytes_recv']:,} bytes received")

        if alerts:
            print(f"\nACTIVE ALERTS ({len(alerts)}):")
            for alert in alerts:
                print(f"   {alert}")
        else:
            print("\nAll systems normal - no alerts")

        print(f"{'=' * 60}")

    def save_stats_json(self, stats: Dict, filename: Optional[str] = None) -> None:
        file_name = filename or f"system_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(file_name, "w", encoding="utf-8") as handle:
                json.dump(stats, handle, indent=2)
            self.logger.info("Statistics saved to %s", file_name)
        except Exception as exc:
            self.logger.error("Failed to save statistics: %s", exc)

    def run_once(self) -> Dict:
        stats = self.get_system_stats()
        if not stats:
            return {}

        alerts = self.check_thresholds(stats)
        self.display_stats(stats, alerts)

        if alerts:
            self.logger.warning("System alerts triggered: %s threshold(s) exceeded", len(alerts))
            self.send_alert(alerts, stats)

        return stats

    def run_monitoring(self) -> None:
        self.logger.info("Starting system health monitoring...")
        self.logger.info(
            "Monitoring interval: %s seconds | CPU threshold: %s%% | Memory threshold: %s%% | Disk threshold: %s%%",
            self.config["check_interval"],
            self.config["thresholds"].get("cpu", 80),
            self.config["thresholds"].get("memory", 85),
            self.config["thresholds"].get("disk", 90),
        )

        try:
            while True:
                stats = self.run_once()
                if stats:
                    self.logger.info(
                        "CPU: %.1f%% | Memory: %.1f%% | Disk: %.1f%%",
                        stats["cpu"]["percent"],
                        stats["memory"]["percent"],
                        stats["disk"]["percent"],
                    )
                time.sleep(int(self.config["check_interval"]))
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user.")
            print("\nSystem monitoring stopped.")
        except Exception as exc:
            self.logger.error("Monitoring error: %s", exc)
            raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="System Health Monitor - Monitor CPU, memory, and disk usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python monitor.py                    # Run continuously with default config
  python monitor.py -c custom.yaml     # Use custom config
  python monitor.py --once             # Run once and exit
  python monitor.py --json output.json # Save stats to JSON
        """,
    )
    parser.add_argument("-c", "--config", default="config.yaml", help="Configuration file path")
    parser.add_argument("--once", action="store_true", help="Run monitoring once and exit")
    parser.add_argument("--json", help="Save statistics to JSON file")
    parser.add_argument("--version", action="version", version="System Health Monitor v1.1.0")
    args = parser.parse_args()

    try:
        monitor = SystemMonitor(args.config)
        if args.once:
            stats = monitor.run_once()
            if args.json and stats:
                monitor.save_stats_json(stats, args.json)
        else:
            monitor.run_monitoring()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as exc:
        print(f"\nError: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
