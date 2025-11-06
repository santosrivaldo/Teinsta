#!/usr/bin/env python3
"""
Script para sincronizar dados entre desenvolvimento e produção
Exporta/importa banco de dados e uploads

Uso:
  # Exportar dados do ambiente local
  python sync_data.py export --output backup_completo.tar.gz
  
  # Importar dados no ambiente de produção (Docker)
  python sync_data.py import --input backup_completo.tar.gz
  
  # Sincronizar tudo (exportar do dev e importar no prod via SSH)
  python sync_data.py sync --host usuario@servidor-producao --path /caminho/do/projeto
"""

import sqlite3
import os
import sys
import tarfile
import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Tentar carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configurações
data_dir = Path(os.environ.get('DATA_DIR', '.'))
if not data_dir.exists():
    data_dir = Path('.')

# Tentar encontrar banco em vários locais
def find_db_file():
    possible_paths = [
        Path('iso27001.db'),
        data_dir / 'iso27001.db',
        Path('data/iso27001.db'),
        Path('./data/iso27001.db'),
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

DB_FILE_FOUND = find_db_file()
DB_PATH = DB_FILE_FOUND if DB_FILE_FOUND else (data_dir / 'iso27001.db')

UPLOADS_DIR = data_dir / 'uploads'
if not UPLOADS_DIR.exists():
    UPLOADS_DIR = Path('uploads')
    if not UPLOADS_DIR.exists():
        UPLOADS_DIR = Path('.')

def export_data(output_file):
    """Exporta banco de dados e uploads para um arquivo tar.gz"""
    print(f"📦 Exportando dados...")
    
    # Verificar se os arquivos existem
    files_to_export = []
    if DB_PATH.exists():
        files_to_export.append(('iso27001.db', DB_PATH))
        print(f"  ✓ Banco de dados encontrado: {DB_PATH}")
    else:
        alt_db = Path('iso27001.db')
        if alt_db.exists():
            files_to_export.append(('iso27001.db', alt_db))
            print(f"  ✓ Banco de dados encontrado: {alt_db}")
        else:
            print(f"  ⚠ Banco de dados não encontrado em {DB_PATH} ou ./iso27001.db")
    
    if UPLOADS_DIR.exists() and any(UPLOADS_DIR.iterdir()):
        files_to_export.append(('uploads', UPLOADS_DIR))
        file_count = sum(1 for _ in UPLOADS_DIR.rglob('*') if _.is_file())
        print(f"  ✓ Uploads encontrados: {file_count} arquivos em {UPLOADS_DIR}")
    else:
        print(f"  ⚠ Nenhum arquivo de upload encontrado")
    
    if not files_to_export:
        print("❌ Nenhum dado para exportar!")
        return False
    
    # Criar arquivo tar.gz
    output_path = Path(output_file)
    with tarfile.open(output_path, 'w:gz') as tar:
        for name, path in files_to_export:
            if path.is_file():
                tar.add(path, arcname=name)
                print(f"  ✓ Adicionado: {name}")
            elif path.is_dir():
                tar.add(path, arcname=name, recursive=True)
                print(f"  ✓ Adicionado: {name}/ (diretório)")
    
    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"\n✅ Exportação concluída: {output_path} ({size_mb:.2f} MB)")
    return True

def import_data(input_file):
    """Importa banco de dados e uploads de um arquivo tar.gz"""
    print(f"📥 Importando dados de {input_file}...")
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Arquivo não encontrado: {input_path}")
        return False
    
    # Criar backup antes de importar
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if DB_PATH.exists():
        backup_db = backup_dir / f'iso27001_backup_{timestamp}.db'
        shutil.copy2(DB_PATH, backup_db)
        print(f"  ✓ Backup criado: {backup_db}")
    
    # Extrair arquivos
    with tarfile.open(input_path, 'r:gz') as tar:
        members = tar.getmembers()
        print(f"  📋 Encontrados {len(members)} arquivos/diretórios")
        
        for member in members:
            print(f"  ✓ Extraindo: {member.name}")
            tar.extract(member, path=data_dir)
    
    # Mover arquivos para locais corretos se necessário
    extracted_db = data_dir / 'iso27001.db'
    if extracted_db.exists() and extracted_db != DB_PATH:
        if DB_PATH.exists():
            DB_PATH.unlink()
        shutil.move(extracted_db, DB_PATH)
        print(f"  ✓ Banco de dados movido para: {DB_PATH}")
    
    extracted_uploads = data_dir / 'uploads'
    if extracted_uploads.exists() and extracted_uploads != UPLOADS_DIR:
        if UPLOADS_DIR.exists():
            shutil.rmtree(UPLOADS_DIR)
        shutil.move(extracted_uploads, UPLOADS_DIR)
        print(f"  ✓ Uploads movidos para: {UPLOADS_DIR}")
    
    print(f"\n✅ Importação concluída!")
    print(f"   Banco de dados: {DB_PATH}")
    print(f"   Uploads: {UPLOADS_DIR}")
    return True

def sync_to_production(host, path):
    """Sincroniza dados do desenvolvimento para produção via SSH"""
    print(f"🔄 Sincronizando dados para produção...")
    print(f"   Host: {host}")
    print(f"   Path: {path}")
    
    # Exportar dados localmente
    temp_file = Path(f'sync_temp_{datetime.now().strftime("%Y%m%d_%H%M%S")}.tar.gz')
    if not export_data(temp_file):
        print("❌ Falha ao exportar dados localmente")
        return False
    
    try:
        # Copiar para servidor
        print(f"\n📤 Enviando para servidor...")
        import subprocess
        remote_file = f"{host}:{path}/sync_data.tar.gz"
        result = subprocess.run(
            ['scp', str(temp_file), remote_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Erro ao copiar arquivo: {result.stderr}")
            return False
        
        print(f"  ✓ Arquivo copiado para servidor")
        
        # Importar no servidor
        print(f"\n📥 Importando no servidor...")
        result = subprocess.run(
            ['ssh', host, f'cd {path} && python3 sync_data.py import --input sync_data.tar.gz && docker-compose restart web'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ Erro ao importar no servidor: {result.stderr}")
            return False
        
        print(f"  ✓ Dados importados e container reiniciado")
        
    finally:
        # Limpar arquivo temporário
        if temp_file.exists():
            temp_file.unlink()
            print(f"\n  🗑️  Arquivo temporário removido")
    
    print(f"\n✅ Sincronização concluída!")
    return True

def main():
    parser = argparse.ArgumentParser(description='Sincronizar dados entre dev e produção')
    subparsers = parser.add_subparsers(dest='command', help='Comando a executar')
    
    # Exportar
    export_parser = subparsers.add_parser('export', help='Exportar dados do ambiente local')
    export_parser.add_argument('--output', '-o', default='backup_completo.tar.gz',
                             help='Arquivo de saída (padrão: backup_completo.tar.gz)')
    
    # Importar
    import_parser = subparsers.add_parser('import', help='Importar dados no ambiente atual')
    import_parser.add_argument('--input', '-i', required=True,
                             help='Arquivo de entrada (.tar.gz)')
    
    # Sincronizar
    sync_parser = subparsers.add_parser('sync', help='Sincronizar dados para produção via SSH')
    sync_parser.add_argument('--host', required=True,
                           help='Host SSH (ex: usuario@servidor.com)')
    sync_parser.add_argument('--path', required=True,
                           help='Caminho do projeto no servidor (ex: /home/user/Teinsta)')
    
    args = parser.parse_args()
    
    if args.command == 'export':
        export_data(args.output)
    elif args.command == 'import':
        import_data(args.input)
    elif args.command == 'sync':
        sync_to_production(args.host, args.path)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

