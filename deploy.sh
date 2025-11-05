#!/bin/bash
# Script de deploy simplificado

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy do Sistema ISO 27001..."
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "📝 Criando arquivo .env com valores padrão..."
    echo ""
    cat > .env << EOF
# Configurações de Segurança
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
DASHBOARD_PASSWORD=admin123

# Ambiente
FLASK_ENV=production
EOF
    echo "✅ Arquivo .env criado!"
    echo "⚠️  IMPORTANTE: Altere a senha padrão em .env antes de usar em produção!"
    echo ""
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data uploads
chmod 755 data uploads

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado!"
    echo "Instale com: curl -fsSL https://get.docker.com | sh"
    exit 1
fi

# Verificar se docker-compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose não está instalado!"
    echo "Instale com: sudo apt install docker-compose"
    exit 1
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down 2>/dev/null || true

# Construir e iniciar
echo "🔨 Construindo imagem..."
docker-compose build

echo "🚀 Iniciando container..."
docker-compose up -d

# Aguardar alguns segundos
echo "⏳ Aguardando aplicação iniciar..."
sleep 5

# Verificar status
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Deploy concluído com sucesso!"
    echo ""
    echo "📊 Status:"
    docker-compose ps
    echo ""
    
    # Obter IP do servidor
    SERVER_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")
    
    echo "🌐 Acesse a aplicação em:"
    echo "   http://$SERVER_IP:5001"
    echo "   ou"
    echo "   http://localhost:5001"
    echo ""
    echo "🔐 Senha: (veja no arquivo .env - DASHBOARD_PASSWORD)"
    echo ""
    echo "📝 Ver logs: docker-compose logs -f"
    echo "🛑 Parar: docker-compose down"
else
    echo ""
    echo "❌ Erro ao iniciar container!"
    echo "📋 Ver logs: docker-compose logs"
    exit 1
fi

