FROM python:3.10-slim

# Install psutil for CPU/memory monitoring
RUN pip install psutil

# Copy filler scripts
COPY filler.py /filler.py
COPY cpu_filler.py /cpu_filler.py
COPY mem_filler.py /mem_filler.py

# Set environment variables with default values (can be overridden at runtime)
# TARGET_CPU: Target total CPU usage percentage (default: 60)
# ADJUST_STEP: CPU load adjustment step per interval (default: 0.2)
# TARGET_MEM: Target total memory usage percentage (default: 60)
# MEM_ADJUST_STEP_MB: Memory allocation step size in MB (default: 64)
# MEM_INTERVAL: Memory check interval in seconds (default: 1.0)
ENV TARGET_CPU=60
ENV ADJUST_STEP=0.2
ENV TARGET_MEM=60
ENV MEM_ADJUST_STEP_MB=64
ENV MEM_INTERVAL=1.0

# Default command: run combined CPU + memory filler
CMD ["python", "/filler.py"]