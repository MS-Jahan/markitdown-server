# 🎯 Quick Copy-Paste for Coolify

## Core Variables (Copy All)

```
PORT=8080
MAX_FILE_SIZE_MB=50
LOG_LEVEL=INFO
ENABLE_MARKITDOWN_PLUGINS=false
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=120
GUNICORN_MAX_REQUESTS=1000
GUNICORN_MAX_REQUESTS_JITTER=50
GUNICORN_GRACEFUL_TIMEOUT=30
DOCKER_MEMORY_LIMIT=2G
DOCKER_CPU_LIMIT=2.0
DOCKER_MEMORY_RESERVATION=512M
DOCKER_CPU_RESERVATION=0.5
```

## Optional: LLM Features (Mark LLM_API_KEY as Secret)

```
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-your-api-key-here
```

---

## 🔍 What Each Variable Does

**MAX_FILE_SIZE_MB** = Upload size limit (50MB default)
**LOG_LEVEL** = Logging detail (INFO, DEBUG, WARNING, ERROR)
**GUNICORN_WORKERS** = Concurrent request handlers (4 default)
**GUNICORN_TIMEOUT** = Max processing time per file (120s)
**GUNICORN_MAX_REQUESTS** = Worker restarts (prevents memory leaks)
**DOCKER_MEMORY_LIMIT** = RAM limit (2GB default)

---

## ⚙️ Common Adjustments

**Need to handle 100MB files?**
```
MAX_FILE_SIZE_MB=100
GUNICORN_TIMEOUT=300
DOCKER_MEMORY_LIMIT=4G
```

**High traffic site?**
```
GUNICORN_WORKERS=8
DOCKER_MEMORY_LIMIT=4G
DOCKER_CPU_LIMIT=4.0
```

**Want AI image descriptions?**
```
LLM_MODEL=gpt-4o
LLM_API_KEY=sk-proj-xxxxx
```
