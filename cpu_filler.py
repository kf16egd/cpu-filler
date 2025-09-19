import os
import time
import multiprocessing

# Read the target total CPU usage percent from environment variable, default is 60%
TARGET_CPU_PERCENT = float(os.getenv("TARGET_CPU", "60"))
# Detect the number of CPU cores
NUM_CORES = os.cpu_count()
INTERVAL = 0.1  # seconds

def cpu_fill_worker(percent_per_core):
    """
    Busy loop to keep the CPU usage for this core at a specific percent.
    """
    work_time = INTERVAL * percent_per_core / 100
    sleep_time = INTERVAL - work_time
    while True:
        start = time.time()
        # Busy wait for work_time seconds
        while time.time() - start < work_time:
            pass
        # Sleep for the rest of interval
        time.sleep(sleep_time)

if __name__ == "__main__":
    # Calculate per-core target percent based on total target percent and number of cores
    percent_per_core = TARGET_CPU_PERCENT
    if NUM_CORES and NUM_CORES > 0:
        percent_per_core = TARGET_CPU_PERCENT / NUM_CORES

    print(f"Detected {NUM_CORES} CPU cores.")
    print(f"Target total CPU: {TARGET_CPU_PERCENT}%, per core: {percent_per_core:.2f}%")

    processes = []
    for _ in range(NUM_CORES):
        p = multiprocessing.Process(target=cpu_fill_worker, args=(percent_per_core,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()