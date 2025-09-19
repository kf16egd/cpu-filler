FROM python:3.10-slim

# Install psutil for CPU monitoring
RUN pip install psutil

# Copy the CPU filler script
COPY cpu_filler.py /cpu_filler.py

# Set environment variables with default values (can be overridden at runtime)
# TARGET_CPU: Target total CPU usage percentage (default: 60)
# DURATION_SEC: Duration to run in seconds (default: 3600)
# THREADS: Number of worker threads (default: 2)
ENV TARGET_CPU=60
ENV DURATION_SEC=3600
ENV THREADS=2

# Default command: run the script
CMD ["python", "/cpu_filler.py"]