import psutil
import time
import os
from datetime import datetime


LOG_FILE = "system_monitor.log"
INTERVAL = 60  # seconds

def get_logged_in_users():
    users = psutil.users()
    return [f"{u.name} ({u.host}) at {datetime.fromtimestamp(u.started).strftime('%Y-%m-%d %H:%M:%S')}" for u in users]


def log_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu": cpu_usage,
        "ram_used": ram.used / (1024 ** 3),  # GB
        "ram_total": ram.total / (1024 ** 3),
        "disk_used": disk.used / (1024 ** 3),
        "disk_total": disk.total / (1024 ** 3)
    }
    
def get_network_speed(prev_sent, prev_recv):
    current = psutil.net_io_counters()
    sent_speed = (current.bytes_sent - prev_sent) / INTERVAL  # bytes/sec
    recv_speed = (current.bytes_recv - prev_recv) / INTERVAL
    return {
        "upload_kbps": sent_speed / 1024,
        "download_kbps": recv_speed / 1024,
        "sent": current.bytes_sent,
        "recv": current.bytes_recv
    }
    
def log_stats():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    users = get_logged_in_users()
    stats = log_system_info()
    prev_sent, prev_recv = 0, 0
    if os.path.exists(LOG_FILE):
        # Try to get previous network stats from last log (optional, can be improved)
        prev_sent, prev_recv = 0, 0
    net = get_network_speed(prev_sent, prev_recv)
    with open(LOG_FILE, "a") as f:
        f.write(f"\n--- Log Time: {now} ---\n")
        f.write("Logged in users:\n")
        for user in users:
            f.write(f"  - {user}\n")

        f.write("System Stats:\n")
        f.write(f"  CPU Usage: {stats['cpu']}%\n")
        f.write(f"  RAM Usage: {stats['ram_used']:.2f} GB / {stats['ram_total']:.2f} GB\n")
        f.write(f"  Disk Usage: {stats['disk_used']:.2f} GB / {stats['disk_total']:.2f} GB\n")

        f.write("Network Speed:\n")
        f.write(f"  Upload Speed: {net['upload_kbps']:.2f} KB/s\n")
        f.write(f"  Download Speed: {net['download_kbps']:.2f} KB/s\n")
    return net["sent"], net["recv"]


if __name__ == "__main__":
    print(f"Server Monitor Started. Logging every {INTERVAL} seconds...\nLog file: {LOG_FILE}")
    while True:
        try:
            log_stats()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break