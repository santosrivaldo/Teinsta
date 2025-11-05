# Troubleshooting: Acesso Externo Não Funciona

**NOTA:** A aplicação usa a porta **3000** (não 6000) para evitar bloqueio de navegadores.

## ✅ Verificações Rápidas

### 1. Verificar se o container está rodando e escutando
```bash
docker-compose ps
netstat -tlnp | grep 3000
# ou
ss -tlnp | grep 3000
```

### 2. Testar localmente no servidor
```bash
curl http://localhost:3000/login
# ou
curl http://127.0.0.1:3000/login
```

Se funcionar localmente mas não externamente, o problema é firewall/rede.

---

## 🔥 Firewall (UFW - Ubuntu/Debian)

### Verificar status do firewall:
```bash
sudo ufw status
```

### Permitir porta 8080:
```bash
# Permitir porta específica
sudo ufw allow 3000/tcp

# Ou permitir por IP específico (mais seguro)
sudo ufw allow from SEU_IP to any port 3000

# Recarregar firewall
sudo ufw reload
```

### Verificar regras:
```bash
sudo ufw status numbered
```

### Remover regra (se necessário):
```bash
sudo ufw delete NUMERO_DA_REGRA
```

---

## 🔥 Firewall (firewalld - CentOS/RHEL)

```bash
# Verificar status
sudo firewall-cmd --state

# Permitir porta
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload

# Verificar
sudo firewall-cmd --list-ports
```

---

## 🌐 Firewall do Cloud Provider

### AWS (Security Groups)
1. Acesse o EC2 Console
2. Vá em Security Groups
3. Selecione o security group da sua instância
4. Adicione regra de entrada:
   - Type: Custom TCP
   - Port: 6000
   - Source: 0.0.0.0/0 (ou IP específico)
   - Description: ISO 27001 App

### Google Cloud (Firewall Rules)
```bash
gcloud compute firewall-rules create allow-iso27001 \
    --allow tcp:3000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow ISO 27001 app"
```

### Azure (Network Security Group)
1. Portal Azure → Network Security Groups
2. Adicione regra de entrada:
   - Port: 3000
   - Protocol: TCP
   - Action: Allow

### DigitalOcean (Firewall)
1. Networking → Firewalls
2. Create Firewall
3. Adicione regra de entrada:
   - Type: Custom
   - Protocol: TCP
   - Port Range: 3000
   - Sources: All IPv4, All IPv6

---

## 🔍 Verificações de Rede

### 1. Verificar se a porta está realmente escutando em todas as interfaces:
```bash
sudo netstat -tlnp | grep 3000
# Deve mostrar: 0.0.0.0:3000 ou :::3000

# Se mostrar apenas 127.0.0.1:3000, o problema é na configuração
```

### 2. Verificar IP do servidor:
```bash
# Ver IPs do servidor
ip addr show
# ou
hostname -I
```

### 3. Testar de outro servidor (se possível):
```bash
# De outro servidor/PC
curl http://IP_DO_SERVIDOR:3000/login
telnet IP_DO_SERVIDOR 3000
```

### 4. Verificar se há outros serviços na porta:
```bash
sudo lsof -i :3000
```

---

## 🐳 Docker Network

### Verificar se o Docker está mapeando corretamente:
```bash
docker port teinsta_web_1
# Deve mostrar: 6000/tcp -> 0.0.0.0:3000
```

### Se não estiver mapeando, verificar docker-compose.yml:
```yaml
ports:
  - "0.0.0.0:3000:6000"  # Externa:3000 -> Interna:6000
```

### Reiniciar container:
```bash
docker-compose down
docker-compose up -d
```

---

## 🔧 Solução Rápida (Ubuntu/Debian)

Execute este script para verificar e corrigir automaticamente:

```bash
#!/bin/bash
echo "=== Verificando Firewall ==="
sudo ufw status

echo -e "\n=== Permitindo porta 3000 ==="
sudo ufw allow 3000/tcp

echo -e "\n=== Verificando porta 3000 ==="
sudo netstat -tlnp | grep 3000

echo -e "\n=== Testando acesso local ==="
curl -I http://localhost:3000/login

echo -e "\n=== IP do servidor ==="
hostname -I

echo -e "\n✅ Verifique se consegue acessar: http://$(hostname -I | awk '{print $1}'):3000"
```

---

## 🔒 Segurança (Recomendado)

Em vez de abrir a porta 6000 para o mundo, considere:

### Opção 1: Nginx Reverse Proxy (Recomendado)
```nginx
# /etc/nginx/sites-available/iso27001
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    client_max_body_size 16M;
}
```

Então:
- Abra apenas porta 80/443 (HTTP/HTTPS)
- Use SSL/HTTPS com Let's Encrypt
- A porta 6000 fica apenas para localhost

### Opção 2: VPN/SSH Tunnel
```bash
# Acesse via SSH tunnel
ssh -L 6000:localhost:6000 usuario@servidor
# Depois acesse: http://localhost:6000
```

### Opção 3: IP Whitelist
```bash
# Permitir apenas IPs específicos
sudo ufw allow from SEU_IP to any port 3000
```

---

## 🧪 Teste Completo

Execute este comando para testar tudo:

```bash
echo "=== Status Container ==="
docker-compose ps

echo -e "\n=== Porta no Docker ==="
docker port teinsta_web_1 2>/dev/null || echo "Container não encontrado"

echo -e "\n=== Porta no Sistema ==="
sudo netstat -tlnp | grep 3000 || echo "Porta não encontrada"

echo -e "\n=== Firewall UFW ==="
sudo ufw status | grep 3000 || echo "Porta não encontrada no firewall"

echo -e "\n=== Teste Local ==="
curl -I http://localhost:3000/login 2>&1 | head -1

echo -e "\n=== IP do Servidor ==="
echo "Acesse: http://$(hostname -I | awk '{print $1}'):3000"
```

---

## ❓ Problemas Comuns

### "Connection refused" ou "ERR_UNSAFE_PORT"
- **ERR_UNSAFE_PORT:** A porta 6000 é bloqueada por navegadores. Use porta 3000!
- Firewall bloqueando
- Porta não está escutando
- Container não está rodando

### "Connection timeout"
- Firewall do cloud provider
- Rede bloqueando
- IP incorreto

### "502 Bad Gateway"
- Container não está respondendo
- Aplicação com erro
- Ver logs: `docker-compose logs`

---

## 📞 Próximos Passos

1. ✅ Verificar firewall local (UFW/firewalld)
2. ✅ Verificar firewall do cloud provider
3. ✅ Testar acesso local
4. ✅ Testar acesso externo
5. ✅ Configurar Nginx (recomendado para produção)
6. ✅ Configurar SSL/HTTPS (obrigatório para produção)

