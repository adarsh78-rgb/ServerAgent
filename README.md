# 🖥️ ServerAgent

ServerAgent is a lightweight Python-based system monitoring tool that tracks:

- ✅ Logged-in users
- 📊 CPU usage
- 💾 RAM & Disk usage
- 🌐 Network upload/download speed
- ⏳ Time-based utilization logs

Logs are recorded every 60 seconds in a file, and automatically reset after 20 entries to keep storage light.

---

## 🚀 Features

- Monitor current user sessions with timestamps.
- Capture system metrics: CPU, RAM, disk.
- Track real-time network speeds (upload/download in KB/s).
- Log stats to `server_monitor_log.txt`.
- Auto-reset logs after a configurable threshold.
- Optionally convert to a `.exe` or Mac binary with `PyInstaller`.

---

## 📂 Sample Log Output

