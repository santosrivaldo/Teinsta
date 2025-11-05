#!/usr/bin/env python3
"""
Script para corrigir controles existentes - marcar todos como boas práticas
Execute este script uma vez para atualizar o banco de dados existente

Uso:
  python fix_obrigatorios.py
  # ou no Docker:
  docker-compose exec web python fix_obrigatorios.py
"""

import sqlite3
import os
import sys
from pathlib import Path

# Tentar carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configurações de arquivos
data_dir = Path(os.environ.get('DATA_DIR', '.'))
# Se não existir, tentar diretório atual
if not data_dir.exists():
    data_dir = Path('.')
data_dir.mkdir(exist_ok=True)

DB_PATH = data_dir / 'iso27001.db'

def fix_obrigatorios():
    """Atualiza todos os controles para boas práticas (obrigatorio = 0)"""
    if not DB_PATH.exists():
        print(f"❌ Banco de dados não encontrado em: {DB_PATH}")
        print(f"   Tentando localizar em outros locais...")
        # Tentar outros caminhos comuns
        alt_paths = [
            Path('iso27001.db'),
            Path('data/iso27001.db'),
            Path('/app/data/iso27001.db'),
            Path('/app/iso27001.db'),
        ]
        for alt_path in alt_paths:
            if alt_path.exists():
                global DB_PATH
                DB_PATH = alt_path
                print(f"✅ Encontrado em: {DB_PATH}")
                break
        else:
            sys.exit(1)
    
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    
    # Verificar quantos estão como obrigatórios
    c.execute('SELECT COUNT(*) FROM controles WHERE obrigatorio = 1')
    total_obrigatorios = c.fetchone()[0]
    
    if total_obrigatorios == 0:
        print("ℹ️  Nenhum controle marcado como obrigatório. Nada a fazer.")
        conn.close()
        return
    
    # Atualizar todos os controles para boas práticas
    c.execute('''
        UPDATE controles 
        SET obrigatorio = 0 
        WHERE obrigatorio = 1
    ''')
    
    updated = c.rowcount
    conn.commit()
    conn.close()
    
    print(f"✅ {updated} controles atualizados para 'Boas Práticas'")
    print("Agora você pode marcar manualmente quais são obrigatórios através da interface.")

if __name__ == '__main__':
    print(f"🔧 Atualizando controles...")
    print(f"   Procurando banco em: {DB_PATH}")
    fix_obrigatorios()

