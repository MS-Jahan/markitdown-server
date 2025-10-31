# MarkItDown Server - Coolify Environment Variables

Copy and paste these into your **Coolify Environment Variables** section:

## 📋 **Required Variables** (with defaults)

```bash
# Server Configuration
PORT=8080

# Application Configuration
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
ENABLE_MARKITDOWN_PLUGINS=false

# Gunicorn Workers
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
GUNICORN_MAX_REQUESTS=1000
GUNICORN_MAX_REQUESTS_JITTER=50
GUNICORN_GRACEFUL_TIMEOUT=30

# Docker Resource Limits
DOCKER_MEMORY_LIMIT=2G
DOCKER_CPU_LIMIT=2.0
DOCKER_MEMORY_RESERVATION=512M
DOCKER_CPU_RESERVATION=0.5
```

## 🔐 **Optional: LLM Integration** (mark as Secret in Coolify)

For AI-powered image descriptions in PDFs/PowerPoint:

```bash
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-openai-api-key-here
```

---

## 📊 **Variable Reference**

### **Server Configuration**

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | External port to expose the server on |

### **Application Settings**

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_FILE_SIZE_MB` | `50` | Maximum upload size in MB. Increase for larger files. |
| `LOG_LEVEL` | `INFO` | Logging verbosity: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `ENABLE_MARKITDOWN_PLUGINS` | `false` | Enable third-party MarkItDown plugins (set to `true`) |

### **Performance Tuning**

| Variable | Default | Description |
|----------|---------|-------------|
| `GUNICORN_WORKERS` | `4` | Number of worker processes. Formula: `(CPU cores × 2) + 1` |
| `GUNICORN_TIMEOUT` | `120` | Request timeout in seconds. Increase for large files. |
| `GUNICORN_MAX_REQUESTS` | `1000` | Restart worker after N requests (prevents memory leaks) |
| `GUNICORN_MAX_REQUESTS_JITTER` | `50` | Random variance to prevent simultaneous restarts |

### **Resource Limits**

| Variable | Default | Description |
|----------|---------|-------------|
| `DOCKER_MEMORY_LIMIT` | `2G` | Hard memory limit. Container killed if exceeded. |
| `DOCKER_CPU_LIMIT` | `2.0` | CPU cores limit (2.0 = 2 full cores) |
| `DOCKER_MEMORY_RESERVATION` | `512M` | Guaranteed memory allocation |
| `DOCKER_CPU_RESERVATION` | `0.5` | Guaranteed CPU allocation |

### **LLM Integration (Optional)**

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_MODEL` | (empty) | OpenAI model: `gpt-4o`, `gpt-4-vision-preview`, `gpt-4o-mini` |
| `LLM_API_KEY` | (empty) | OpenAI API key (mark as **Secret** in Coolify!) |

---

## 🎯 **Recommended Configurations**

### **Small Deployment** (Low traffic, 1-2 concurrent users)
```bash
MAX_FILE_SIZE_MB=50
GUNICORN_WORKERS=2
DOCKER_MEMORY_LIMIT=1G
DOCKER_CPU_LIMIT=1.0
```

### **Medium Deployment** (Moderate traffic, 5-10 concurrent users)
```bash
MAX_FILE_SIZE_MB=100
GUNICORN_WORKERS=4
DOCKER_MEMORY_LIMIT=2G
DOCKER_CPU_LIMIT=2.0
```

### **Large Deployment** (High traffic, 20+ concurrent users)
```bash
MAX_FILE_SIZE_MB=200
GUNICORN_WORKERS=8
DOCKER_MEMORY_LIMIT=4G
DOCKER_CPU_LIMIT=4.0
GUNICORN_MAX_REQUESTS=500
```

### **Very Large Files** (Processing 100MB+ PDFs)
```bash
MAX_FILE_SIZE_MB=200
GUNICORN_WORKERS=2
GUNICORN_TIMEOUT=300
DOCKER_MEMORY_LIMIT=4G
DOCKER_CPU_LIMIT=2.0
```

---

## 🚀 **Quick Start in Coolify**

1. **Go to your service** → **Environment Variables**
2. **Add variables** one by one (or bulk paste)
3. **Mark sensitive variables** as "Secret" (e.g., `LLM_API_KEY`)
4. **Save and restart** the service
5. **Monitor logs** to verify configuration loaded correctly

Look for this log line on startup:
```
Server configuration: MAX_FILE_SIZE=50MB, REQUEST_TIMEOUT=120s, ENABLE_PLUGINS=False
```

---

## 🔧 **Troubleshooting**

**Memory issues?**
- Reduce `GUNICORN_WORKERS`
- Increase `DOCKER_MEMORY_LIMIT`
- Lower `GUNICORN_MAX_REQUESTS` for more frequent worker recycling

**Slow conversions?**
- Increase `GUNICORN_TIMEOUT`
- Increase `GUNICORN_WORKERS` (if you have CPU headroom)
- Check if files are hitting `MAX_FILE_SIZE_MB` limit

**Workers restarting too often?**
- Increase `GUNICORN_MAX_REQUESTS`
- Check for memory leaks in logs

---

## 📚 **Additional Resources**

- [MarkItDown GitHub](https://github.com/microsoft/markitdown)
- [Gunicorn Settings](https://docs.gunicorn.org/en/stable/settings.html)
- [OpenAI Models](https://platform.openai.com/docs/models)
