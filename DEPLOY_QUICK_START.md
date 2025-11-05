# Guia Rápido de Deploy - Docker

## ✅ Status: Container criado com sucesso!

O container foi criado, mas parece ter parado. Vamos verificar e corrigir:

## 🔍 Verificações

### 1. Verificar status do container:
```bash
docker-compose ps
```

### 2. Ver logs completos:
```bash
docker-compose logs --tail=100
```

### 3. Verificar se o container está rodando:
```bash
docker ps -a | grep teinsta
```

## 🚀 Iniciar o container

Se o container não estiver rodando, inicie com:

```bash
docker-compose up -d
```

O flag `-d` roda em modo detached (background).

## ⚙️ Configurar Variáveis de Ambiente

**IMPORTANTE:** Antes de usar em produção, configure as variáveis de ambiente:

1. **Criar arquivo `.env` na raiz do projeto:**
```bash
nano .env
```

2. **Adicionar as seguintes variáveis:**
```env
SECRET_KEY=sua-chave-secreta-muito-longa-e-aleatoria-aqui
DASHBOARD_PASSWORD=sua-senha-forte-aqui
```

3. **Salvar e reiniciar o container:**
```bash
docker-compose down
docker-compose up -d
```

## 🌐 Acessar a aplicação

Após iniciar o container, acesse:

- **Local:** http://localhost:6000
- **Rede:** http://IP_DO_SERVIDOR:6000

**Login:** Use a senha configurada em `DASHBOARD_PASSWORD` (padrão: `admin123`)

## 📊 Comandos úteis

### Ver logs em tempo real:
```bash
docker-compose logs -f
```

### Parar o container:
```bash
docker-compose down
```

### Reiniciar o container:
```bash
docker-compose restart
```

### Rebuild da imagem (após mudanças no código):
```bash
docker-compose up --build -d
```

### Entrar no container:
```bash
docker-compose exec web bash
```

### Verificar uso de recursos:
```bash
docker stats teinsta_web_1
```

## 🔧 Troubleshooting

### Container para imediatamente:
- Verifique os logs: `docker-compose logs`
- Verifique se a porta 6000 está disponível
- Verifique permissões dos volumes

### Erro de permissão:
```bash
sudo chown -R $USER:$USER data/ uploads/
```

### Banco de dados não persiste:
- Verifique se o volume `./data:/app/data` está montado no docker-compose.yml
- Verifique se o diretório `data/` existe e tem permissões

### Aplicação não responde:
- Verifique firewall: `sudo ufw allow 6000`
- Verifique se o container está rodando: `docker-compose ps`
- Teste localmente: `curl http://localhost:6000/login`

## 🔒 Segurança para Produção

Antes de colocar em produção:

1. ✅ Altere `SECRET_KEY` para uma chave forte e aleatória
2. ✅ Altere `DASHBOARD_PASSWORD` para uma senha forte
3. ✅ Configure HTTPS (use nginx como reverse proxy)
4. ✅ Configure firewall adequadamente
5. ✅ Configure backups automáticos do banco de dados
6. ✅ Configure monitoramento e alertas

## 📝 Próximos Passos

1. Configure variáveis de ambiente (`.env`)
2. Teste a aplicação localmente
3. Configure nginx como reverse proxy (opcional)
4. Configure SSL/HTTPS (opcional mas recomendado)
5. Configure backups automáticos

## 🆘 Precisa de ajuda?

Consulte o guia completo em `DEPLOY.md` para mais opções de deploy.

