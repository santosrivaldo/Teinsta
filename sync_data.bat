@echo off
REM Script para sincronizar dados no Windows

echo 🔄 Sincronização de Dados - ISO 27001
echo.

REM Verificar se está usando Docker
docker ps | findstr teinsta_web >nul 2>&1
if %errorlevel% equ 0 (
    set USE_DOCKER=true
    echo ℹ️  Docker detectado
) else (
    set USE_DOCKER=false
)

REM Função para exportar
if "%1"=="export" (
    echo 📦 Exportando dados...
    
    if "%USE_DOCKER%"=="true" (
        REM Exportar do container
        docker-compose exec -T web python sync_data.py export --output /tmp/sync_data.tar.gz
        docker cp teinsta_web_1:/tmp/sync_data.tar.gz backup_completo.tar.gz
        docker-compose exec -T web rm /tmp/sync_data.tar.gz
    ) else (
        REM Exportar localmente
        python sync_data.py export --output backup_completo.tar.gz
    )
    
    echo ✅ Exportação concluída: backup_completo.tar.gz
    goto :end
)

REM Função para importar
if "%1"=="import" (
    if "%2"=="" (
        echo ❌ Especifique o arquivo: %0 import arquivo.tar.gz
        exit /b 1
    )
    
    if not exist "%2" (
        echo ❌ Arquivo não encontrado: %2
        exit /b 1
    )
    
    echo 📥 Importando dados de %2...
    
    if "%USE_DOCKER%"=="true" (
        REM Copiar para container
        docker cp "%2" teinsta_web_1:/tmp/sync_data.tar.gz
        REM Importar no container
        docker-compose exec -T web python sync_data.py import --input /tmp/sync_data.tar.gz
        docker-compose exec -T web rm /tmp/sync_data.tar.gz
        REM Reiniciar container
        docker-compose restart web
    ) else (
        REM Importar localmente
        python sync_data.py import --input "%2"
    )
    
    echo ✅ Importação concluída!
    goto :end
)

REM Menu de ajuda
echo Uso: %0 {export^|import [arquivo.tar.gz]}
echo.
echo Exemplos:
echo   %0 export                    # Exportar dados do ambiente atual
echo   %0 import backup.tar.gz      # Importar dados no ambiente atual
exit /b 1

:end

