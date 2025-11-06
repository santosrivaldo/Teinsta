"""
Sistema de Gestão ISO 27001
Aplicação Flask modular
"""

from flask import Flask
import os
from pathlib import Path

# Tentar carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações de segurança
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'iso27001-secret-key-change-in-production')
    app.config['PASSWORD'] = os.environ.get('DASHBOARD_PASSWORD', 'admin123')
    
    # Configurações de arquivos
    data_dir = Path(os.environ.get('DATA_DIR', '.'))
    data_dir.mkdir(exist_ok=True)
    
    app.config['UPLOAD_FOLDER'] = data_dir / 'uploads'
    app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'png', 'jpg', 'jpeg', 'zip', 'rar'}
    app.config['DB_PATH'] = data_dir / 'iso27001.db'
    
    # Registrar blueprints
    from app.routes import auth, politicas, nao_conformidades, auditorias, api
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(politicas.bp)
    app.register_blueprint(nao_conformidades.bp)
    app.register_blueprint(auditorias.bp)
    app.register_blueprint(api.bp)
    
    # Por enquanto, importar rotas do app.py original para dashboard, controles e modulos
    # TODO: Refatorar completamente esses módulos
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Importar e registrar rotas do app.py original
    from app_old import app as old_app
    for rule in old_app.url_map.iter_rules():
        if rule.endpoint not in ['static'] and not rule.rule.startswith('/api') and not rule.rule.startswith('/politicas') and not rule.rule.startswith('/nao-conformidades') and not rule.rule.startswith('/auditorias') and not rule.rule.startswith('/login') and not rule.rule.startswith('/logout'):
            # Registrar manualmente as rotas que ainda não foram modularizadas
            pass
    
    # Inicializar banco de dados
    from app.utils.database import init_db
    try:
        init_db(app.config['DB_PATH'])
        # Importar dados padrão após criar as tabelas
        try:
            from app.utils.seed_data import import_default_data
            import_default_data(app.config['DB_PATH'])
        except ImportError:
            # Se o módulo não existir ainda, continuar normalmente
            pass
        except Exception as e:
            # Se houver erro ao importar dados, logar mas não impedir a aplicação
            import sys
            print(f"AVISO: Erro ao importar dados padrão: {e}", file=sys.stderr)
    except Exception as e:
        import sys
        print(f"AVISO: Erro ao inicializar banco de dados: {e}", file=sys.stderr)
    
    return app

