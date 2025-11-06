"""
Configurações da aplicação
"""

import os
from pathlib import Path

# Tentar carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'iso27001-secret-key-change-in-production')
    PASSWORD = os.environ.get('DASHBOARD_PASSWORD', 'admin123')
    
    # Diretórios
    data_dir = Path(os.environ.get('DATA_DIR', '.'))
    data_dir.mkdir(exist_ok=True)
    
    UPLOAD_FOLDER = data_dir / 'uploads'
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    DB_PATH = data_dir / 'iso27001.db'
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'png', 'jpg', 'jpeg', 'zip', 'rar'}

