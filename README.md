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
