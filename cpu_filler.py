import psutil
import time
import threading
import os

# Target total CPU usage percentage (set via environment variable)
TARGET_CPU_PERCENT = float(os.getenv("TARGET_CPU", "60"))
# How often to check system CPU usage, in seconds
CHECK_INTERVAL = 0.5
# How long to run (seconds, set via environment variable)
DURATION_SEC = int(os.getenv("DURATION_SEC", "3600"))
# Number of worker threads (set via environment variable or defaults to logical CPUs)
THREADS = int(os.getenv("THREADS", str(os.cpu_count())))

def busy_wait(duration):
    """
    Busy wait for a given duration (seconds).
    """
    end = time.time() + duration
    while time.time() < end:
        pass

def cpu_filler():
    """
    Dynamically fills CPU usage to reach the target percentage.
    """
    start_time = time.time()
    while time.time() - start_time < DURATION_SEC:
        current_cpu = psutil.cpu_percent(interval=None)
        fill_percent = max(0, TARGET_CPU_PERCENT - current_cpu)
        # Calculate busy loop time for this interval
        busy_time = CHECK_INTERVAL * fill_percent / 100.0
        sleep_time = CHECK_INTERVAL - busy_time
        if busy_time > 0:
            busy_wait(busy_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    workers = []
    for _ in range(THREADS):
        t = threading.Thread(target=cpu_filler)
        t.daemon = True
        t.start()
        workers.append(t)
    for t in workers:
        t.join()