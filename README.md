# Dynamic CPU Filler

This project automatically fills system CPU usage up to a target percentage.  
It is designed for testing, benchmarking, or reserving CPU resources.

## Features

- Dynamically compensates to reach your desired CPU usage
- Configurable via environment variables
- Docker-ready

## Usage

### Build Docker Image

```bash
docker build -t cpu-filler .
```

### Run the Container

```bash
docker run --rm \
  -e TARGET_CPU=60 \
  -e DURATION_SEC=600 \
  -e THREADS=2 \
  cpu-filler
```

- `TARGET_CPU`: Target total CPU usage percentage (default: 60)
- `DURATION_SEC`: Duration to run, in seconds (default: 3600)
- `THREADS`: Number of threads to use (default: number of logical CPUs)

## Publish to GitHub Container Registry (GHCR)

1. Login to GHCR:
   ```bash
   echo $GHCR_TOKEN | docker login ghcr.io -u <your_github_username> --password-stdin
   ```
2. Tag and push image:
   ```bash
   docker tag cpu-filler ghcr.io/<your_github_username>/cpu-filler:latest
   docker push ghcr.io/<your_github_username>/cpu-filler:latest
   ```

## License

MIT
