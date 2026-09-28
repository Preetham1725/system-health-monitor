import yaml

from monitor import SystemMonitor


def test_default_config_loads_and_has_keys(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump({"thresholds": {"cpu": 75, "memory": 80, "disk": 85}}), encoding="utf-8")

    monitor = SystemMonitor(str(config_path))
    assert monitor.config["thresholds"]["cpu"] == 75
    assert monitor.config["thresholds"]["memory"] == 80
    assert monitor.config["thresholds"]["disk"] == 85


def test_check_thresholds_detects_alerts():
    monitor = SystemMonitor(config_file="nonexistent.yaml")
    stats = {
        "cpu": {"percent": 90.0},
        "memory": {"percent": 97.0, "used_gb": 7.0, "total_gb": 8.0},
        "disk": {"percent": 80.0, "used_gb": 10.0, "total_gb": 12.0},
    }

    alerts = monitor.check_thresholds(stats)
    assert any("CPU usage" in alert for alert in alerts)
    assert any("Memory usage" in alert for alert in alerts)
    assert any("Disk usage" in alert for alert in alerts)
