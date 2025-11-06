#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para copiar banco de dados de dev para produção
Copia EXATAMENTE o banco atual, mantendo todos os dados
"""

import sqlite3
import shutil
import sys
import os
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def find_db_file():
    """Encontra o arquivo de banco de dados"""
    possible_paths = [
        Path('iso27001.db'),
        Path('data/iso27001.db'),
        Path('./data/iso27001.db'),
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def verify_db(db_path):
    """Verifica se o banco está válido e mostra estatísticas"""
    try:
        conn = sqlite3.connect(str(db_path))
        c = conn.cursor()
        
        # Contar registros em cada tabela
        tables = {
            'controles': 'SELECT COUNT(*) FROM controles',
            'normas': 'SELECT COUNT(*) FROM normas',
            'politicas': 'SELECT COUNT(*) FROM politicas',
            'modulos': 'SELECT COUNT(*) FROM modulos',
            'nao_conformidades': 'SELECT COUNT(*) FROM nao_conformidades',
            'auditorias': 'SELECT COUNT(*) FROM auditorias',
        }
        
        print(f"\n[STATS] Estatisticas do banco: {db_path}")
        print("-" * 50)
        
        total_records = 0
        for table, query in tables.items():
            try:
                c.execute(query)
                count = c.fetchone()[0]
                total_records += count
                print(f"  {table:20s}: {count:4d} registros")
            except sqlite3.OperationalError:
                print(f"  {table:20s}: tabela nao existe")
        
        print("-" * 50)
        print(f"  Total aproximado: {total_records} registros")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")
        return False

def copy_to_production(local_db, output_file='iso27001_prod.db'):
    """Copia o banco de dados para arquivo"""
    print(f"\n[COPIANDO] Banco de dados...")
    print(f"   Origem: {local_db}")
    print(f"   Destino: {output_file}")
    
    try:
        # Verificar tamanho
        size_mb = local_db.stat().st_size / (1024 * 1024)
        print(f"   Tamanho: {size_mb:.2f} MB")
        
        # Copiar arquivo
        shutil.copy2(local_db, output_file)
        
        # Verificar se copiou corretamente
        if Path(output_file).exists():
            print(f"\n[OK] Banco copiado com sucesso!")
            print(f"   Arquivo: {output_file}")
            return True
        else:
            print(f"[ERRO] Arquivo nao foi criado")
            return False
            
    except Exception as e:
        print(f"[ERRO] Erro ao copiar: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("[SINCRONIZAR] COPIAR BANCO DE DADOS - DEV -> PRODUCAO")
    print("=" * 60)
    
    # Encontrar banco local
    db_file = find_db_file()
    
    if not db_file:
        print("\n[ERRO] Banco de dados nao encontrado!")
        print("\nProcurou em:")
        print("  - ./iso27001.db")
        print("  - ./data/iso27001.db")
        print("\nCertifique-se de estar no diretorio correto do projeto.")
        sys.exit(1)
    
    print(f"\n[OK] Banco encontrado: {db_file}")
    
    # Verificar banco
    if not verify_db(db_file):
        sys.exit(1)
    
    # Copiar
    output_file = 'iso27001_prod.db'
    if copy_to_production(db_file, output_file):
        print("\n" + "=" * 60)
        print("[PROXIMOS PASSOS]")
        print("=" * 60)
        print(f"\n1. Transferir '{output_file}' para o servidor de produção:")
        print(f"   scp {output_file} usuario@servidor:/caminho/do/projeto/")
        print(f"\n2. No servidor, substituir o banco:")
        print(f"   ssh usuario@servidor")
        print(f"   cd /caminho/do/projeto")
        print(f"   docker-compose stop web")
        print(f"   cp iso27001_prod.db data/iso27001.db")
        print(f"   docker-compose start web")
        print(f"\n   OU dentro do container:")
        print(f"   docker cp iso27001_prod.db $(docker-compose ps -q web):/app/data/iso27001.db")
        print(f"   docker-compose restart web")
        print("\n" + "=" * 60)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

