# 🚀 Deploy Simplificado - 3 Passos

## Passo 1: Configurar Senha (1 minuto)

```bash
nano .env
```

Adicione:
```
SECRET_KEY=sua-chave-secreta-aqui
DASHBOARD_PASSWORD=sua-senha-forte
```

**Dica:** Para gerar uma SECRET_KEY segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Passo 2: Fazer Deploy (1 comando)

```bash
./deploy.sh
```

Ou se não tiver permissão:
```bash
bash deploy.sh
```

## Passo 3: Acessar

Abra no navegador: `http://SEU_IP:5001`

Senha: a que você configurou no `.env`

---

## 🔥 Abrir Firewall (Apenas 1 vez)

```bash
sudo ufw allow 5001/tcp
```

---

## 📝 Comandos Úteis

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

## ❓ Problemas?

1. **Container não inicia?** → Ver logs: `docker-compose logs`
2. **Acesso externo não funciona?** → Abrir firewall: `sudo ufw allow 5001/tcp`
3. **Erro de build?** → Ver conexão com internet do servidor
4. **Todos os controles como obrigatórios?** → Execute: `bash fix_obrigatorios.sh` (ou `fix_obrigatorios.bat` no Windows)

---

**Pronto! É só isso!** 🎉

