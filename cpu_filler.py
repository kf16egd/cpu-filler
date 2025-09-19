import os
import time
import multiprocessing

# TARGET_CPU_PERCENT means total system load target (0~100%), achieved by making all cores reach TARGET_CPU_PERCENT
TARGET_CPU_PERCENT = float(os.getenv("TARGET_CPU", "60"))
NUM_CORES = os.cpu_count()
INTERVAL = 0.1  # seconds

def cpu_fill_worker(target_percent):
    """
    Busy loop to keep this core's CPU usage at target_percent percent.
    """
    work_time = INTERVAL * target_percent / 100
    sleep_time = INTERVAL - work_time
    while True:
        start = time.time()
        # Busy wait for work_time seconds
        while time.time() - start < work_time:
            pass
        # Sleep for the rest of interval
        time.sleep(sleep_time)

if __name__ == "__main__":
    print(f"Detected {NUM_CORES} CPU cores.")
    print(f"Target system CPU (all cores): {TARGET_CPU_PERCENT}%")
    print(f"Each core will fill: {TARGET_CPU_PERCENT}%")

    processes = []
    for _ in range(NUM_CORES):
        p = multiprocessing.Process(target=cpu_fill_worker, args=(TARGET_CPU_PERCENT,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
