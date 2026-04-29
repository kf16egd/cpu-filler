import os
import time
import threading
import multiprocessing
import psutil  # For system CPU/memory usage detection

# --- CPU settings ---
TARGET_CPU_PERCENT = float(os.getenv("TARGET_CPU", "60"))
NUM_CORES = os.cpu_count()
CPU_INTERVAL = 0.1  # seconds
ADJUST_STEP = float(os.getenv("ADJUST_STEP", "0.2"))

# --- Memory settings ---
TARGET_MEM_PERCENT = float(os.getenv("TARGET_MEM", "60"))
MEM_INTERVAL = float(os.getenv("MEM_INTERVAL", "1.0"))
ADJUST_STEP_MB = float(os.getenv("MEM_ADJUST_STEP_MB", "64"))

PAGE_SIZE = 4096  # bytes; used to touch each OS memory page after allocation


def cpu_fill_worker(core_id, target_percent):
    """
    Busy loop to keep this core's CPU usage at target_percent percent,
    auto yielding when the system is busy.
    """
    work_ratio = target_percent / 100
    while True:
        sys_cpu = psutil.cpu_percent(interval=None)
        if sys_cpu > target_percent:
            work_ratio = max(0, work_ratio - ADJUST_STEP)
        elif sys_cpu < target_percent:
            work_ratio = min(1, work_ratio + ADJUST_STEP)
        work_time = CPU_INTERVAL * work_ratio
        sleep_time = CPU_INTERVAL - work_time
        start = time.time()
        while time.time() - start < work_time:
            pass
        time.sleep(sleep_time)


def mem_fill_worker():
    """
    Allocate or release memory chunks to keep system memory usage at
    TARGET_MEM_PERCENT, running in a background thread.
    """
    allocated = []
    chunk_size = int(ADJUST_STEP_MB * 1024 * 1024)  # Convert MB to bytes

    while True:
        current_percent = psutil.virtual_memory().percent

        if current_percent < TARGET_MEM_PERCENT:
            try:
                buf = bytearray(chunk_size)
                # Touch each page to ensure the OS actually commits the memory
                for i in range(0, len(buf), PAGE_SIZE):
                    buf[i] = 1
                allocated.append(buf)
            except MemoryError:
                pass
        elif current_percent > TARGET_MEM_PERCENT:
            if allocated:
                allocated.pop()

        time.sleep(MEM_INTERVAL)


if __name__ == "__main__":
    mem = psutil.virtual_memory()
    print(f"=== CPU Filler ===")
    print(f"  Detected {NUM_CORES} CPU cores")
    print(f"  Target CPU usage: {TARGET_CPU_PERCENT}%")
    print(f"  ADJUST_STEP: {ADJUST_STEP}")
    print(f"=== Memory Filler ===")
    print(f"  Total memory: {mem.total / (1024 ** 3):.1f} GB")
    print(f"  Current memory usage: {mem.percent}%")
    print(f"  Target memory usage: {TARGET_MEM_PERCENT}%")
    print(f"  MEM_ADJUST_STEP_MB: {ADJUST_STEP_MB} MB")
    print(f"  MEM_INTERVAL: {MEM_INTERVAL} s")

    # Start memory filler in a background thread
    mem_thread = threading.Thread(target=mem_fill_worker, daemon=True)
    mem_thread.start()

    # Start one CPU filler process per core
    processes = []
    for i in range(NUM_CORES):
        p = multiprocessing.Process(target=cpu_fill_worker, args=(i, TARGET_CPU_PERCENT))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
