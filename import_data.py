#!/usr/bin/env python3
"""
Script para importar dados padrão no banco de dados
Pode ser executado manualmente ou automaticamente no início do app
"""

import sys
import os
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

# Tentar carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def main():
    """Importa dados padrão no banco"""
    from app.utils.seed_data import import_default_data
    
    # Determinar caminho do banco
    data_dir = Path(os.environ.get('DATA_DIR', '.'))
    db_path = data_dir / 'iso27001.db'
    
    if not db_path.exists():
        print(f"❌ Banco de dados não encontrado: {db_path}")
        print("   Execute primeiro: python app.py (para criar o banco)")
        sys.exit(1)
    
    print(f"📦 Importando dados padrão...")
    print(f"   Banco: {db_path}")
    
    try:
        import_default_data(db_path)
        print("\n✅ Dados importados com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao importar dados: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

