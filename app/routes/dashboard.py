"""Rotas do dashboard - TEMPORÁRIO: importa do app_old"""

from flask import Blueprint
import sys
from pathlib import Path

# Importar temporariamente do app_old.py
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app_old import app as old_app

bp = Blueprint('dashboard', __name__)

# Registrar rotas do app_old temporariamente
@bp.route('/')
def index():
    """Dashboard principal - temporário"""
    from app_old import index as old_index
    return old_index()

