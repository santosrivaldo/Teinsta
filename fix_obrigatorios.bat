@echo off
REM Script para corrigir controles - marcar todos como boas práticas

echo 🔧 Corrigindo controles no banco de dados...

REM Se estiver usando Docker
if exist docker-compose.yml (
    echo Executando no container Docker...
    docker-compose exec web python fix_obrigatorios.py
) else (
    echo Executando localmente...
    python fix_obrigatorios.py
)

echo ✅ Concluído!

