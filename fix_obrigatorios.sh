#!/bin/bash
# Script para corrigir controles - marcar todos como boas práticas

echo "🔧 Corrigindo controles no banco de dados..."

# Se estiver usando Docker
if command -v docker-compose &> /dev/null && [ -f docker-compose.yml ]; then
    echo "Executando no container Docker..."
    docker-compose exec web python fix_obrigatorios.py
elif command -v docker &> /dev/null && docker ps | grep -q teinsta_web; then
    echo "Executando no container Docker (usando docker exec)..."
    docker exec teinsta_web_1 python fix_obrigatorios.py
else
    echo "Executando localmente..."
    python3 fix_obrigatorios.py || python fix_obrigatorios.py
fi

echo "✅ Concluído!"

