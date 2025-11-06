"""
Funções de banco de dados
"""

import sqlite3
from pathlib import Path

# Este arquivo será preenchido com a função init_db completa do app.py
# Por enquanto, vamos importar diretamente do app.py para manter funcionando

def init_db(db_path):
    """Inicializa o banco de dados com as tabelas necessárias"""
    # Importar a função do app.py original temporariamente
    # Depois vamos mover todo o código aqui
    from app import init_db as original_init_db
    original_init_db(db_path)

