# Dynamic CPU & Memory Filler

This project automatically fills system CPU **and** memory usage up to target percentages simultaneously.  
It is designed for testing, benchmarking, or reserving system resources.

## Features

- Fills CPU and memory at the same time by default
- Dynamically compensates to reach your desired usage levels
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
  -e TARGET_MEM=70 \
  cpu-filler
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `TARGET_CPU` | Target total CPU usage percentage | `60` |
| `ADJUST_STEP` | CPU load adjustment step per interval | `0.2` |
| `TARGET_MEM` | Target total memory usage percentage | `60` |
| `MEM_ADJUST_STEP_MB` | Memory allocation/release step size in MB | `64` |
| `MEM_INTERVAL` | Memory check interval in seconds | `1.0` |

### Run individual fillers

If you only need one of the fillers, you can override the command:

```bash
# CPU only
docker run --rm -e TARGET_CPU=60 cpu-filler python /cpu_filler.py

# Memory only
docker run --rm -e TARGET_MEM=70 cpu-filler python /mem_filler.py
```

## Multi-Architecture Images

Images are automatically built and published to GHCR for both `linux/amd64` and `linux/arm64` platforms on every push to `main` and on every release.

### Tags

| Trigger | Tags produced |
|---------|--------------|
| Push to `main` | `latest`, `sha-<short>` |
| Release tag (e.g. `v1.2.3`) | `v1.2.3`, `latest`, `sha-<short>` |

### Pull a specific platform

```bash
# default (registry picks best match for your host)
docker pull ghcr.io/kf16egd/cpu-filler:latest

# force a specific platform
docker pull --platform linux/arm64 ghcr.io/kf16egd/cpu-filler:latest
```

### Verify platform support

```bash
docker buildx imagetools inspect ghcr.io/kf16egd/cpu-filler:latest
```

The output should list both `linux/amd64` and `linux/arm64` manifests, confirming the image is a proper multi-arch manifest list with no `unknown/unknown` entries.

## Publish to GitHub Container Registry (GHCR)

1. Login to GHCR:
   ```bash
   echo $GHCR_TOKEN | docker login ghcr.io -u <your_github_username> --password-stdin
   ```
2. Build and push a multi-arch image locally:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64 \
     -t ghcr.io/<your_github_username>/cpu-filler:latest \
     --push .
   ```

## License

MIT
