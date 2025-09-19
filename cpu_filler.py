import os
import time
import multiprocessing
import psutil  # For system CPU usage detection

# TARGET_CPU_PERCENT means total system load target (0~100%), achieved by making all cores reach TARGET_CPU_PERCENT
TARGET_CPU_PERCENT = float(os.getenv("TARGET_CPU", "60"))
NUM_CORES = os.cpu_count()
INTERVAL = 0.1  # seconds
# ADJUST_STEP default value is 0.2, allow environment variable ADJUST_STEP to override
ADJUST_STEP = float(os.getenv("ADJUST_STEP", "0.2"))

def cpu_fill_worker(core_id, target_percent):
    """
    Busy loop to keep this core's CPU usage at target_percent percent, auto yielding when system is busy.
    """
    work_ratio = target_percent / 100  # Initial target ratio
    while True:
        sys_cpu = psutil.cpu_percent(interval=None)
        # Yielding logic: decrease load if system is busy, increase if system is idle
        if sys_cpu > target_percent:
            work_ratio = max(0, work_ratio - ADJUST_STEP)
        elif sys_cpu < target_percent:
            work_ratio = min(1, work_ratio + ADJUST_STEP)
        work_time = INTERVAL * work_ratio
        sleep_time = INTERVAL - work_time
        start = time.time()
        # Busy wait for work_time seconds
        while time.time() - start < work_time:
            pass
        # Sleep for the rest of interval
        time.sleep(sleep_time)

if __name__ == "__main__":
    print(f"Detected {NUM_CORES} CPU cores.")
    print(f"Target system CPU (all cores): {TARGET_CPU_PERCENT}%")
    print(f"Each core will fill: {TARGET_CPU_PERCENT}% (with auto yielding)")
    print(f"ADJUST_STEP: {ADJUST_STEP}")

    processes = []
    for i in range(NUM_CORES):
        p = multiprocessing.Process(target=cpu_fill_worker, args=(i, TARGET_CPU_PERCENT))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()