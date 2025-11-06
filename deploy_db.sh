#!/bin/bash
# Script para copiar banco de dados para produção via SSH

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploy de Banco de Dados para Produção${NC}"
echo ""

# Verificar argumentos
if [ "$#" -lt 2 ]; then
    echo -e "${RED}Uso: $0 <usuario@servidor> <caminho_no_servidor>${NC}"
    echo ""
    echo "Exemplo:"
    echo "  $0 root@192.168.1.100 /root/Teinsta"
    exit 1
fi

SERVER="$1"
SERVER_PATH="$2"

echo -e "${YELLOW}Servidor:${NC} $SERVER"
echo -e "${YELLOW}Caminho:${NC} $SERVER_PATH"
echo ""

# 1. Encontrar banco local
echo "📋 Procurando banco de dados local..."
if [ -f "iso27001.db" ]; then
    DB_FILE="iso27001.db"
elif [ -f "data/iso27001.db" ]; then
    DB_FILE="data/iso27001.db"
else
    echo -e "${RED}❌ Banco de dados não encontrado!${NC}"
    echo "   Procurou em: ./iso27001.db e ./data/iso27001.db"
    exit 1
fi

echo -e "${GREEN}✅ Encontrado: $DB_FILE${NC}"
DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
echo "   Tamanho: $DB_SIZE"

# 2. Verificar banco
echo ""
echo "🔍 Verificando banco de dados..."
python3 -c "
import sqlite3
conn = sqlite3.connect('$DB_FILE')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM controles')
controles = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM modulos')
modulos = c.fetchone()[0]
conn.close()
print(f'   Controles: {controles}')
print(f'   Módulos: {modulos}')
" || python -c "
import sqlite3
conn = sqlite3.connect('$DB_FILE')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM controles')
controles = c.fetchone()[0]
c.execute('SELECT COUNT(*) FROM modulos')
modulos = c.fetchone()[0]
conn.close()
print(f'   Controles: {controles}')
print(f'   Módulos: {modulos}')
"

# 3. Criar backup no servidor
echo ""
echo "💾 Criando backup no servidor..."
ssh "$SERVER" "cd $SERVER_PATH && docker-compose exec -T web python -c \"
import sqlite3
from pathlib import Path
from datetime import datetime
import shutil

data_dir = Path('/app/data')
db_path = data_dir / 'iso27001.db'
if db_path.exists():
    backup_path = data_dir / f'iso27001_backup_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.db'
    shutil.copy2(db_path, backup_path)
    print(f'Backup criado: {backup_path.name}')
else:
    print('Banco não encontrado (primeira vez)')
\""

# 4. Copiar banco para servidor
echo ""
echo "📤 Copiando banco para servidor..."
scp "$DB_FILE" "$SERVER:$SERVER_PATH/iso27001_new.db"

# 5. Substituir banco no container
echo ""
echo "🔄 Substituindo banco no container..."
ssh "$SERVER" "cd $SERVER_PATH && \
    docker cp iso27001_new.db \$(docker-compose ps -q web):/app/data/iso27001.db && \
    rm iso27001_new.db && \
    docker-compose restart web"

# 6. Verificar
echo ""
echo "✅ Verificando..."
sleep 3
ssh "$SERVER" "cd $SERVER_PATH && docker-compose logs --tail=10 web"

echo ""
echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo ""
echo "Acesse: http://$SERVER:5001"


