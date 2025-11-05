# Guia de Deploy para Produção - Sistema ISO 27001

Este guia apresenta várias opções para fazer o deploy do sistema para produção.

## ⚠️ Preparações Antes do Deploy

### 1. Configurações de Segurança

**IMPORTANTE:** Antes de fazer deploy, você DEVE:

1. **Alterar a SECRET_KEY** no código ou via variável de ambiente:
   ```bash
   export SECRET_KEY="sua-chave-secreta-super-segura-aqui"
   ```

2. **Alterar a senha padrão** via variável de ambiente:
   ```bash
   export DASHBOARD_PASSWORD="sua-senha-segura-aqui"
   ```

3. **Configurar variáveis de ambiente** (veja `.env.example`)

### 2. Backup do Banco de Dados

Antes do deploy, faça backup do banco de dados local:
```bash
cp iso27001.db iso27001.db.backup
```

---

## Opção 1: Deploy com Docker (Recomendado)

### Requisitos
- Docker instalado
- Docker Compose (opcional)

### Passos

1. **Construir a imagem Docker:**
   ```bash
   docker build -t sistema-iso27001 .
   ```

2. **Executar o container:**
   ```bash
   docker run -d \
     -p 6000:6000 \
     -e SECRET_KEY="sua-chave-secreta" \
     -e DASHBOARD_PASSWORD="sua-senha" \
     -v $(pwd)/iso27001.db:/app/iso27001.db \
     -v $(pwd)/uploads:/app/uploads \
     --name iso27001-app \
     sistema-iso27001
   ```

3. **Ou usando Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Acessar a aplicação:**
   ```
   http://localhost:6000
   ```

### Vantagens
- ✅ Isolamento completo
- ✅ Fácil de replicar
- ✅ Portável entre ambientes

---

## Opção 2: Deploy em Render.com

Render é uma plataforma gratuita (com limitações) para aplicações web.

### Passos

1. **Criar conta em [Render.com](https://render.com)**

2. **Conectar repositório Git** (GitHub/GitLab)

3. **Configurar novo Web Service:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3

4. **Configurar variáveis de ambiente:**
   - `SECRET_KEY`: sua chave secreta
   - `DASHBOARD_PASSWORD`: sua senha
   - `PORT`: será definido automaticamente

5. **Configurar Disco Persistente** (para banco de dados):
   - No dashboard do Render, vá em "Disk"
   - Adicione um disco persistente
   - Monte em `/app/data`

6. **Ajustar código para usar disco persistente:**
   ```python
   # No app.py, alterar:
   DB_PATH = Path(os.environ.get('DATA_DIR', '.')) / 'iso27001.db'
   ```

### Vantagens
- ✅ Gratuito para começar
- ✅ Deploy automático via Git
- ✅ SSL/HTTPS automático

---

## Opção 3: Deploy em Railway.app

Railway é uma plataforma moderna e fácil de usar.

### Passos

1. **Criar conta em [Railway.app](https://railway.app)**

2. **Instalar CLI do Railway:**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

3. **No diretório do projeto:**
   ```bash
   railway init
   railway up
   ```

4. **Configurar variáveis de ambiente via dashboard:**
   - `SECRET_KEY`
   - `DASHBOARD_PASSWORD`
   - `PORT` (automático)

5. **Configurar volume persistente** para banco de dados

### Vantagens
- ✅ Muito fácil de usar
- ✅ Deploy automático
- ✅ SSL automático

---

## Opção 4: Deploy em Servidor VPS (Ubuntu/Debian)

### Requisitos
- Servidor VPS com Ubuntu/Debian
- Acesso SSH
- Python 3.8+ instalado

### Passos

1. **Conectar ao servidor:**
   ```bash
   ssh usuario@seu-servidor.com
   ```

2. **Atualizar sistema:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **Instalar dependências:**
   ```bash
   sudo apt install python3-pip python3-venv nginx supervisor -y
   ```

4. **Clonar/copiar o projeto:**
   ```bash
   cd /var/www
   git clone seu-repositorio.git iso27001
   cd iso27001
   ```

5. **Criar ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

6. **Configurar variáveis de ambiente:**
   ```bash
   nano .env
   ```
   Adicione:
   ```
   SECRET_KEY=sua-chave-secreta
   DASHBOARD_PASSWORD=sua-senha
   FLASK_ENV=production
   ```

7. **Configurar Supervisor (para manter aplicação rodando):**
   ```bash
   sudo nano /etc/supervisor/conf.d/iso27001.conf
   ```
   Adicione:
   ```ini
   [program:iso27001]
   directory=/var/www/iso27001
   command=/var/www/iso27001/venv/bin/gunicorn app:app --bind 127.0.0.1:6000 --workers 3
   user=www-data
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/iso27001/error.log
   stdout_logfile=/var/log/iso27001/access.log
   ```

8. **Criar diretório de logs:**
   ```bash
   sudo mkdir -p /var/log/iso27001
   sudo chown www-data:www-data /var/log/iso27001
   ```

9. **Iniciar Supervisor:**
   ```bash
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start iso27001
   ```

10. **Configurar Nginx (reverse proxy):**
    ```bash
    sudo nano /etc/nginx/sites-available/iso27001
    ```
    Adicione:
    ```nginx
    server {
        listen 80;
        server_name seu-dominio.com;

        location / {
            proxy_pass http://127.0.0.1:6000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        client_max_body_size 16M;
    }
    ```

11. **Ativar site Nginx:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/iso27001 /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

12. **Configurar SSL com Let's Encrypt (opcional mas recomendado):**
    ```bash
    sudo apt install certbot python3-certbot-nginx -y
    sudo certbot --nginx -d seu-dominio.com
    ```

### Vantagens
- ✅ Controle total
- ✅ Melhor performance
- ✅ Custo-benefício para uso intenso

---

## Opção 5: Deploy em Heroku

### Passos

1. **Instalar Heroku CLI:**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli

   # Linux/Mac
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login no Heroku:**
   ```bash
   heroku login
   ```

3. **Criar aplicação:**
   ```bash
   heroku create seu-app-iso27001
   ```

4. **Configurar variáveis de ambiente:**
   ```bash
   heroku config:set SECRET_KEY="sua-chave-secreta"
   heroku config:set DASHBOARD_PASSWORD="sua-senha"
   ```

5. **Configurar PostgreSQL (Heroku não persiste SQLite):**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
   
   **Nota:** Você precisará migrar de SQLite para PostgreSQL ou usar Heroku Postgres.

6. **Deploy:**
   ```bash
   git push heroku main
   ```

7. **Abrir aplicação:**
   ```bash
   heroku open
   ```

### Vantagens
- ✅ Fácil de usar
- ✅ Escalável
- ✅ Muitos add-ons disponíveis

---

## Opção 6: Deploy em PythonAnywhere

PythonAnywhere oferece hospedagem gratuita para aplicações Python.

### Passos

1. **Criar conta em [PythonAnywhere](https://www.pythonanywhere.com)**

2. **Fazer upload dos arquivos** via interface web ou Git

3. **Configurar aplicação web:**
   - Vá em "Web" → "Add a new web app"
   - Escolha "Flask"
   - Selecione Python 3.10

4. **Editar arquivo WSGI:**
   ```python
   import sys
   path = '/home/seu-usuario/iso27001'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Configurar variáveis de ambiente** no arquivo WSGI:
   ```python
   import os
   os.environ['SECRET_KEY'] = 'sua-chave'
   os.environ['DASHBOARD_PASSWORD'] = 'sua-senha'
   ```

6. **Reload aplicação**

### Vantagens
- ✅ Gratuito para começar
- ✅ Interface web amigável
- ✅ Bom para desenvolvimento/teste

---

## Configurações Importantes

### Variáveis de Ambiente

Crie um arquivo `.env` (não versionado) ou configure nas plataformas:

```bash
# Segurança
SECRET_KEY=sua-chave-secreta-muito-longa-e-aleatoria
DASHBOARD_PASSWORD=sua-senha-forte

# Ambiente
FLASK_ENV=production
PORT=6000

# Banco de Dados (se usar PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

### Backup do Banco de Dados

Configure backups automáticos:

```bash
# Script de backup diário
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /caminho/para/iso27001.db /backups/iso27001_$DATE.db
# Manter apenas últimos 30 dias
find /backups -name "iso27001_*.db" -mtime +30 -delete
```

### Monitoramento

Considere adicionar:
- Logs estruturados
- Monitoramento de erros (Sentry)
- Alertas de disponibilidade

---

## Troubleshooting

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Execute `pip install -r requirements.txt`

### Erro: "Database is locked"
- SQLite não é ideal para produção com múltiplos usuários
- Considere migrar para PostgreSQL

### Erro: "Permission denied"
- Verifique permissões de arquivos e pastas
- Garanta que `uploads/` seja gravável

### Aplicação não inicia
- Verifique logs: `sudo supervisorctl tail -f iso27001`
- Verifique variáveis de ambiente
- Teste localmente primeiro

---

## Migração de SQLite para PostgreSQL (Recomendado para Produção)

Para produção, considere migrar para PostgreSQL:

1. **Instalar psycopg2:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Modificar `app.py`** para usar PostgreSQL quando `DATABASE_URL` estiver definida

3. **Migrar dados:**
   ```bash
   # Exportar do SQLite
   sqlite3 iso27001.db .dump > dump.sql
   
   # Ajustar dump.sql para PostgreSQL e importar
   psql $DATABASE_URL < dump.sql
   ```

---

## Checklist Final

Antes de considerar produção:

- [ ] SECRET_KEY alterada
- [ ] Senha padrão alterada
- [ ] Variáveis de ambiente configuradas
- [ ] Backup do banco de dados configurado
- [ ] SSL/HTTPS configurado
- [ ] Logs configurados
- [ ] Testes realizados
- [ ] Monitoramento configurado
- [ ] Documentação atualizada

---

## Suporte

Para dúvidas ou problemas, consulte:
- Logs da aplicação
- Documentação da plataforma escolhida
- Issues do repositório

