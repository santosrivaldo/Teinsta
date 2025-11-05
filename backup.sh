#!/bin/bash
# Script de backup do banco de dados ISO 27001

# Configurações
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DB_PATH="${DB_PATH:-./iso27001.db}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

# Criar diretório de backup se não existir
mkdir -p "$BACKUP_DIR"

# Nome do arquivo de backup com data/hora
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/iso27001_$TIMESTAMP.db"

# Verificar se o banco de dados existe
if [ ! -f "$DB_PATH" ]; then
    echo "Erro: Banco de dados não encontrado em $DB_PATH"
    exit 1
fi

# Fazer backup
echo "Fazendo backup do banco de dados..."
cp "$DB_PATH" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup criado com sucesso: $BACKUP_FILE"
    
    # Remover backups antigos (mais de RETENTION_DAYS dias)
    echo "Removendo backups antigos (mais de $RETENTION_DAYS dias)..."
    find "$BACKUP_DIR" -name "iso27001_*.db" -mtime +$RETENTION_DAYS -delete
    
    echo "Backup concluído!"
else
    echo "Erro ao criar backup"
    exit 1
fi

