#!/usr/bin/env python3
"""
Script para inicializar banco de dados no Docker
Cria um banco de dados inicial com dados de exemplo
"""

import sqlite3
import sys
from pathlib import Path

def init_db_initial(db_path):
    """Inicializa banco de dados inicial"""
    # Importar função do app.py
    sys.path.insert(0, str(Path(__file__).parent))
    from app import init_db
    
    # Criar diretório se não existir
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Inicializar banco
    init_db(db_path)
    print(f"Banco de dados inicializado: {db_path}")

if __name__ == '__main__':
    db_path = Path('/app/data/iso27001.db')
    if len(sys.argv) > 1:
        db_path = Path(sys.argv[1])
    init_db_initial(db_path)

