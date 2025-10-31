# MarkItDown Server

A production-ready HTTP server for converting documents to Markdown using [Microsoft's MarkItDown](https://github.com/microsoft/markitdown) library.

## Features

- **Stream-based processing** - No temporary files, minimal memory footprint
- **Production-ready** - Uses Gunicorn WSGI server with worker management
- **Memory-safe** - Built-in file size limits, request timeouts, and worker recycling
- **Secure** - Runs as non-root user, multi-stage Docker build
- **Observable** - Health checks, structured logging, and request metrics
- **Docker-optimized** - Multi-stage build for minimal image size

## Supported File Formats

- PDF documents
- Microsoft Office (DOCX, XLSX, PPTX)
- Images (JPEG, PNG, etc.) with EXIF metadata
- Audio files (with transcription)
- HTML, CSV, JSON, XML
- ZIP archives
- EPUB books
- And more...

## Quick Start

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

### Using Docker

```bash
# Build the image
docker build -t markitdown-server .

# Run the container
docker run -d -p 8080:8080 --name markitdown-server markitdown-server
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python server.py
```

## API Usage

### Convert a File

```bash
curl -X POST http://localhost:8080/convert \
  -F "file=@document.pdf" \
  -o output.md
```

### Health Check

```bash
curl http://localhost:8080/health
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GUNICORN_WORKERS` | `(CPU cores * 2) + 1` | Number of worker processes |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |

### File Size Limits

Default maximum file size: **50 MB**

To change, edit `MAX_FILE_SIZE` in `server.py`:

```python
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
```

### Memory Limits

Docker Compose sets a 2GB memory limit by default. Adjust in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      memory: 4G  # Increase for larger files
```

## Performance Optimizations

### 1. **Stream-Based Processing**
- Uses `convert_stream()` to process files directly from memory
- No temporary file creation = faster and less I/O

### 2. **Worker Management**
- Workers restart after 1,000 requests to prevent memory leaks
- Configurable worker count based on CPU cores

### 3. **Request Timeouts**
- 120-second timeout for long-running PDF conversions
- Prevents workers from hanging indefinitely

### 4. **Multi-Stage Docker Build**
- Separates build dependencies from runtime
- Results in smaller, more secure images

### 5. **Singleton MarkItDown Instance**
- Reuses converter instance across requests
- Eliminates initialization overhead

## Memory Leak Prevention

This server implements several strategies to prevent memory leaks common with PDF processing:

1. **File size limits** - Reject files larger than 50 MB
2. **Worker recycling** - Restart workers after 1,000 requests
3. **Request timeouts** - Kill long-running conversions
4. **Stream processing** - No disk I/O, minimal memory usage
5. **Memory limits** - Docker enforces hard memory caps

## Troubleshooting

### Memory Issues with Large PDFs

If you're processing very large PDFs (>50 MB):

1. Increase `MAX_FILE_SIZE` in `server.py`
2. Increase Docker memory limit in `docker-compose.yml`
3. Reduce `GUNICORN_WORKERS` to limit concurrent processing
4. Consider using a dedicated PDF parser like [Docling](https://github.com/ds4sd/docling)

### Worker Timeouts

If conversions are timing out:

1. Increase `timeout` in `gunicorn.conf.py`
2. Check logs for specific errors: `docker logs markitdown-server`

### Build Errors

If Docker build fails with missing dependencies:

```bash
# Clear Docker cache and rebuild
docker-compose build --no-cache
```

## Production Deployment

### Coolify / Kubernetes

The server includes:
- Health check endpoint (`/health`) for readiness probes
- Liveness checks via Docker HEALTHCHECK
- Graceful shutdown handling
- Structured JSON logging

### Behind a Reverse Proxy

When deploying behind Nginx/Traefik, ensure:
- Client max body size matches your file limit
- Proxy timeouts exceed worker timeouts (120s)

Example Nginx config:

```nginx
location /convert {
    proxy_pass http://markitdown-server:8080;
    client_max_body_size 50M;
    proxy_read_timeout 180s;
}
```

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP POST /convert
       ▼
┌─────────────────────┐
│  Gunicorn Workers   │
│  (4 processes)      │
└──────┬──────────────┘
       │
       ▼
┌──────────────────────┐
│  MarkItDown Library  │
│  (Singleton Instance)│
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│  Format Converters   │
│  (PDF, DOCX, etc.)   │
└──────────────────────┘
```

## Development

### Running Tests

```bash
# TODO: Add tests
pytest tests/
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## License

MIT License - See Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) for the underlying library license.

## Credits

- Built on [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- Optimizations inspired by production best practices and community feedback
