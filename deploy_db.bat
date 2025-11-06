@echo off
REM Script para copiar banco de dados para produção

echo 🚀 Deploy de Banco de Dados para Produção
echo.

REM Verificar argumentos
if "%1"=="" (
    echo ❌ Uso: %0 usuario@servidor caminho_no_servidor
    echo.
    echo Exemplo:
    echo   %0 root@192.168.1.100 /root/Teinsta
    exit /b 1
)

if "%2"=="" (
    echo ❌ Caminho no servidor não especificado
    exit /b 1
)

set SERVER=%1
set SERVER_PATH=%2

echo Servidor: %SERVER%
echo Caminho: %SERVER_PATH%
echo.

REM 1. Encontrar banco local
echo 📋 Procurando banco de dados local...
if exist "iso27001.db" (
    set DB_FILE=iso27001.db
) else if exist "data\iso27001.db" (
    set DB_FILE=data\iso27001.db
) else (
    echo ❌ Banco de dados não encontrado!
    echo    Procurou em: .\iso27001.db e .\data\iso27001.db
    exit /b 1
)

echo ✅ Encontrado: %DB_FILE%

REM 2. Verificar banco
echo.
echo 🔍 Verificando banco de dados...
python -c "import sqlite3; conn = sqlite3.connect('%DB_FILE%'); c = conn.cursor(); c.execute('SELECT COUNT(*) FROM controles'); print('Controles:', c.fetchone()[0]); c.execute('SELECT COUNT(*) FROM modulos'); print('Módulos:', c.fetchone()[0]); conn.close()"

REM 3. Criar backup no servidor
echo.
echo 💾 Criando backup no servidor...
ssh %SERVER% "cd %SERVER_PATH% && docker-compose exec -T web python -c \"import sqlite3; from pathlib import Path; from datetime import datetime; import shutil; data_dir = Path('/app/data'); db_path = data_dir / 'iso27001.db'; backup_path = data_dir / ('iso27001_backup_' + datetime.now().strftime('%%Y%%m%%d_%%H%%M%%S') + '.db') if db_path.exists() else None; shutil.copy2(db_path, backup_path) if backup_path else None; print('Backup criado' if backup_path else 'Banco não encontrado')\""

REM 4. Copiar banco para servidor
echo.
echo 📤 Copiando banco para servidor...
scp %DB_FILE% %SERVER%:%SERVER_PATH%/iso27001_new.db

REM 5. Substituir banco no container
echo.
echo 🔄 Substituindo banco no container...
ssh %SERVER% "cd %SERVER_PATH% && docker cp iso27001_new.db $(docker-compose ps -q web):/app/data/iso27001.db && rm iso27001_new.db && docker-compose restart web"

REM 6. Verificar
echo.
echo ✅ Verificando...
timeout /t 3 /nobreak >nul
ssh %SERVER% "cd %SERVER_PATH% && docker-compose logs --tail=10 web"

echo.
echo ✅ Deploy concluído!
echo.
echo Acesse: http://%SERVER%:5001


