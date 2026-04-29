FROM python:3.10-slim

# Install psutil for CPU/memory monitoring
RUN pip install psutil

# Copy filler scripts and entrypoint
COPY cpu_filler.py /cpu_filler.py
COPY mem_filler.py /mem_filler.py
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set environment variables with default values (can be overridden at runtime)
# MODE: Which filler to run — cpu (default), mem, or all
# TARGET_CPU: Target total CPU usage percentage (default: 60)
# TARGET_MEM: Target total memory usage percentage (default: 60)
# MEM_ADJUST_STEP_MB: Memory allocation step size in MB (default: 64)
# MEM_INTERVAL: Memory check interval in seconds (default: 1.0)
ENV MODE=cpu
ENV TARGET_CPU=60
ENV TARGET_MEM=60
ENV MEM_ADJUST_STEP_MB=64
ENV MEM_INTERVAL=1.0

# Default command: run via entrypoint
ENTRYPOINT ["/entrypoint.sh"]