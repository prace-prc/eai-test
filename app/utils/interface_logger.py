import os
from datetime import datetime

LOG_DIR = "interface_logs"
os.makedirs(LOG_DIR, exist_ok=True)


def write_interface_log(request_id, step, status, message=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_line = f"[{now}] [{request_id}] [{step}] [{status}] {message}\n"

    filename = f"{LOG_DIR}/interface_{datetime.now().strftime('%Y%m%d')}.log"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(log_line)