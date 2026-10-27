"""
BNS Instagram Automated Scheduler
Runs 2 or 3 times daily at specified target hours (e.g. 10:00 AM, 3:00 PM, 8:00 PM IST).
"""
import time
import datetime
import subprocess
import sys
from pathlib import Path

# Target hours for 3 posts per day (24-hour clock, local system time)
# e.g., 10:00 AM, 15:00 (3:00 PM), 20:00 (8:00 PM)
TARGET_HOURS = [10, 15, 20]

def log(msg: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

def run_post():
    script_path = Path(__file__).resolve().parent / "auto_poster.py"
    cmd = [sys.executable, str(script_path)]
    log(f"Triggering scheduled post: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

def main():
    log("BNS 3x/Day Automated Scheduler started.")
    log(f"Configured schedule times: {', '.join(f'{h:02d}:00' for h in TARGET_HOURS)}")
    
    last_triggered_hour = -1
    while True:
        now = datetime.datetime.now()
        cur_hour = now.hour
        cur_minute = now.minute

        # Check if current time matches any target hour (within the first 5 minutes of the hour)
        if cur_hour in TARGET_HOURS and cur_minute < 5 and last_triggered_hour != cur_hour:
            log(f"Time slot reached: {cur_hour:02d}:{cur_minute:02d}. Executing post...")
            run_post()
            last_triggered_hour = cur_hour
        elif cur_hour not in TARGET_HOURS:
            last_triggered_hour = -1

        time.sleep(60)

if __name__ == "__main__":
    main()
