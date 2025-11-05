# Configuração do Gunicorn para produção
import multiprocessing
import os

# Número de workers
workers = multiprocessing.cpu_count() * 2 + 1

# Binding
bind = f"0.0.0.0:{os.environ.get('PORT', '6000')}"

# Timeout
timeout = 120

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.environ.get('LOG_LEVEL', 'info')

# Worker class
worker_class = "sync"

# Preload
preload_app = True

# Max requests (ajuda a prevenir memory leaks)
max_requests = 1000
max_requests_jitter = 50

