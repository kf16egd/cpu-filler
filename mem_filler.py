import os
import time
import psutil  # For system memory usage detection

# TARGET_MEM_PERCENT means total system memory usage target (0~100%)
TARGET_MEM_PERCENT = float(os.getenv("TARGET_MEM", "60"))
INTERVAL = float(os.getenv("MEM_INTERVAL", "1.0"))
# ADJUST_STEP_MB default value is 64 MB, allow environment variable MEM_ADJUST_STEP_MB to override
ADJUST_STEP_MB = float(os.getenv("MEM_ADJUST_STEP_MB", "64"))

def mem_fill():
    """
    Allocate or release memory chunks to keep system memory usage at TARGET_MEM_PERCENT.
    """
    allocated = []
    chunk_size = int(ADJUST_STEP_MB * 1024 * 1024)  # Convert MB to bytes

    while True:
        mem = psutil.virtual_memory()
        current_percent = mem.percent

        if current_percent < TARGET_MEM_PERCENT:
            # Allocate more memory
            try:
                buf = bytearray(chunk_size)
                # Write to each page to ensure the OS actually commits the memory
                for i in range(0, len(buf), 4096):
                    buf[i] = 1
                allocated.append(buf)
            except MemoryError:
                pass
        elif current_percent > TARGET_MEM_PERCENT:
            # Release some memory
            if allocated:
                allocated.pop()

        time.sleep(INTERVAL)

if __name__ == "__main__":
    mem = psutil.virtual_memory()
    print(f"Total memory: {mem.total / (1024 ** 3):.1f} GB")
    print(f"Current memory usage: {mem.percent}%")
    print(f"Target memory usage: {TARGET_MEM_PERCENT}%")
    print(f"MEM_ADJUST_STEP_MB: {ADJUST_STEP_MB} MB")
    print(f"MEM_INTERVAL: {INTERVAL} s")
    mem_fill()
