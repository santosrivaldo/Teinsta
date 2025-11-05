#!/bin/bash
# Script simplificado para sincronizar dados

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Sincronização de Dados - ISO 27001${NC}"
echo ""

# Verificar se está usando Docker
USE_DOCKER=false
if [ -f docker-compose.yml ] && docker ps | grep -q teinsta_web; then
    USE_DOCKER=true
    echo -e "${YELLOW}ℹ️  Docker detectado${NC}"
fi

# Função para exportar
export_data() {
    echo -e "${GREEN}📦 Exportando dados...${NC}"
    
    if [ "$USE_DOCKER" = true ]; then
        # Exportar do container
        docker-compose exec -T web python sync_data.py export --output /tmp/sync_data.tar.gz
        docker cp $(docker-compose ps -q web):/tmp/sync_data.tar.gz ./backup_completo.tar.gz
        docker-compose exec -T web rm /tmp/sync_data.tar.gz
    else
        # Exportar localmente
        python3 sync_data.py export --output backup_completo.tar.gz || python sync_data.py export --output backup_completo.tar.gz
    fi
    
    echo -e "${GREEN}✅ Exportação concluída: backup_completo.tar.gz${NC}"
}

# Função para importar
import_data() {
    if [ ! -f "$1" ]; then
        echo -e "${RED}❌ Arquivo não encontrado: $1${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}📥 Importando dados de $1...${NC}"
    
    if [ "$USE_DOCKER" = true ]; then
        # Copiar para container
        docker cp "$1" $(docker-compose ps -q web):/tmp/sync_data.tar.gz
        # Importar no container
        docker-compose exec -T web python sync_data.py import --input /tmp/sync_data.tar.gz
        docker-compose exec -T web rm /tmp/sync_data.tar.gz
        # Reiniciar container
        docker-compose restart web
    else
        # Importar localmente
        python3 sync_data.py import --input "$1" || python sync_data.py import --input "$1"
    fi
    
    echo -e "${GREEN}✅ Importação concluída!${NC}"
}

# Menu
case "$1" in
    export)
        export_data
        ;;
    import)
        if [ -z "$2" ]; then
            echo -e "${RED}❌ Especifique o arquivo: $0 import arquivo.tar.gz${NC}"
            exit 1
        fi
        import_data "$2"
        ;;
    *)
        echo "Uso: $0 {export|import [arquivo.tar.gz]}"
        echo ""
        echo "Exemplos:"
        echo "  $0 export                    # Exportar dados do ambiente atual"
        echo "  $0 import backup.tar.gz      # Importar dados no ambiente atual"
        exit 1
        ;;
esac

