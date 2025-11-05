@echo off
REM Script de backup do banco de dados ISO 27001 para Windows

REM Configurações
set BACKUP_DIR=backups
set DB_PATH=iso27001.db
set RETENTION_DAYS=30

REM Criar diretório de backup se não existir
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Verificar se o banco de dados existe
if not exist "%DB_PATH%" (
    echo Erro: Banco de dados não encontrado em %DB_PATH%
    exit /b 1
)

REM Nome do arquivo de backup com data/hora
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%
set BACKUP_FILE=%BACKUP_DIR%\iso27001_%TIMESTAMP%.db

REM Fazer backup
echo Fazendo backup do banco de dados...
copy "%DB_PATH%" "%BACKUP_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Backup criado com sucesso: %BACKUP_FILE%
    echo.
    echo Nota: Remoção automática de backups antigos não suportada no Windows.
    echo Por favor, remova manualmente backups com mais de %RETENTION_DAYS% dias.
    echo.
) else (
    echo Erro ao criar backup
    exit /b 1
)

