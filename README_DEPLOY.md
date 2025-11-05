# 🚀 Deploy - Guia Rápido

## Opção 1: Script Automatizado (Mais Fácil)

### Linux/Mac:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Windows:
```cmd
deploy.bat
```

**Pronto!** Acesse: `http://localhost:5001`

---

## Opção 2: Manual (3 Comandos)

```bash
# 1. Criar arquivo .env (edite com suas configurações)
cp .env.example .env
nano .env

# 2. Fazer deploy
docker-compose up -d --build

# 3. Abrir firewall (se necessário)
sudo ufw allow 5001/tcp
```

---

## 📝 Configuração (.env)

Crie o arquivo `.env`:

```env
SECRET_KEY=sua-chave-secreta-aqui
DASHBOARD_PASSWORD=sua-senha-forte
```

**Gerar SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🔥 Acesso Externo

Se não conseguir acessar de fora do servidor:

```bash
sudo ufw allow 5001/tcp
```

Depois acesse: `http://IP_DO_SERVIDOR:5001`

---

## 📊 Comandos Úteis

```bash
# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Reiniciar
docker-compose restart

# Ver status
docker-compose ps
```

---

**Pronto!** 🎉

