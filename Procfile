release: python railway_init.py
web: /bin/sh -c "gunicorn backend.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --workers 1 --timeout 60 --graceful-timeout 30 --access-logfile - --error-logfile - --log-level info"
