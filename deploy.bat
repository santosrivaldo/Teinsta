@echo off
REM Script de deploy simplificado para Windows

echo 🚀 Iniciando deploy do Sistema ISO 27001...
echo.

REM Verificar se .env existe
if not exist .env (
    echo ⚠️  Arquivo .env não encontrado!
    echo 📝 Criando arquivo .env com valores padrão...
    echo.
    (
        echo # Configurações de Segurança
        echo SECRET_KEY=change-this-in-production
        echo DASHBOARD_PASSWORD=admin123
        echo.
        echo # Ambiente
        echo FLASK_ENV=production
    ) > .env
    echo ✅ Arquivo .env criado!
    echo ⚠️  IMPORTANTE: Altere a senha padrão em .env antes de usar em produção!
    echo.
)

REM Criar diretórios necessários
echo 📁 Criando diretórios...
if not exist data mkdir data
if not exist uploads mkdir uploads

REM Verificar se Docker está instalado
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker não está instalado!
    echo Instale Docker Desktop: https://www.docker.com/products/docker-desktop
    exit /b 1
)

REM Parar containers existentes
echo 🛑 Parando containers existentes...
docker-compose down 2>nul

REM Construir e iniciar
echo 🔨 Construindo imagem...
docker-compose build
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao construir imagem!
    exit /b 1
)

echo 🚀 Iniciando container...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao iniciar container!
    exit /b 1
)

REM Aguardar alguns segundos
echo ⏳ Aguardando aplicação iniciar...
timeout /t 5 /nobreak >nul

REM Verificar status
docker-compose ps | findstr "Up" >nul
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Deploy concluído com sucesso!
    echo.
    echo 📊 Status:
    docker-compose ps
    echo.
    echo 🌐 Acesse a aplicação em: http://localhost:5001
    echo.
    echo 🔐 Senha: (veja no arquivo .env - DASHBOARD_PASSWORD)
    echo.
    echo 📝 Ver logs: docker-compose logs -f
    echo 🛑 Parar: docker-compose down
) else (
    echo.
    echo ❌ Erro ao iniciar container!
    echo 📋 Ver logs: docker-compose logs
    exit /b 1
)

